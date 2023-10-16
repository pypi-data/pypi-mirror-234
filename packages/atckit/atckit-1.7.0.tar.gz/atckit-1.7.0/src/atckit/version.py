# Copyright 2023-2023 by AccidentallyTheCable <cableninja@cableninja.net>.
# All rights reserved.
# This file is part of AccidentallyTheCables Utility Kit,
# and is released under "GPLv3". Please see the LICENSE
# file that should have been included as part of this package.
#### END COPYRIGHT BLOCK ###
import typing

def version_locator(search_version_str:str, version_list:list[str]) -> list[str]:
    """Using a Version search string, find versions which match from version_list
    @param str \c search_version_str Search String, format is `<comparator>:<version>,...`
    @param list[str] \c version_list List of Versions to search through
    @retval list[str] Versions which match the specified search string.
    """
    result:list[str] = []
    parts_versions:list[Version] = []
    parts_checks:list[str] = []
    for p in search_version_str.split(','):
        s:list[str] = p.split(':')
        parts_versions.append(Version(s[1]))
        parts_checks.append(s[0])
    for v in version_list:
        version:Version = Version(v)
        matched:bool = True
        for i in range(0,len(parts_versions)):
            check_mode:str = parts_checks[i]
            check_vers:Version = parts_versions[i]
            if check_mode == ">=":
                matched = version >= check_vers
            elif check_mode == "<=":
                matched = version <= check_vers
            elif check_mode == "==":
                matched = version == check_vers
            elif check_mode == "!=":
                matched = version != check_vers
            elif check_mode == ">":
                matched = version > check_vers
            elif check_mode == "<":
                matched = version < check_vers
            else:
                raise SyntaxError("Invalid Version Search comparator for Version")
            if not matched:
                break
        if matched:
            result.append(v)
    return result

def version_search_merge(search_a:str,search_b:str) -> str:
    """Version Search String Merger
    Combine 2 Version Search Strings (`<comparator>:<version>,...`) to form a single viable search
    @param str \c search_a Version Search String 1
    @param str \c search_b Version Search String 2
    @retval Combined Search String
    """
    versions:list[str] = []
    parts:list[str] = []
    # Create Versions and Comparators for Each Search String
    for part in search_a.split(','):
        s:list[str] = part.split(':')
        parts.append(s[0])
        versions.append(s[1])
    for part in search_b.split(','):
        s:list[str] = part.split(':')
        parts.append(s[0])
        versions.append(s[1])

    result_versions:list[str] = []
    result_output:list[str] = []

    # Create 1 query with combined searches, and locate the versions from search that match
    result_versions = version_locator(f"{search_a},{search_b}",versions)
    # Locate Comparators for each version, to build the final search
    for result_version in result_versions:
        result_comparator:str = parts[versions.index(result_version)]
        result_output.append(f"{result_comparator}:{result_version}")
    # Ensure we include version exclusions as well, if they exist
    if "!=" in parts:
        for i in range(0,len(parts)):
            if parts[i] == "!=":
                nv:str = versions[i] # Pull the exclusion version
                result_out_str:str = ','.join(result_output)
                # We may have not found any compatible versions, maybe theres only `!=` comparator entries
                if len(result_out_str) == 0:
                    result_output.append(f"!=:{nv}")
                    continue
                # Check if the exclusion version is in the current combined search result, if so, include it
                if len(version_locator(result_out_str,[nv])) > 0:
                    result_output.append(f"!=:{nv}")
    if len(result_output) == 0:
        raise ValueError(f"Unable to construct a search string which satisfies given search: '{search_a},{search_b}'")
    result:str = ','.join(result_output)
    return result


# mypy linting is disabled for this file because the unions dont play with bytes and other various things
# changes to this file should still make a best effort to be lint free.
# mypy: ignore-errors
class Version:
    """Version Breakdown Class
    A Version can be created from:
     - Semantic String ("1.0.0")
     - List of Strings or Ints of a version (["1","0","0"] or [1,0,0])
     - Tuple of Strings or Ints of a version (("1","0","0") or (1,0,0))

    Versions are comparable (>,<,>=,<=,==,!=)
    Versions are addable and subtractable (a -= b, a += b)
     - If a part goes negative, it will be set to 0

    @throws ValueError Mixed type add/subtract (str and int attempted to be added/subtracted)
    @throws TypeError Comparing Version to NoneType
    """

    parts:list[typing.Union[str,int]]

    @property
    def empty(self) -> bool:
        """Empty/None Set Version Check
        @retval bool Whether Version.parts is defined
        """
        return not hasattr(self,"parts")

    def __init__(self,version:typing.Union[
        str,
        list[
            typing.Union[str,int]
        ],
        tuple[
            typing.Union[str,int],
            ...
        ],
        None
    ]) -> None:
        if version is None:
            return
        self.parts = []
        if isinstance(version,str):
            version = version.split('.')
        elif isinstance(version,tuple):
            version = list(version)
        if version is None:
            return
        for i in range(0,len(version)):
            try:
                version[i] = int(version[i])
            except BaseException:
                version[i] = str(version[i])
            self.parts.append(version[i])

    def __str__(self) -> str:
        if not hasattr(self,"parts"):
            raise ValueError("Cannot convert empty Version to string")
        parts:list[typing.Union[str,int]] = self.parts.copy()
        out:str = str(parts.pop(0))
        for p in parts:
            out += f".{str(p)}"
        return out

    def __iadd__(self,version: typing.Union[
        str,
        list[
            typing.Union[str,int]
        ],
        tuple[
            typing.Union[str,int],
            ...
        ],
        "Version",
        None
    ]) -> "Version":
        comp:"Version" = self.__to_version(version)
        r:range = self.__define_range(comp)
        for i in r:
            if isinstance(self.parts[i],int) and isinstance(comp.parts[i],int):
                self.parts[i] += comp.parts[i]
            elif isinstance(self.parts[i],str) and isinstance(comp.parts[i],str):
                self.parts[i] = comp.parts[i]
            else:
                raise ValueError("Cannot add mixed types")
        return self

    def __add__(self,version: typing.Union[
        str,
        list[
            typing.Union[str,int]
        ],
        tuple[
            typing.Union[str,int],
            ...
        ],
        "Version",
        None
    ]) -> "Version":
        out:"Version" = Version(self.__str__())
        out += version
        return out

    def __isub__(self,version: typing.Union[
        str,
        list[
            typing.Union[str,int]
        ],
        tuple[
            typing.Union[str,int],
            ...
        ],
        "Version",
        None
    ]) -> "Version":
        comp:"Version" = self.__to_version(version)
        r:range = self.__define_range(comp)
        for i in r:
            if isinstance(self.parts[i],int) and isinstance(comp.parts[i],int):
                self.parts[i] -= comp.parts[i]
                if self.parts[i] < 0:
                    self.parts[i] = 0
                    # s:int = i - 1
                    # up:bool = True
                    # while up:
                    #     self.parts[s] -= 1
                    #     if self.parts[s] >= 0:
                    #         up = False
                    #     elif self.parts[s] < 0:
                    #         self.parts[s] = 0
                    #     s -= 1
            elif isinstance(self.parts[i],str) and isinstance(comp.parts[i],str):
                self.parts[i] = comp.parts[i]
            else:
                raise ValueError("Cannot subtract mixed types")
        return self

    def __sub__(self,version: typing.Union[
        str,
        list[
            typing.Union[str,int]
        ],
        tuple[
            typing.Union[str,int],
            ...
        ],
        "Version",
        None
    ]) -> "Version":
        out:"Version" = Version(self.__str__())
        out -= version
        return out

    def __ge__(self,version: typing.Union[
        str,
        list[
            typing.Union[str,int]
        ],
        tuple[
            typing.Union[str,int],
            ...
        ],
        "Version",
        None
    ]) -> bool:
        comp:"Version" = self.__to_version(version)
        r:range = self.__define_range(comp)
        result:bool = True
        for i in r:
            s:bytes = b''
            c:bytes = b''
            if isinstance(self.parts[i],int):
                s = bytes(self.parts[i])
            elif isinstance(self.parts[i],str):
                s = bytes(self.parts[i],"utf-8")
            if isinstance(comp.parts[i],int):
                c = bytes(comp.parts[i])
            elif isinstance(comp.parts[i],str):
                c = bytes(comp.parts[i],"utf-8")
            result = result and s >= c
            if result:
                return True
        return result

    def __le__(self,version: typing.Union[
        str,
        list[
            typing.Union[str,int]
        ],
        tuple[
            typing.Union[str,int],
            ...
        ],
        "Version",
        None
    ]) -> bool:
        comp:"Version" = self.__to_version(version)
        r:range = self.__define_range(comp)
        result:bool = True
        for i in r:
            s:bytes = b''
            c:bytes = b''
            if isinstance(self.parts[i],int):
                s = bytes(self.parts[i])
            elif isinstance(self.parts[i],str):
                s = bytes(self.parts[i],"utf-8")
            if isinstance(comp.parts[i],int):
                c = bytes(comp.parts[i])
            elif isinstance(comp.parts[i],str):
                c = bytes(comp.parts[i],"utf-8")
            result = result and s <= c
            if result:
                return True
        return result

    def __gt__(self,version: typing.Union[
        str,
        list[
            typing.Union[str,int]
        ],
        tuple[
            typing.Union[str,int],
            ...
        ],
        "Version",
        None
    ]) -> bool:
        comp:"Version" = self.__to_version(version)
        r:range = self.__define_range(comp)
        result:bool = True
        for i in r:
            s:bytes = b''
            c:bytes = b''
            if isinstance(self.parts[i],int):
                s = bytes(self.parts[i])
            elif isinstance(self.parts[i],str):
                s = bytes(self.parts[i],"utf-8")
            if isinstance(comp.parts[i],int):
                c = bytes(comp.parts[i])
            elif isinstance(comp.parts[i],str):
                c = bytes(comp.parts[i],"utf-8")
            result = result and s > c
            if result:
                return True
        return False

    def __lt__(self,version: typing.Union[
        str,
        list[
            typing.Union[str,int]
        ],
        tuple[
            typing.Union[str,int],
            ...
        ],
        "Version",
        None
    ]) -> bool:
        comp:"Version" = self.__to_version(version)
        r:range = self.__define_range(comp)
        result:bool = True
        for i in r:
            s:bytes = b''
            c:bytes = b''
            if isinstance(self.parts[i],int):
                s = bytes(self.parts[i])
            elif isinstance(self.parts[i],str):
                s = bytes(self.parts[i],"utf-8")
            if isinstance(comp.parts[i],int):
                c = bytes(comp.parts[i])
            elif isinstance(comp.parts[i],str):
                c = bytes(comp.parts[i],"utf-8")
            result = result and s < c
            if result:
                return True
        return result

    def __eq__(self,version:object) -> bool:
        comp:"Version" = self.__to_version(version)
        r:range = self.__define_range(comp)
        result:bool = True
        for i in r:
            result = result and self.parts[i] == comp.parts[i]
        return result

    def __ne__(self,version:object) -> bool:
        comp:"Version" = self.__to_version(version)
        r:range = self.__define_range(comp)
        result:bool = True
        for i in r:
            result = self.parts[i] != comp.parts[i]
            if result:
                return True
        return False

    def __to_version(self,version:object) -> "Version":
        if version is None:
            raise TypeError("Cannot Convert NoneType to Version")
        if isinstance(version,type(self)):
            return version
        return Version(version)

    def __define_range(self,version:"Version") -> range:
        if not hasattr(self,"parts") or not hasattr(version,"parts"):
            raise ValueError("Cannot compare an empty Version")
        if len(self.parts) >= len(version.parts):
            r = range(0,len(version.parts))
        else:
            r = range(0,len(self.parts))
        return r
