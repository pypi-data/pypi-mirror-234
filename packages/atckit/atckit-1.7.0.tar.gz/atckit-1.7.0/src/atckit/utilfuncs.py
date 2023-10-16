# Copyright 2023-2023 by AccidentallyTheCable <cableninja@cableninja.net>.
# All rights reserved.
# This file is part of AccidentallyTheCables Utility Kit,
# and is released under "GPLv3". Please see the LICENSE
# file that should have been included as part of this package.
#### END COPYRIGHT BLOCK ###
import datetime
import re
import sys
import signal
import logging
import typing
from os import kill,getpid
from pathlib import Path
from json import loads as json_parse
from json import dumps as json_dump
from yaml import dump as yaml_dump
from yaml import safe_load as yaml_parse
from tomlkit import parse as toml_parse
from tomlkit import dumps as toml_dump

def toml_parser(content:str) -> dict[typing.Any,typing.Any]:
    """TOML Parse and unwrap
    @param str \c content Raw TOML string
    @retval dict[Any,Any] Dictionary from TOML
    """
    return toml_parse(content).unwrap()

class UtilFuncs:
    """Utility Functions
    """

    FILE_TYPE_MAP:dict[str,typing.Callable] = {
        ".yml": yaml_parse,
        ".yaml": yaml_parse,
        ".json": json_parse,
        ".toml": toml_parser
    }
    TYPE_OVERRIDE_MAP:dict[str,typing.Callable] = {
        "yaml": yaml_parse,
        "json": json_parse,
        "toml": toml_parser
    }
    OUTPUT_TYPE_MAP:dict[str,typing.Callable] = {
        "yaml": yaml_dump,
        "json": json_dump,
        "toml": toml_dump
    }

    CONFIG_SCAN_BASE_PATHS:list[Path] = [
        Path("~/.local/"),
        Path("/etc/")
    ]

    CONFIG_SCAN_FILE_EXTS:list[str] = [
        "json",
        "yaml",
        "toml"
    ]

    shutdown:bool = False
    restart:bool = False

    @staticmethod
    def create_object_logger(obj:object) -> logging.Logger:
        """Create logging.Logger with Specified object Class Name
        @param object \c obj Object to Create Logger for
        @retval logging.Logger Logger Instance
        """
        classname:str = str(obj.__class__.__qualname__)
        return logging.getLogger(classname)

    @staticmethod
    def create_static_logger(classname:str) -> logging.Logger:
        """Create logging.Logger with Specified Name
        @param str \c classname Name of Logger to Create
        @retval logging.Logger Logger Instance
        """
        return logging.getLogger(classname)

    @staticmethod
    def deltatime_str(time:str) -> datetime.timedelta:
        """Create datetime.timedelta from Time string
        @param str \c time Time String
        @throws ValueError Invalid Format
        @retval datetime.timedelta timedelta object

        Format: `0Y0M0w0d0h0m0s0ms`

        Not all entries are required, ex: `1d4h20m` is acceptable
        """
        time_match:typing.Union[re.Match,None] = re.search(r'^(\d+Y)?(\d+M)?(\d+w)?(\d+d)?(\d+h)?(\d+m)?(\d+s)?(\d+ms)?$',time)
        if time_match is None:
            raise ValueError("Invalid Format. Expects some part of: 0Y0M0w0d0h0m0s0ms")
        values:list[int] = [ 0, 0, 0, 0, 0 ]
        i:int = 0
        for value in time_match.groups():
            if value is not None:
                v:int = int(re.sub(r'[YMwdhms]{1,2}$','',value))
                if re.match(r'.*Y$',value):
                    values[0] += 365 * v
                elif re.match(r'.*M$',value):
                    values[0] += 30 * v
                elif re.match(r'.*w$',value):
                    values[0] += 7 * v
                elif re.match(r'.*d$',value):
                    values[0] += v
                elif re.match(r'.*[hms]$',value):
                    values[i] += v
                    i += 1
                continue
            i += 1
        return datetime.timedelta(days=values[0],hours=values[1],minutes=values[2],seconds=values[3],milliseconds=values[4])

    @staticmethod
    def dump_sstr(content:dict[typing.Any,typing.Any],output_type:str,**kwargs:typing.Any) -> str:
        """Dump Structured Data to String, Selectable Output Type.
        @param dict[Any,Any] \c content Content to dump
        @param str \c output_type Output Type, Allowed: yaml, json, toml
        @param kwargs \c kwargs kwargs passed to selected data dumper
        @retval str Structured Data as a string
        @exception LookupError Raised When Unable to Locate a a parser by file type, or the overridden type is invalid
        @exception RuntimeError Raised When Unable to Parse the specified file using the specified type (automatically, or overridden)

        kwargs:
            See the related kwargs for:
                json.dumps
                yaml.dump
                tomlkit.dumps
        """
        if output_type not in UtilFuncs.OUTPUT_TYPE_MAP.keys():
            raise LookupError("Output Type is not valid",output_type)
        dumper:typing.Callable = UtilFuncs.OUTPUT_TYPE_MAP[output_type]
        try:
            output:str = dumper(content,*kwargs)
        except BaseException as e:
            raise RuntimeError("Failed to output content",'.'.join([dumper.__class__.__name__,dumper.__name__]),e) from e
        return output

    @staticmethod
    def load_sstr(raw_data:str,content_type:str) -> dict[typing.Any,typing.Any]:
        """Load Structured Data Content, based on content_type
        @param str \c raw_data Raw Content
        @param str \c content_type Render for Content Type, Allowed: yaml, json, toml
        @retval dict[Any,Any] Dictionary of Structured Data
        """
        parser:typing.Callable
        if content_type not in UtilFuncs.TYPE_OVERRIDE_MAP.keys():
            raise LookupError("Override Type is not valid",content_type)
        parser = UtilFuncs.TYPE_OVERRIDE_MAP[content_type]
        loaded_config:dict[typing.Any,typing.Any] = parser(raw_data)
        return loaded_config

    @staticmethod
    def load_sfile(target_file:Path,override_type:str = "auto") -> dict[typing.Any,typing.Any]:
        """Load Structured Data File, automatically determining data by file extension
        @param Path \c target_file Configuration File to Load
        @param str \c override_type Input Type Override, Allowed: yaml, json, toml, auto. Default: auto
        @retval dict[Any,Any] Dictionary of Structured Data
        @exception LookupError Raised When Unable to Locate a a parser by file type, or the overridden type is invalid
        @exception RuntimeError Raised When Unable to Parse the specified file using the specified type (automatically, or overridden)

        Accepted File Extensions:
            YAML: .yaml, .yml
            JSON: .json
            TOML: .toml
        """
        if not target_file.exists():
            raise FileNotFoundError("Cannot Locate File",target_file.as_posix())
        content_type:str = override_type
        if override_type == "auto":
            if target_file.suffix not in UtilFuncs.FILE_TYPE_MAP.keys():
                raise LookupError("No Parser located for file type",target_file.suffix)
            content_type = re.sub(r'^\.','',target_file.suffix)
        try:
            with open(target_file,"r",encoding="utf-8") as f:
                loaded_config:dict[typing.Any,typing.Any] = UtilFuncs.load_sstr(f.read(),content_type)
                return loaded_config
        except BaseException as e:
            raise RuntimeError("Failed to Parse file",target_file.as_posix(),e) from e

    @staticmethod
    def find_config_file(service:str,config_name:str) -> typing.Union[Path,None]:
        """Search for Configuration File in common places

        Uses UtilFuncs.CONFIG_SCAN_BASE_PATHS and UtilFuncs.CONFIG_SCAN_FILE_EXTS to search for files

        Scans as: <scan path>/<service>/<config_name>.<scan ext>

        @param str \c service Name of Service to Use (EX: myservice)
        @param str \c config_name Name of Configration File to find
        @retval Union[Path,None] Located configuration path, or None if not found
        """
        for p in UtilFuncs.CONFIG_SCAN_BASE_PATHS:
            check_svcpath:Path = p.joinpath(service).resolve()
            if not check_svcpath.is_dir():
                continue
            for ext in UtilFuncs.CONFIG_SCAN_FILE_EXTS:
                check_file:Path = check_svcpath.joinpath(f"{config_name}.{ext}").resolve()
                if check_file.is_file():
                    return check_file
        return None

    @staticmethod
    def add_config_search_path(path:Path) -> None:
        """Add Basepath to Config Search (EX /usr/local/)
        @param Path \c path Basepath to add for scanning
        @retval None Nothing
        """
        if path not in UtilFuncs.CONFIG_SCAN_BASE_PATHS:
            UtilFuncs.CONFIG_SCAN_BASE_PATHS.append(path)

    @staticmethod
    def remove_config_search_path(path:Path) -> None:
        """Remove Basepath from Config Search
        @param Path \c path Basepath to attempt to remove
        @retval None Nothing
        """
        try:
            UtilFuncs.CONFIG_SCAN_BASE_PATHS.pop(UtilFuncs.CONFIG_SCAN_BASE_PATHS.index(path))
        except ValueError:
            return

    @staticmethod
    def add_config_search_file_ext(ext:str) -> None:
        """Add File Extension to Config Search (EX conf)
        @param str \c ext File Extension to add for scanning
        @retval None Nothing
        """
        if ext not in UtilFuncs.CONFIG_SCAN_FILE_EXTS:
            UtilFuncs.CONFIG_SCAN_FILE_EXTS.append(ext)

    @staticmethod
    def remove_config_search_file_ext(ext:str) -> None:
        """Remove File Extension from Config Search
        @param str \c ext File Extension to attempt to remove
        @retval None Nothing
        """
        try:
            UtilFuncs.CONFIG_SCAN_FILE_EXTS.pop(UtilFuncs.CONFIG_SCAN_FILE_EXTS.index(ext))
        except ValueError:
            return

    @staticmethod
    def scan_dir(target_path:Path,
                 callback:typing.Callable[[Path,dict[str,typing.Any]],None],
                 callback_data:dict[str,typing.Any],
                 exclude_dirs:typing.Optional[list[re.Pattern]] = None,
                 exclude_files:typing.Optional[list[re.Pattern]] = None,
                 include_files:typing.Optional[list[re.Pattern]] = None
                ) -> None:
        """Scan A Directory, and Execute callback on discovered files, that do not match the exclusions
        @param Path \c target_path Path to Scan for Files
        @param typing.Callable[[Path,dict[str,Any]],None] \c callback Callback function to execute on each file
        @param dict[str,Any] \c callback_data Data to pass to the callback function
        @param list[re.Pattern] \c exclude_dirs (optional) Regex Compiled list of directory patterns to exclude
        @param list[re.Pattern] \c exclude_files (optional) Regex Compiled list of file patterns to exclude
        @param list[re.Pattern] \c include_files (optional) Regex Compiled list of file patterns to include
        """
        files:typing.Generator[Path, None, None] = target_path.glob("*")
        skip:bool = False
        for file in files:
            file_path:Path = Path(file)
            if file_path.is_dir():
                skip = False
                if exclude_dirs is not None:
                    for reg in exclude_dirs:
                        if reg.match(file_path.name):
                            skip = True
                            break
                if not skip:
                    UtilFuncs.scan_dir(target_path=file_path,callback=callback,callback_data=callback_data,exclude_dirs=exclude_dirs,exclude_files=exclude_files)
            if file_path.is_file():
                if include_files is not None:
                    skip = True
                    for reg in include_files:
                        if reg.match(file_path.name):
                            skip = False
                            break
                if exclude_files is not None:
                    skip = False
                    for reg in exclude_files:
                        if reg.match(file_path.name):
                            skip = True
                            break
                if not skip:
                    callback(file_path,callback_data)

    @staticmethod
    def deep_sort(input:dict[str,typing.Any]) -> dict[str,typing.Any]:
        """Deep Sort Dictionaries of varying data
        @param dict[str,typing.Any] \c input Input Dictionary
        @retval dict[str,typing.Any] New Sorted Dictionary
        """
        new_dict:dict[str,typing.Any] = {}
        for k,v in input.items():
            if isinstance(v,dict):
                new_dict[k] = dict(sorted(v.items()))
            elif isinstance(v,list):
                new_list:list[typing.Any] = []
                for i in v:
                    if isinstance(i,dict):
                        new_list.append(UtilFuncs.deep_sort(i))
                    else:
                        new_list.append(i)
                new_dict[k] = new_list
            else:
                new_dict[k] = v
        return new_dict

    @staticmethod
    def register_pid(service:str,pid_dir:Path = Path("/var/run/")) -> None:
        """Write Process ID to pid file at <pid_dir>/<service>.pid
        @param str service Service Name
        @param Path pid_dir Directory to write pid file to
        @retval None Nothing
        """
        pid_file:Path = pid_dir.joinpath(f"{service}.pid")
        if not pid_dir.exists():
            pid_dir.mkdir(parents=True,exist_ok=True)
        if pid_file.exists():
            with open(pid_file, "r", encoding="utf-8") as f:
                read_pid:int = int(f.read())
            if UtilFuncs.check_pid(read_pid):
                raise SystemError("Cannot start another process, one is already running",read_pid)
        with open(pid_file, "w", encoding="utf-8") as f:
            f.write(str(getpid()))

    @staticmethod
    def check_pid(pid:int) -> bool:
        """Check if PID exists (via os.kill(..,0))
        @param int \c pid PID to check
        @retval bool Whether PID exists or not
        """
        try:
            kill(pid,0)
        except OSError:
            return False
        return True

    # pylint: disable=unused-argument
    @staticmethod
    def sighandler(signum:int, frame:typing.Any) -> None:
        """Signal Handler
        @param signal.Signals \c signum Raised Signal
        @param Any \c frame Frame which raised the signal
        @retval None Nothing
        """
        logging.warning("Signal thrown")

        restart_signals:list[signal.Signals] = []
        shut_signals:list[signal.Signals] = []
        if sys.platform == "win32":
            shut_signals = [ signal.SIGINT, signal.CTRL_C_EVENT ]
            restart_signals = [ ]
        else:
            shut_signals = [ signal.SIGABRT, signal.SIGILL, signal.SIGINT, signal.SIGTERM ]
            restart_signals = [ signal.SIGHUP ]

        if signum in shut_signals:
            UtilFuncs.shutdown = True
            logging.info("Shutting Down")
            return
        if signum in restart_signals:
            logging.info("Reloading Service")
            UtilFuncs.restart = True
            return
    # pylint: enable=unused-argument

    @staticmethod
    def register_signals() -> None:
        """Register Signal Handlers
        @retval None Nothing
        """
        signals:list[signal.Signals] = []
        if sys.platform == "win32":
            signals = [ signal.SIGINT ]
        else:
            signals = [ signal.SIGABRT, signal.SIGILL, signal.SIGINT, signal.SIGTERM, signal.SIGHUP ]
        for sig in signals:
            signal.signal(sig,UtilFuncs.sighandler)
