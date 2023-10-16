# Copyright 2023-2023 by AccidentallyTheCable <cableninja@cableninja.net>.
# All rights reserved.
# This file is part of AccidentallyTheCables Utility Kit,
# and is released under "GPLv3". Please see the LICENSE
# file that should have been included as part of this package.
#### END COPYRIGHT BLOCK ###
import logging
import threading
import typing
from pathlib import Path
from time import sleep
from sys import exit as sys_exit

from atckit.subscriber import FunctionSubscriber
from atckit.utilfuncs import UtilFuncs

class Service:
    """Service Controller
    Modify Service threads by adding to or subtracting from Service.services (See FunctionSubscriber)
    """

    _SERVICE_NAME:str# = "myservice"
    _SERVICE_SHUTDOWN_LIMIT:int# = 300
    _SERVICE_CHECK_TIME:float# = 0.5
    services:FunctionSubscriber

    _config_file:Path
    _config_path:Path
    _pid_dir:Path
    _pid_file:Path
    _config:dict[str,typing.Any]
    _service_threads:dict[typing.Callable,threading.Thread]

    @property
    def should_run(self) -> bool:
        """Should be running Flag
        Combine shutdown and restart
        @retval bool Should be Running
        """
        return not (self.shutdown or self.restart)

    @property
    def shutdown(self) -> bool:
        """Shutdown Flag
        Passthrough to Utilfuncs.shutdown
        """
        return UtilFuncs.shutdown

    @shutdown.setter
    def shutdown(self,value:bool) -> None:
        """Shutdown Flag
        Passthrough to Utilfuncs.shutdown
        @param bool value Flag Value
        """
        UtilFuncs.shutdown = value

    @property
    def restart(self) -> bool:
        """Restart Flag
        Passthrough to Utilfuncs.restart
        """
        return UtilFuncs.restart

    @restart.setter
    def restart(self,value:bool) -> None:
        """Restart Flag
        Passthrough to Utilfuncs.restart
        @param bool value Flag Value
        """
        UtilFuncs.restart = value

    logger:logging.Logger

    def __init__(self) -> None:
        """Initializer
        Read Config
        Write PID
        @throws ValueError: invalid self._mode
        """
        if not hasattr(self,"_SERVICE_CHECK_TIME"):
            self._SERVICE_CHECK_TIME = 0.5
        if not hasattr(self,"_SERVICE_SHUTDOWN_LIMIT"):
            self._SERVICE_SHUTDOWN_LIMIT = 300
        if not hasattr(self,"_SERVICE_NAME"):
            raise ValueError(f"Service name must be defined in {type(self).__qualname__}._SERVICE_NAME")
        UtilFuncs.register_signals()
        self.logger = UtilFuncs.create_object_logger(self)
        self.services = FunctionSubscriber()
        self._service_threads = {}
        config_path:typing.Union[Path,None] = UtilFuncs.find_config_file(self._SERVICE_NAME,self._SERVICE_NAME)
        if config_path is None:
            self.logger.critical(f"Unable to locate configuration file for {self._SERVICE_NAME}")
            self._config = {}
        else:
            self._config_file = config_path
            self._config_path = config_path.parent
            config_file_str:str = self._config_file.as_posix()
            self.logger.debug(f"Loading {config_file_str}")
            self._config = UtilFuncs.load_sfile(self._config_file)

        if "pid_dir" not in self._config.keys():
            self._pid_dir = Path(f"/var/run/{self._SERVICE_NAME}/")
        else:
            self._pid_dir = Path(self._config["pid_dir"]).resolve()
        self._pid_file = self._pid_dir.joinpath(f"{self._SERVICE_NAME}.pid")
        try:
            UtilFuncs.register_pid(self._SERVICE_NAME,self._pid_dir)
        except BaseException as e:
            self.logger.critical("Register PID failed, See Exception information",exc_info=e)
            sys_exit(1)

    def run(self) -> None:
        """Start Service Thread(s)
        @retval None Nothing
        """
        while not self.shutdown:
            for f in self.services.functions:
                t:threading.Thread
                if f in self._service_threads.keys():
                    t = self._service_threads[f]
                    if not t.is_alive():
                        self.logger.warning(f"Thread for {f.__qualname__} was not running, starting again")
                        self._service_threads[f] = t = threading.Thread(target=f,name=f"{self._SERVICE_NAME}.service")
                        t.start()
                    else:
                        # self.logger.debug(f"Thread for {f.__qualname__} already running")
                        continue
                else:
                    self.logger.info(f"Creating Thread for {f.__qualname__}")
                    t = threading.Thread(target=f,name=f"{self._SERVICE_NAME}.service")
                    t.start()
                    self._service_threads[f] = t
            if self.restart:
                self._stop_threads()
                self.restart = False
            sleep(self._SERVICE_CHECK_TIME)

    def _stop_threads(self) -> bool:
        """Wait for all threads to stop
        @retval bool Threads stopped or timed out waiting
        """
        running_threads:int = len(self._service_threads)
        wait_count:int = 0
        service_threads:dict[typing.Callable,threading.Thread]
        error:bool = False
        while running_threads > 0:
            self.logger.info(f"Waiting for {str(running_threads)} thread(s) to stop")
            if wait_count > self._SERVICE_SHUTDOWN_LIMIT:
                self.logger.error("Timed out waiting for all threads to shutdown. This is likely a developer error")
                for f in self._service_threads.keys():
                    self.logger.error(f"Running Thread: {f.__qualname__}")
                    error = True
                break
            service_threads = self._service_threads.copy()
            for f,t in service_threads.items():
                if t.is_alive():
                    self.logger.debug(f"Waiting for {f.__qualname__} to finish its thread.")
                else:
                    self.logger.debug(f"Thread for {f.__qualname__} has finished.")
                    self._service_threads.pop(f)
            wait_count += 1
            running_threads = len(self._service_threads)
            sleep(1)
        return error

    def stop(self) -> None:
        """Stop Service Thread(s)
        @retval None Nothing
        """
        error:bool = self._stop_threads()
        self._pid_file.unlink()
        if error:
            sys_exit(4)

    # def service(self) -> None:
    #     """Service Thread Functionality
    #     @retval None Nothing
    #     """
    #     pass
