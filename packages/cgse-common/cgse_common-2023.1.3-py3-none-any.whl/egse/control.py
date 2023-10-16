"""
This module defines the abstract class for any control server and some convenience functions.
"""
import abc
import logging
import pickle
import threading
import time
from typing import Any

import zmq

from egse.logger import close_all_zmq_handlers
from egse.process import ProcessStatus
from egse.settings import Settings
from egse.system import do_every
from egse.system import get_average_execution_time
from egse.system import get_average_execution_times
from egse.system import get_full_classname
from egse.system import get_host_ip
from egse.system import save_average_execution_time

MODULE_LOGGER = logging.getLogger(__name__)
PROCESS_SETTINGS = Settings.load("PROCESS")


def time_in_ms():
    """Returns the current time in milliseconds since the Epoch."""
    return int(round(time.time() * 1000))


def time_in_s():
    """Returns the current time in seconds since the Epoch."""
    return time.time()


def is_control_server_active(endpoint: str = None, timeout: float = 0.5) -> bool:
    """
    Check if the control server is running. This function sends a *Ping* message to the
    control server and expects a *Pong* answer back within the timeout period.

    Args:
        endpoint (str): the endpoint to connect to, i.e. <protocol>://<address>:<port>
        timeout (float): timeout when waiting for a reply [seconds, default=0.5]
    Returns:
        True if the Control Server is running and replied with the expected answer.
    """
    ctx = zmq.Context.instance()

    return_code = False

    try:
        socket = ctx.socket(zmq.REQ)
        socket.connect(endpoint)
        data = pickle.dumps("Ping")
        socket.send(data)
        rlist, _, _ = zmq.select([socket], [], [], timeout=timeout)
        if socket in rlist:
            data = socket.recv()
            response = pickle.loads(data)
            return_code = response == "Pong"
        socket.close(linger=0)
    except Exception as exc:
        MODULE_LOGGER.warning(f"Caught an exception while pinging a control server at {endpoint}: {exc}.")

    return return_code


class Response:
    """Base class for any reply or response between client-server communication.

    The idea is that the response is encapsulated in one of the subclasses depending
    on the type of response.
    """

    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return self.message

    @property
    def successful(self):
        """Returns True if the Response is not an Exception."""
        return not isinstance(self, Exception)


class Failure(Response, Exception):
    """A failure response indicating something went wrong at the other side.

    This class is used to encapsulate an Exception that was caught and needs to be
    passed to the client. So, the intended use is like this:
    ```
    try:
        # perform some useful action that might raise an Exception
    except SomeException as exc:
        return Failure("Our action failed", exc)
    ```
    The client can inspect the Exception that was originally raised, in this case `SomeException`
    with the `cause` variable.

    Since a Failure is also an Exception, the property `successful` will return False.
    So, the calling method can test for this easily.

    ```
    rc: Response = function_that_returns_a_response()

    if not rc.successful:
        # handle the failure
    else:
        # handle success
    ```

    """

    def __init__(self, message: str, cause: Exception = None):
        msg = f"{message}: {cause}" if cause is not None else message
        super().__init__(msg)
        self.cause = cause


class Success(Response):
    """A success response for the client.

    The return code from any action or function that needs to be returned to the
    client shall be added.

    Since `Success` doesn't inherit from `Exception`, the property `successful` will return True.
    """

    def __init__(self, message: str, return_code: Any = None):
        msg = f"{message}: {return_code}" if return_code is not None else message
        super().__init__(msg)
        self.return_code = return_code


class Message(Response):
    """A message response from the client.

    Send a Message when there is no Failure, but also no return code. This is the alternative of
    returning a None.

    Message returns True for the property successful since it doesn't inherit from Exception.
    """

    pass


class ControlServer(metaclass=abc.ABCMeta):
    """
    The base class for all device control servers and for the Storage Manager and Configuration
    Manager. A Control Server reads commands from a ZeroMQ socket and executes these commands by
    calling the `execute()` method of the commanding protocol class.

    The sub-class shall define the following:

    * Define the device protocol class -> `self.device_protocol`
    * Bind the command socket to the device protocol -> `self.dev_ctrl_cmd_sock`
    * Register the command socket in the poll set -> `self.poller`

    """

    def __init__(self):
        from egse.monitoring import MonitoringProtocol
        from egse.services import ServiceProtocol

        self._process_status = ProcessStatus()

        self._timer_thread = threading.Thread(
            target=do_every, args=(PROCESS_SETTINGS.METRICS_INTERVAL, self._process_status.update))
        self._timer_thread.daemon = True
        self._timer_thread.start()

        # The logger will be overwritten by the sub-class, if not, then we use this logger
        # with the name of the sub-class. That will help us to identify which sub-class did not
        # overwrite the logger attribute.

        self.logger = logging.getLogger(get_full_classname(self))

        self.interrupted = False
        self.delay = 1000  # delay between publish status information [milliseconds]
        self.hk_delay = 1000  # delay between saving housekeeping information [milliseconds]

        self.zcontext = zmq.Context.instance()
        self.poller = zmq.Poller()

        self.device_protocol = None  # This will be set in the sub-class
        self.service_protocol = ServiceProtocol(self)
        self.monitoring_protocol = MonitoringProtocol(self)

        # Setup the control server waiting for service requests

        self.dev_ctrl_service_sock = self.zcontext.socket(zmq.REP)
        self.service_protocol.bind(self.dev_ctrl_service_sock)

        # Setup the control server for sending monitoring info

        self.dev_ctrl_mon_sock = self.zcontext.socket(zmq.PUB)
        self.monitoring_protocol.bind(self.dev_ctrl_mon_sock)

        # Setup the control server waiting for device commands.
        # The device protocol shall bind the socket in the sub-class

        self.dev_ctrl_cmd_sock = self.zcontext.socket(zmq.REP)

        # Initialize the poll set

        self.poller.register(self.dev_ctrl_service_sock, zmq.POLLIN)
        self.poller.register(self.dev_ctrl_mon_sock, zmq.POLLIN)

    @abc.abstractmethod
    def get_communication_protocol(self):
        pass

    @abc.abstractmethod
    def get_commanding_port(self):
        pass

    @abc.abstractmethod
    def get_service_port(self):
        pass

    @abc.abstractmethod
    def get_monitoring_port(self):
        pass

    def get_ip_address(self):
        return get_host_ip()

    def get_storage_mnemonic(self):
        return self.__class__.__name__

    def get_process_status(self):
        return self._process_status.as_dict()

    def get_average_execution_times(self):
        return get_average_execution_times()

    def set_delay(self, seconds: float) -> float:
        """
        Sets the delay time for monitoring. The delay time is the time between two successive executions of the
        `get_status()` function of the device protocol.

        It might happen that the delay time that is set is longer than what you requested. That is the case when
        the execution of the `get_status()` function takes longer than the requested delay time. That should
        prevent the server from blocking when a too short delay time is requested.

        Args:
            seconds: the number of seconds between the monitoring calls.
        Returns:
            The delay that was set in milliseconds.
        """
        execution_time = get_average_execution_time(self.device_protocol.get_status)
        self.delay = max(seconds * 1000, (execution_time + 0.2) * 1000)
        return self.delay

    def set_hk_delay(self, seconds) -> float:
        """
        Sets the delay time for housekeeping. The delay time is the time between two successive executions of the
        `get_housekeeping()` function of the device protocol.

        It might happen that the delay time that is set is longer than what you requested. That is the case when
        the execution of the `get_housekeeping()` function takes longer than the requested delay time. That should
        prevent the server from blocking when a too short delay time is requested.

        Args:
            seconds: the number of seconds between the housekeeping calls.
        Returns:
            The delay that was set in milliseconds.
        """
        execution_time = get_average_execution_time(self.device_protocol.get_housekeeping)
        self.hk_delay = max(seconds * 1000, (execution_time + 0.2) * 1000)
        return self.hk_delay

    def set_logging_level(self, level):
        self.logger.setLevel(level=level)

    def quit(self):
        self.interrupted = True

    def before_serve(self):
        pass

    def after_serve(self):
        pass

    def serve(self):

        self.before_serve()

        # check if Storage Manager is available

        from egse.storage import is_storage_manager_active

        storage_manager = is_storage_manager_active(timeout=0.1)

        storage_manager and self.register_to_storage_manager()

        # This approach is very simplistic and not time efficient
        # We probably want to use a Timer that executes the monitoring and saving actions at
        # dedicated times in the background.

        last_time = time_in_ms()
        last_time_hk = time_in_ms()

        while True:
            try:
                socks = dict(self.poller.poll(50))  # timeout in milliseconds, do not block
            except KeyboardInterrupt:
                self.logger.warning("Keyboard interrupt caught!")
                self.logger.warning(
                    "The ControlServer can not be interrupted with CTRL-C, "
                    "send a quit command to the server."
                )
                continue

            if self.dev_ctrl_cmd_sock in socks:
                self.device_protocol.execute()

            if self.dev_ctrl_service_sock in socks:
                self.service_protocol.execute()

            # Now handle the periodic sending out of status information. A dictionary with the
            # status or HK info is sent out periodically based on the DELAY time that is in the
            # YAML config file.

            if time_in_ms() - last_time >= self.delay:
                last_time = time_in_ms()
                # self.logger.debug("Sending status to monitoring processes.")
                self.monitoring_protocol.send_status(
                    save_average_execution_time(self.device_protocol.get_status)
                )

            if time_in_ms() - last_time_hk >= self.hk_delay:
                last_time_hk = time_in_ms()
                if storage_manager:
                    # self.logger.debug("Sending housekeeping information to Storage.")
                    self.store_housekeeping_information(
                        save_average_execution_time(self.device_protocol.get_housekeeping)
                    )

            if self.interrupted:
                self.logger.info(
                    f"Quit command received, closing down the {self.__class__.__name__}."
                )
                break

            # Some device protocol sub-classes might start a number of threads or processes to
            # support the commanding. Check if these threads/processes are still alive and
            # terminate gracefully if they are not.

            if not self.device_protocol.is_alive():
                self.logger.error(
                    "Some Thread or sub-process that was started by Protocol has "
                    "died, terminating..."
                )
                break

        storage_manager and self.unregister_from_storage_manager()

        self.after_serve()

        self.device_protocol.quit()

        self.dev_ctrl_mon_sock.close()
        self.dev_ctrl_service_sock.close()
        self.dev_ctrl_cmd_sock.close()

        close_all_zmq_handlers()

        self.zcontext.term()

    def store_housekeeping_information(self, data):
        """Send housekeeping information to the Storage manager."""

        from egse.storage.storage_cs import StorageControlServer
        from egse.storage import StorageProxy

        if isinstance(self, StorageControlServer):
            self.logger.log(0, f"{self.__class__.__name__} doesn't store housekeeping information.")
            return

        self.logger.log(0, "Sending housekeeping to storage manager.")

        try:
            with StorageProxy() as proxy:
                rc = proxy.save({"origin": self.get_storage_mnemonic(), "data": data})
                if not rc.successful:
                    self.logger.warning(
                        f"Couldn't save data to the Storage manager: {data}, cause: {rc}"
                    )
        except ConnectionError as exc:
            self.logger.warning(
                f"Couldn't connect to the Storage manager to store housekeeping: {exc}"
            )

    def register_to_storage_manager(self):
        """Register this ControlServer to the Storage manager."""

        from egse.storage.storage_cs import StorageControlServer
        from egse.storage import StorageProxy
        from egse.storage.persistence import TYPES

        if isinstance(self, StorageControlServer):
            return

        try:
            with StorageProxy() as proxy:
                rc = proxy.register(
                    {
                        "origin": self.get_storage_mnemonic(),
                        "persistence_class": TYPES['CSV'],
                        "prep": {
                            "column_names": list(self.device_protocol.get_housekeeping().keys()),
                            "mode": "a",
                        },
                    }
                )
                if not rc.successful:
                    self.logger.warning(f"Couldn't register to the Storage manager: {rc}")
        except ConnectionError as exc:
            self.logger.warning(f"Couldn't connect to the Storage manager for registration: {exc}")

    def unregister_from_storage_manager(self):
        """Unregister this ControlServer from the Storage manager."""

        from egse.storage.storage_cs import StorageControlServer
        from egse.storage import StorageProxy

        if isinstance(self, StorageControlServer):
            return

        try:
            with StorageProxy() as proxy:
                rc = proxy.unregister({"origin": self.get_storage_mnemonic()})
                if not rc.successful:
                    self.logger.warning(f"Couldn't unregister from the Storage manager: {rc}")

        except ConnectionError as exc:
            self.logger.warning(
                f"Couldn't connect to the Storage manager for de-registration: {exc}"
            )
