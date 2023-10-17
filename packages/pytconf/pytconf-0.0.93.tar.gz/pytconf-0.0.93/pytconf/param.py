import abc
from enum import Enum
from typing import List, Union, Callable, Any, Optional

from pytconf.enum_subset import EnumSubset

from pytconf.extended_enum import str_to_enum_value, enum_type_to_list_str

from pytconf.convert import convert_str_to_str, convert_str_to_int, convert_int_to_str, convert_str_to_int_default, \
    convert_str_to_list_int, convert_list_int_to_str, convert_str_to_list_str, convert_list_str_to_str, \
    convert_str_to_int_or_none, convert_int_or_none_to_str, convert_str_to_str_or_none, convert_str_or_none_to_str, \
    convert_str_to_bool, convert_bool_to_str
from pytconf.param_collector import the_collector

NO_HELP = "No help for this configuration option"


class Unique:
    pass


NO_DEFAULT = Unique()


class Param(abc.ABC):
    """
    Parent class of all parameters of configuration
    """

    def __init__(
        self,
        help_string=NO_HELP,
        default: Any = NO_DEFAULT,
        type_name: Optional[str] = None,
    ):
        super().__init__()
        self.help_string = help_string
        self.required = default is NO_DEFAULT
        self.default = default
        self.type_name = type_name

    def get_type_name(self):
        return self.type_name

    def collect(self):
        the_collector.add_data(self)

    @abc.abstractmethod
    def s2t(self, s: str) -> object:
        pass

    def s2t_generate_from_default(self, s: str) -> object:
        raise ValueError("we do not support generation from default")

    @abc.abstractmethod
    def t2s(self, t: object) -> str:
        pass

    def more_help(self) -> Optional[str]:
        return None


class ParamFunctions(Param):
    """
    Parent class of all parameters of configuration
    """

    def __init__(
        self,
        function_s2t: Callable,
        function_s2t_generate_from_default: Callable,
        function_t2s: Callable,
        help_string=NO_HELP,
        default=None,
        type_name=None,
    ):
        super().__init__(
            help_string=help_string,
            default=default,
            type_name=type_name,
        )
        self.function_s2t = function_s2t
        self.function_t2s = function_t2s
        self.function_s2t_generate_from_default = function_s2t_generate_from_default
        super().collect()

    def s2t(self, s: str) -> Any:
        return self.function_s2t(s)

    def s2t_generate_from_default(self, s: str) -> Any:
        return self.function_s2t_generate_from_default(self.default, s)

    def t2s(self, t: Any) -> str:
        return self.function_t2s(t)


class ParamFilename(Param):
    def __init__(
        self,
        help_string: str = NO_HELP,
        default: Union[Unique, str] = NO_DEFAULT,
        type_name=None,
        suffixes: Optional[List[str]] = None,
    ):
        super().__init__(
            help_string=help_string,
            default=default,
            type_name=type_name,
        )
        self.suffixes = suffixes
        super().collect()

    def s2t(self, s):
        if self.suffixes is not None:
            assert any(
                s.endswith(x) for x in self.suffixes
            ), "filename suffix is not accepted"
        return s

    def t2s(self, t):
        return t

    def more_help(self):
        if self.suffixes is None:
            return "no limitation on suffixes"
        return f"allowed suffixes are {self.suffixes}"


class ParamEnum(Param):
    def __init__(
        self,
        enum_type: Enum,
        help_string=NO_HELP,
        default: Any = NO_DEFAULT,
    ):
        super().__init__(
            help_string=help_string,
            default=default,
            type_name="enum",
        )
        self.enum_type = enum_type
        super().collect()

    def get_type_name(self):
        return f"Enum[{self.enum_type.__name__}]"

    def s2t(self, s: str) -> Any:
        return str_to_enum_value(s, self.enum_type)

    def t2s(self, t: Any) -> str:
        return t.name

    def more_help(self):
        return f"allowed values {enum_type_to_list_str(self.enum_type)}"


class ParamEnumSubset(Param):
    def __init__(
        self,
        help_string=NO_HELP,
        default: Any = NO_DEFAULT,
        enum_type: Optional[Enum] = None,
    ):
        super().__init__(
            help_string=help_string,
            default=default,
            type_name="enum",
        )
        self.enum_type = enum_type
        super().collect()

    def get_type_name(self):
        # pylint: disable=protected-access
        return f"EnumSubset[{self.enum_type._name_}]"  # type: ignore

    def s2t(self, s: str) -> EnumSubset:
        return EnumSubset.from_string(e=self.enum_type, s=s)

    def t2s(self, t: Any) -> str:
        return t.to_string()  # type: ignore

    def s2t_generate_from_default(self, s: str) -> Optional[EnumSubset]:
        return None

    def more_help(self):
        return f"allowed values {enum_type_to_list_str(self.enum_type)}"  # type: ignore


class ParamChoice(Param):
    def __init__(
        self,
        help_string=NO_HELP,
        default: Union[str, Unique] = NO_DEFAULT,
        choice_list: Optional[List[str]] = None
    ):
        super().__init__(
            help_string=help_string,
            default=default,
            type_name="Choice",
        )
        self.choice_list = choice_list
        super().collect()

    def s2t(self, s: str) -> Any:
        return s

    def t2s(self, t: Any) -> str:
        return t

    def more_help(self):
        return f"allowed values {','.join(self.choice_list)}"  # type: ignore


class ParamCreator:
    """
    Static namespace with all the param creation functions.
    """

    @staticmethod
    def create_int(
        help_string: str = NO_HELP,
        default: Union[int, Unique] = NO_DEFAULT,
    ) -> int:
        """
        Create an int parameter
        :param help_string:
        :param default:
        :return:
        """
        ParamFunctions(
            help_string=help_string,
            default=default,
            type_name="int",
            function_s2t=convert_str_to_int,
            function_t2s=convert_int_to_str,
            function_s2t_generate_from_default=convert_str_to_int_default,
        )
        return default  # type: ignore

    @staticmethod
    def create_list_int(
        help_string: str = NO_HELP,
        # This is because of pylint
        # default: List[int] = NO_DEFAULT,
        # pylint: disable=dangerous-default-value
        default: List[int] = [],
    ) -> List[int]:
        """
        Create a List[int] parameter
        :param help_string:
        :param default:
        :return:
        """
        ParamFunctions(
            help_string=help_string,
            default=default,
            type_name="List[int]",
            function_s2t=convert_str_to_list_int,
            function_t2s=convert_list_int_to_str,
            function_s2t_generate_from_default=convert_str_to_list_int,
        )
        if default is NO_DEFAULT:
            return []
        return default

    @staticmethod
    def create_list_str(
        help_string: str = NO_HELP,
        # This is because of pylint
        # default: List[str] = NO_DEFAULT,
        # pylint: disable=dangerous-default-value
        default: List[str] = [],
    ) -> List[str]:
        """
        Create a List[str] parameter
        :param help_string:
        :param default:
        :return:
        """
        ParamFunctions(
            help_string=help_string,
            default=default,
            type_name="List[str]",
            function_s2t=convert_str_to_list_str,
            function_t2s=convert_list_str_to_str,
            function_s2t_generate_from_default=convert_str_to_list_str,
        )
        if default is NO_DEFAULT:
            return []
        return default

    @staticmethod
    def create_int_or_none(
        help_string: str = NO_HELP,
        default: Union[int, None, Unique] = NO_DEFAULT,
    ) -> Optional[int]:
        """
        Create an int parameter
        :param help_string:
        :param default:
        :return:
        """
        ParamFunctions(
            help_string=help_string,
            default=default,
            type_name="Optional[int]",
            function_s2t=convert_str_to_int_or_none,
            function_t2s=convert_int_or_none_to_str,
            function_s2t_generate_from_default=convert_str_to_int_or_none,
        )
        return default  # type: ignore

    @staticmethod
    def create_str(
        help_string: str = NO_HELP,
        default: Union[str, Unique] = NO_DEFAULT,
    ) -> str:
        """
        Create a string parameter
        :param help_string:
        :param default:
        :return:
        """
        ParamFunctions(
            help_string=help_string,
            default=default,
            type_name="str",
            function_s2t=convert_str_to_str,
            function_s2t_generate_from_default=convert_str_to_str,
            function_t2s=convert_str_to_str,
        )
        return default  # type: ignore

    @staticmethod
    def create_str_or_none(
        help_string: str = NO_HELP,
        default: Union[str, None, Unique] = NO_DEFAULT,
    ) -> Optional[str]:
        """
        Create a string parameter
        :param help_string:
        :param default:
        :return:
        """
        ParamFunctions(
            help_string=help_string,
            default=default,
            type_name="str_or_none",
            function_s2t=convert_str_to_str_or_none,
            function_s2t_generate_from_default=convert_str_to_str_or_none,
            function_t2s=convert_str_or_none_to_str,
        )
        return default  # type: ignore

    @staticmethod
    def create_bool(
        help_string: str = NO_HELP,
        default: Union[bool, Unique] = NO_DEFAULT,
    ) -> bool:
        """
        Create a bool parameter
        :param help_string:
        :param default:
        :return:
        """
        ParamFunctions(
            help_string=help_string,
            default=default,
            type_name="bool",
            function_s2t=convert_str_to_bool,
            function_s2t_generate_from_default=convert_str_to_bool,
            function_t2s=convert_bool_to_str,
        )
        if default is NO_DEFAULT:
            return False
        return bool(default)

    @staticmethod
    def create_new_file(
        help_string: str = NO_HELP,
        default: Union[str, Unique] = NO_DEFAULT,
        suffixes: Optional[List[str]] = None,
    ) -> str:
        """
        Create a new file parameter
        :param help_string:
        :param default:
        :param suffixes:
        :return:
        """
        ParamFilename(
            help_string=help_string,
            default=default,
            type_name="new_file",
            suffixes=suffixes,
        )
        return default  # type: ignore

    @staticmethod
    def create_existing_file(
        help_string: str = NO_HELP,
        default: Union[str, Unique] = NO_DEFAULT,
        suffixes: Optional[List[str]] = None,
    ) -> str:
        """
        Create a new file parameter
        :param help_string:
        :param default:
        :param suffixes:
        :return:
        """
        ParamFilename(
            help_string=help_string,
            default=default,
            type_name="existing_file",
            suffixes=suffixes,
        )
        return default  # type: ignore

    @staticmethod
    def create_existing_folder(
        help_string: str = NO_HELP,
        default: Union[str, Unique] = NO_DEFAULT,
        suffixes: Optional[List[str]] = None,
    ) -> str:
        """
        Create a new folder parameter
        :param help_string:
        :param default:
        :param suffixes:
        :return:
        """
        ParamFilename(
            help_string=help_string,
            default=default,
            type_name="existing_folder",
            suffixes=suffixes,
        )
        return default  # type: ignore

    @staticmethod
    def create_choice(
        choice_list: List[str],
        help_string: str = NO_HELP,
        default: Union[str, Unique] = NO_DEFAULT,
    ) -> str:
        """
        Create a choice config
        :param choice_list:
        :param help_string:
        :param default:
        :return:
        """
        ParamChoice(
            help_string=help_string,
            default=default,
            choice_list=choice_list,
        )
        return default  # type: ignore

    @staticmethod
    def create_enum(
        enum_type: Enum,
        help_string: str = NO_HELP,
        default: Union[Enum, Unique] = NO_DEFAULT,
    ) -> Enum:
        """
        Create an enum config
        :param enum_type:
        :param help_string:
        :param default:
        :return:
        """
        ParamEnum(
            help_string=help_string,
            default=default,
            enum_type=enum_type,
        )
        return default  # type: ignore

    @staticmethod
    def create_enum_subset(
        enum_type: Enum,
        help_string: str = NO_HELP,
        default: Union[EnumSubset, Unique] = NO_DEFAULT,
    ) -> EnumSubset:
        """
        Create an enum config
        :param enum_type:
        :param help_string:
        :param default:
        :return:
        """
        ParamEnumSubset(
            help_string=help_string,
            default=default,
            enum_type=enum_type,
        )
        return default  # type: ignore

    @staticmethod
    def create_existing_bucket(
        help_string: str = NO_HELP,
        default: Union[str, Unique] = NO_DEFAULT,
    ) -> str:
        """
        Create a bucket name on gcp
        :param help_string:
        :param default:
        :return:
        """
        ParamFunctions(
            help_string=help_string,
            default=default,
            type_name="bucket_name",
            function_s2t=convert_str_to_str,
            function_s2t_generate_from_default=convert_str_to_str,
            function_t2s=convert_str_to_str,
        )
        return default  # type: ignore
