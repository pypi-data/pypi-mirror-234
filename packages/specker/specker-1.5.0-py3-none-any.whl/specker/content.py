# Copyright 2023-2023 by AccidentallyTheCable <cableninja@cableninja.net>.
# All rights reserved.
# This file is part of Specker JSON Specification Validator,
# and is released under "GPLv3". Please see the LICENSE
# file that should have been included as part of this package.
#### END COPYRIGHT BLOCK ###
from pathlib import Path
import re
import typing

class SpecContent:
    """Spec Content Container
    """

    _name:str
    _required:bool
    _default:typing.Any
    _type:str
    _comment:str
    _example:str
    _values:list[typing.Any]
    _format:str

    _spec_chain:str

    def get(self,attr:str) -> typing.Any:
        """Get a Parameter
        @param str \c attr Attribute to Get
        @retval Any Value of Attribute if it exists
        @throws AttributeError Cannot find Requested Attribute (or not set)
        """
        if not hasattr(self,f"_{attr}"):
            raise AttributeError(f"{self._name} does not have attribute '{attr}'")
        return getattr(self,f"_{attr}")

    __type_map:dict[str,typing.Type] = {
        "str": str,
        "int": int,
        "list": list,
        "dict": dict,
        "bool": bool,
        "any": typing.Any, # type: ignore
        "float": float,
        "path": Path,
        "file": Path,
        "dir": Path,
        "file:exist": Path,
        "dir:exist": Path,
        "path:exist": Path
    }

    @property
    def format(self) -> typing.Union[re.Pattern,None]:
        """Get Spec Regex Format
        @retval Union[re.Pattern,None] Regex Pattern if defined, otherwise, None
        """
        if not hasattr(self,"_format"):
            raise AttributeError(f"{self._name} does not have attribute 'format'")
        format:str = getattr(self,"_format")
        if len(format) > 0:
            return re.compile(format)
        return None

    @property
    def type(self) -> typing.Type:
        """Get Spec Value Type
        @retval type Type specified from Spec
        """
        if self._type not in self.__type_map.keys():
            raise TypeError(f"Unknown Type: {str(self._type)}")
        return self.__type_map[self._type]

    @staticmethod
    # pylint: disable=unused-argument
    def create(name:str,
               value_type:typing.Type,
               required:bool = False,
               default:typing.Union[typing.Any,None] = None,
               comment:typing.Union[str,None] = None,
               example:typing.Union[str,None] = None,
               values:typing.Union[list[str],None] = None,
               spec_chain:typing.Union[str,None] = None,
               format:typing.Union[str,None] = None
            ) -> "SpecContent":
        """Create New Spec Entry for loading into SpecLoader
        @param str \c name Key Name that will be validated
        @param Type \c value_type Type of Value to validate
        @param bool \c required Whether Key is required or not. Defaults to False.
        @param Union[Any,None] \c default Default Value. Defaults to None.
        @param Union[str,None] \c comment Item Comment / Description. Defaults to None.
        @param Union[str,None] \c example Item Example(s), Defaults to None.
        @param Union[list[str],None] \c values Valid Values for Item. Defaults to None.
        @param Union[str,None] \c spec_chain Name of Spec to Chain to. Defaults to None.
        @retval SpecContent New Spec Entry
        """
        config:dict[str,typing.Any] = locals()
        type_map:dict[typing.Type,str] = { v:k for k,v in SpecContent.__type_map.items() }
        config.pop("value_type")
        config["type"] = type_map[value_type]
        c:dict[str,typing.Any] = config.copy()
        for k,v in c.items():
            if v is None:
                config.pop(k)
        return SpecContent(config)
    # pylint: enable=unused-argument

    def __init__(self,content:dict[str,typing.Any]) -> None:
        """Initializer
        @param dict[str,typing.Any] \c content Spec Content
        """
        valid_attrs:list[str] = [ "required", "default", "comment", "example", "values", "spec_chain", "format" ]
        attr_defaults:list[typing.Any] = [  False, None, "", "", [], None, "" ]

        for k,v in content.items(): # Set Passed Attrs
            setattr(self,f"_{k}",v)

        for i in range(0,len(valid_attrs),1): # Set Default Attrs
            attr:str = valid_attrs[i]
            default:typing.Any = attr_defaults[i]
            if not hasattr(self,f"_{attr}"):
                setattr(self,f"_{attr}",default)

        if not hasattr(self,"_name"):
            raise ValueError("Spec is missing required attribute: name")
        if not hasattr(self,"_type"):
            raise ValueError("Spec is missing required attribute: type")
        if self._type not in self.__type_map.keys():
            raise TypeError(f"Spec has invalid type option. See Documentation for valid options for 'type', '{self._type} is not valid")

    def __str__(self) -> str:
        """To String Generator
        @retval str Markdown Formatted Data about Spec
        """
        default_str:str = ""
        if self._default is not None:
            default_str = f"\n - Default: {str(self._default)}"
        values_str:str = ""
        if len(self._values) > 0:
            values_str = f"\n - Acceptable Values: {', '.join(self._values)}"
        format_str:str = ""
        if len(self._format) > 0:
            format_str = f"\n - Acceptable Format: {self._format}"
        example_str:str = ""
        if len(self._example) > 0:
            example_str = f"\n - Example: {str(self._example)}"
        chain_str:str = ""
        if self._spec_chain is not None:
            chain_str = f"\n - Additionally Validates With: `{self._spec_chain}`"
        return f'''Option: `{self._name}` - {self._comment}
 - Type: {self._type}
 - Required: {str(self._required)}{default_str}{values_str}{format_str}{example_str}{chain_str}
'''
