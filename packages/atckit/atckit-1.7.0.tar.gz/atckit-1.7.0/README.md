# ATCKit

AccidentallyTheCable's Utility Kit

- [ATCKit](#atckit)
  - [About](#about)
    - [How does it work?](#how-does-it-work)
  - [Usage](#usage)
    - [FunctionSubscriber](#functionsubscriber)
  - [UtilFuncs](#utilfuncs)
    - [`create_object_logger`](#create_object_logger)
    - [`create_static_logger`](#create_static_logger)
    - [`deltatime_str`](#deltatime_str)
    - [`dump_sstr`](#dump_sstr)
    - [`load_sstr`](#load_sstr)
    - [`load_sfile`](#load_sfile)
    - [`scan_dir`](#scan_dir)
    - [`deep_sort`](#deep_sort)
    - [`check_pid`](#check_pid)
    - [`register_pid`](#register_pid)
    - [`register_signals`](#register_signals)
    - [`find_config_file`](#find_config_file)
    - [`add_config_search_path`](#add_config_search_path)
    - [`remove_config_search_path`](#remove_config_search_path)
    - [`add_config_search_file_ext`](#add_config_search_file_ext)
    - [`remove_config_search_file_ext`](#remove_config_search_file_ext)
  - [Service](#service)
  - [Version](#version)
    - [Version Search Strings](#version-search-strings)
      - [`version_locator`](#version_locator)
      - [`version_search_merge`](#version_search_merge)

## About

This is a small kit of classes, util functions, etc that I found myself rewriting or reusing frequently, and instead of copying everywhere, they are now here.


### How does it work?

Do the needfuls.... *do the needful dance*

Literally, import whatever you need to use..

## Usage

### FunctionSubscriber

A Class container for Function callback subscription via `+=` or `-=`. Functions can be retrieved in order of addition.

```
subscriber = FunctionSubscriber()

def a():
    print("I am a teapot")

def b():
    print("I am definitely totally not also a teapot, I swear")

subscriber += a
subscriber += b

for cb in subscriber.functions:
    cb()

>> I am a teapot
>> I am definitely totally not also a teapot, I swear
```

This class uses the `typing.Callable` type for function storage. You can extend the `FunctionSubscriber` class to define the
callback function parameters, etc.

```
class MySubscriber(FunctionSubscriber):
    """My Function Subscriber
    Callback: (bool) -> None
    """

    _functions:list[Callable[[bool],None]]

    def __iadd__(self,fn:Callable[[bool],None]) -> Self:
        """Inline Add. Subscribe Function
        @param method \c fn Method to Subscribe
        """
        return super().__iadd__(fn)

    def __isub__(self,fn:Callable[[bool],None]) -> Self:
        """Inline Subtract. Unsubscribe Function
        @param method \c fn Method to Unsubscribe
        """
        return super().__isub__(fn)
```

## UtilFuncs

A Class containing various static methods:

### `create_object_logger`

 Create `logging.Logger` instance for object specifically

### `create_static_logger`

 Create `logging.Logger` instance of a specified name

### `deltatime_str`

 Create `datetime.timedelta` from short formatted time string. Format: `0Y0M0w0d0h0m0s0ms`

### `dump_sstr`
 
 Dump Structured Data (dict) to str of specified format. Accepts JSON, YAML, TOML

### `load_sstr`

 Load Structured Data from String. Accepts JSON, YAML, TOML

### `load_sfile`
 
 Load Structured Data from File, automatically determining data by file extension. Accepts JSON, YAML, TOML
### `scan_dir`
 
 Search a specified Path, and execute a callback function on discovered files.
   - Allows exclusion of Files/Dirs via regex pattern matching
### `deep_sort`
 
 Sort a Dictionary recursively, including through lists of dicts
### `check_pid`
 
 Check if a process ID exists (via kill 0)
### `register_pid`
 
 Register (Write) process ID in specified directory as `<service>.pid`
### `register_signals`
 
 Register Shutdown / Restart Handlers
   - Check for Shutdown via UtilFuncs.shutdown (bool)
   - Check for Restart via UtilFuncs.restart (bool)

### `find_config_file`
 
 Look for config file in 'well defined' paths. Searches for `<service>/<config>.[toml,json,yaml]` in `~/.local/` and `/etc/` (in that order)

### `add_config_search_path`
 
 Add Search Path for [`find_config_file`](#find_config_file)

### `remove_config_search_path`
 
 Remove Search Path for [`find_config_file`](#find_config_file)

### `add_config_search_file_ext`
 
 Add file extension for [`find_config_file`](#find_config_file)

### `remove_config_search_file_ext`
 
 Remove file extension for [`find_config_file`](#find_config_file)

## Service

A Service / Daemon Class. Responds to signals properly, including HUP to restart threads

HUP does not restart main thread. So if the main configuration file needs to be re-read, the service needs to be stopped and started completely.

Entrypoint functions for services are defined under the `.services` [`FunctionSubscriber`](#FunctionSubscriber). These functions should be loopable, or be capable of starting again each time the function completes.

Create a class, which extends `Service`, such as `MyService`.

 - Set Service Name: `MyService._SERVICE_NAME = "myservice"`
 - Set Shutdown Time Limit: `MyService._SERVICE_SHUTDOWN_LIMIT = 300` (default shown)
 - Set Thread Check Interval: `MyService._SERVICE_CHECK_TIME = 0.5` (default shown)
 - Configuration Loading: Utilizes [`UtilFuncs.find_config_file()`](#find_config_file) and [`UtilFuncs.load_sfile()`](#load_sfile), will attempt to load `<service_name>/<service_name>.[toml,yaml,json]` from 'well known' paths, configuaration available in `MyService._config`. Additional locations can be added with [`UtilFuncs.add_config_search_path()`](#add_config_search_path)
 - Subscribe / Create Thread: `MyService.services += <function>`
 - Unsubscribe / Remove Thread: `MyService.services -= <function>`
 - Shutdown: Set `MyService.shutdown` (bool), Utilizes `Utilfuncs.shutdown`
 - Restart: Set `MyService.restart` (bool), Utilizes `Utilfuncs.restart`
 - Run Check: Check `MyService.should_run` to see if thread needs to stop
 - Run: Call `MyService.run()`
 - Stop: Call `MyService.stop()`
 - Signal Handlers: Utilizes [`Utilfuncs.register_signals()`](#register_signals)
 - Process ID storage: Set `pid_dir` in Configuration File

Example Service Functions:

```
import logging
from time import sleep

from atckit.service import Service

class MyService(Service):
    def __init__(self) -> None:
        super().__init__()
        self.services += self._testloopA # Add Thread to Service
        self.services += self._testloopB # Add another Thread

    def _testloopA(self) -> None:
        """Test Function, Continuous loop
        @retval None Nothing
        """
        while self.should_run:
            self.logger.info("Loop test")
            sleep(1)

    def _testloopB(self) -> None:
        """Test Function, One Shot, restarting at minimum every `MyService._SERVICE_CHECK_TIME` seconds
        @retval None Nothing
        """
        self.logger.info("Test Looop")
        sleep(1)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG) # Logging Configuration
    service:MyService = MyService() # Initialize Service
    service.run() # Stop with ABRT/INT/TERM CTRL+C
    service.stop() # Cleanup / Wait for Shutdown
```

## Version

A Class for version manipulation.

A Version can be created from:
 - Semantic String (`"1.0.0"`)
 - List of Strings or Ints of a version (`["1","0","0"]` or `[1,0,0]`)
 - Tuple of Strings or Ints of a version (`("1","0","0")` or `(1,0,0)`)

Versions are comparable (`>`,`<`,`>=`,`<=`,`==`,`!=`)
Versions are addable and subtractable (`a -= b`, `a += b`)
 - During subtraction, if a part goes negative, it will be set to 0

### Version Search Strings

To make Version things even easier, 2 functions are also included in the Version module, which enables a list of matching versions to be created, from the search.

Version Search Strings are 1 or more entries in a specially formatted string: `<comparator>:<version>,...`

Supported comparators: `>`,`<`,`>=`,`<=`,`==`,`!=`

Example Searches:

 - ">=:1.0.0,!=:2.0.2,<=:4.0.0"
 - "<=:3.0.0,>:0.9.0"

#### `version_locator`

Given a list of versions, locate a version which matches a given search string.

 - Example 1 matching:
   - Any Version Newer than 1.0.0, including 1.0.0
   - Not Version 2.0.2
   - Any Version Older than 4.0.0, including 4.0.0
 - Example 2 matching:
   - Any Version Older than 3.0.0, including 3.0.0
   - Any Version Newer than 0.9.0, not including 0.9.0

#### `version_search_merge`

Combine 2 Version Search Strings, creating a single string, which satisfies all searches in each string.

Given the examples above, merging these two searches, would result in the following compatible search: `>=:1.0.0,<=:3.0.0,!=:2.0.2`
