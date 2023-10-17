import json
import os
import sys
from typing import List, Any, Callable, Dict, Set, Optional
from enum import Enum
from dataclasses import dataclass, field
import yaml

from pytconf.color_utils import (
    print_highlight,
    color_hi,
    print_title,
    color_ok,
    color_warn,
    print_error,
)
from pytconf.errors_collector import ErrorsCollector
from pytconf.param_collector import the_collector
from pytconf.pydoc import get_first_line
from pytconf.registry import the_registry
from pytconf.utils import noun, HtmlGen

DEFAULT_FUNCTION_GROUP_NAME = "default"
DEFAULT_FUNCTION_GROUP_DESCRIPTION = "default command group"
DEFAULT_FUNCTION_GROUP_SHOW_META = False
DEFAULT_FUNCTION_GROUP_SHOW = True

SPECIAL_FUNCTION_GROUP_NAME = "special"
SPECIAL_FUNCTION_GROUP_DESCRIPTION = "special command group"
SPECIAL_FUNCTION_GROUP_SHOW_META = False
SPECIAL_FUNCTION_GROUP_SHOW = False

DEFAULT_FUNCTION_DESCRIPTION = "No function description available"


class ConfigType(Enum):
    USER = 1
    SYSTEM = 2


class ConfigFormat(Enum):
    JSON = 1
    YAML = 2


class MetaConfig(type):
    def __new__(cls, name, bases, namespace):
        ret = super().__new__(cls, name, bases, namespace)
        i = 0
        for k, v in namespace.items():
            if not k.startswith("__") and not isinstance(v, classmethod):
                the_registry.register(ret, k, the_collector.get_item(i))
                i += 1
        the_collector.clear()
        return ret


class Config(metaclass=MetaConfig):
    pass


def is_help(string: str) -> bool:
    return string.lower()[:4] == "help"


@dataclass
class FunctionData:
    name: str
    description: str
    function: Callable
    configs: List[Config] = field(default_factory=list)
    suggest_configs: List[Config] = field(default_factory=list)
    allow_free_args: bool = False
    min_free_args: Optional[int] = None
    max_free_args: Optional[int] = None
    group: str = DEFAULT_FUNCTION_GROUP_NAME


@dataclass
class FunctionGroupData:
    name: str
    description: str
    show_meta: bool = False
    show: bool = False
    names: Set[str] = field(default_factory=set)
    list_names: List[str] = field(default_factory=list)


class PytconfConf:
    def __init__(self):
        self.main_function: Optional[Callable] = None
        self.main_description: str = "No application description"

        self.functions: Dict[str, FunctionData] = {}
        self.groups: Dict[str, FunctionGroupData] = {}

        self.free_args: List[str] = []
        self.app_name: str = "No application name"
        self.version: str = "No version"
        self.default_function = None

        self.register_defaults()

    def register_main(
        self,
        main_function: Callable,
        main_description: str,
        app_name: str,
        version: str,
    ):
        self.main_function = main_function
        self.main_description = main_description
        self.app_name = app_name
        self.version = version

    def has_function(
        self,
        function_name: str,
    ) -> bool:
        return function_name in self.functions

    def register_function(self, data: FunctionData):
        self.functions[data.name] = data
        self.groups[data.group].names.add(data.name)

    @classmethod
    def print_errors(cls, errors: ErrorsCollector) -> None:
        for error in errors.yield_errors():
            print_error(error)

    def show_help(self) -> None:
        print(f"Usage: {color_hi(self.app_name)} COMMAND [ARGS]...")
        space = " " * 2
        print_highlight(f"\n{space}{self.main_description}\n")
        for name, group in self.groups.items():
            if not group.show:
                continue
            if group.show_meta:
                print(f"{space}{group.name}: {group.description}")
                cmd_space = space + " " * 2
            else:
                cmd_space = space
            for name in sorted(group.names):
                data = self.functions[name]
                print(f"{cmd_space}{color_hi(name)}: {data.description}")
            print()

    def show_help_for_function(
        self,
        name: str,
        show_help_full: bool = False,
        show_help_suggest: bool = False,
    ) -> None:
        print(f"Usage: {self.app_name} {name} [OPTIONS] [ARGS]...")
        data = self.functions[name]
        print_highlight(f"\n  {data.description}")
        print("\nOptions:\n")
        for config in data.configs:
            self.show_help_for_config(config)
        if show_help_suggest:
            for config in data.suggest_configs:
                self.show_help_for_config(config)
        if show_help_full:
            for config in the_registry.yield_configs():
                self.show_help_for_config(config)

    @classmethod
    def show_help_for_config(cls, config):
        if config == Config:
            return
        doc = get_first_line(config, "Undocumented parameter set")
        print_title(f"  {doc}")
        for name, param in the_registry.yield_name_data_for_config(config):
            if param.required:
                default = color_warn("MANDATORY")
            else:
                default = color_ok(param.t2s(param.default))
            print(f"    {color_hi(name)} [{param.get_type_name()}]: {param.help_string} [{default}]")
            more_help = param.more_help()
            if more_help is not None:
                print(f"      {more_help}")
        print()

    def process_flags(
        self, select: FunctionData, flags: Dict[str, str], errors: ErrorsCollector,
    ) -> None:
        # set the flags into the "default" field and collect unknown flags
        unknown_flags = []
        for flag_raw, value in flags.items():
            if not the_registry.has_name(flag_raw):
                if is_help(flag_raw):
                    errors.set_do_help()
                    errors.unset_show_errors()
                else:
                    unknown_flags.append(flag_raw)
                continue
            config = the_registry.get_config_for_name(flag_raw)
            param = the_registry.get_data_for_name(flag_raw)
            edit = value.startswith("=")
            # noinspection PyBroadException
            # pylint: disable=broad-except
            try:
                if edit:
                    v = param.s2t_generate_from_default(value[1:])
                else:
                    v = param.s2t(value)
                setattr(config, flag_raw, v)
            except Exception:
                errors.add_error(f"could not convert [{flag_raw}]")
        if unknown_flags:
            errors.add_error(f"unknown flags [{','.join(unknown_flags)}]")

        # check for missing parameters
        missing_parameters = []
        for config in select.configs:
            for name, param in the_registry.yield_name_data_for_config(config):
                if param.required and name not in flags:
                    missing_parameters.append(name)
        if missing_parameters:
            errors.add_error(
                f"missing {noun('parameter', len(missing_parameters))} [{','.join(missing_parameters)}]"
            )

    @staticmethod
    def read_flags_from_config(
        app_name: str,
        config_type: ConfigType,
        config_format: ConfigFormat,
        flags: Dict[str, str],
    ) -> None:
        file_name: str = PytconfConf.get_config(app_name, config_type, config_format)
        if os.path.isfile(file_name):
            with open(file_name, "rt") as json_file:
                new_flags: Dict[str, str]
                if config_format == ConfigFormat.JSON:
                    new_flags = json.load(json_file)
                if config_format == ConfigFormat.YAML:
                    new_flags = yaml.safe_load(json_file)
                assert isinstance(flags, dict)
            for k, v in new_flags.items():
                flags[k] = v

    @staticmethod
    def get_config(app_name: str, config_type: ConfigType, config_format: ConfigFormat):
        if config_format == ConfigFormat.JSON:
            suffix = "json"
        if config_format == ConfigFormat.YAML:
            suffix = "yaml"
        if config_type == ConfigType.USER:
            return os.path.expanduser(f"~/.config/{app_name}.{suffix}")
        return f"/etc/{app_name}.{suffix}"

    def register_function_group(
        self,
        data: FunctionGroupData,
    ):
        self.groups[data.name] = data

    def register_defaults(self):
        data = FunctionGroupData(
            name=DEFAULT_FUNCTION_GROUP_NAME,
            description=DEFAULT_FUNCTION_GROUP_DESCRIPTION,
            show_meta=DEFAULT_FUNCTION_GROUP_SHOW_META,
            show=DEFAULT_FUNCTION_GROUP_SHOW,
        )
        self.register_function_group(data)
        data = FunctionGroupData(
            name=SPECIAL_FUNCTION_GROUP_NAME,
            description=SPECIAL_FUNCTION_GROUP_DESCRIPTION,
            show_meta=SPECIAL_FUNCTION_GROUP_SHOW_META,
            show=SPECIAL_FUNCTION_GROUP_SHOW,
        )
        self.register_function_group(data)

        def do_help():
            if self.free_args:
                for arg in self.free_args:
                    if self.has_function(arg):
                        self.show_help_for_function(name=arg)
                    else:
                        print(f"have no function called [{arg}]")
                        sys.exit(1)
            else:
                self.show_help()
        data = FunctionData(
            function=do_help,
            name="help",
            description="show help",
            allow_free_args=True,
            max_free_args=2,
            group=SPECIAL_FUNCTION_GROUP_NAME,
        )
        self.register_function(data)

    def get_function_selected(self, args: List[str], errors) -> Optional[FunctionData]:
        function_selected = None
        if len(args) > 0:
            command = args.pop(0)
            if command in self.functions:
                function_selected = self.functions[command]
            else:
                if is_help(command):
                    errors.set_do_help()
                    errors.unset_show_errors()
                else:
                    errors.add_error(f"unknown command [{command}]")
                    errors.set_force_show_errors()
        return function_selected

    def config_arg_parse_and_launch(
        self,
        args: Optional[List[str]] = None,
        launch=True,
        do_exit=True,
    ) -> None:

        if args is None:
            args = sys.argv[1:]

        flags: Dict[str, str] = {}
        errors = ErrorsCollector()
        self.free_args = []

        # read config files
        self.read_flags_from_config(self.app_name, ConfigType.SYSTEM, ConfigFormat.JSON, flags=flags)
        self.read_flags_from_config(self.app_name, ConfigType.SYSTEM, ConfigFormat.YAML, flags=flags)
        self.read_flags_from_config(self.app_name, ConfigType.USER, ConfigFormat.JSON, flags=flags)
        self.read_flags_from_config(self.app_name, ConfigType.USER, ConfigFormat.YAML, flags=flags)

        select = self.get_function_selected(args, errors)

        # now parse the args
        self.parse_args(args, errors, flags)

        # if we have command we can check free args errors
        if select is not None:
            if select.allow_free_args:
                if select.min_free_args is not None:
                    if len(self.free_args) < select.min_free_args:
                        errors.add_error(f"too few free args - {select.min_free_args} required")
                if select.max_free_args is not None:
                    if len(self.free_args) >= select.max_free_args:
                        errors.add_error(f"too many free args - {select.max_free_args} required")
            else:
                if len(self.free_args) > 0:
                    if len(self.free_args) == 1 and is_help(self.free_args[0]):
                        errors.set_do_help()
                        errors.unset_show_errors()
                    else:
                        errors.add_error(f"free args are not allowed [{','.join(self.free_args)}]")
            self.process_flags(select, flags, errors)
        else:
            errors.add_error("no command is selected")
            errors.set_do_help()
            errors.unset_show_errors()

        if errors.have_errors() or errors.get_do_help():
            if errors.get_show_errors():
                self.print_errors(errors)
            if errors.get_do_help():
                if select:
                    self.show_help_for_function(select.name)
                else:
                    self.show_help()
            if do_exit:
                sys.exit(1)
            return

        self.launch(launch, select, errors)

    def launch(self, launch: bool, select: Optional[FunctionData], errors):
        if launch:
            if select is None:
                errors.add_error("no function to launch")
                errors.set_do_help()
            else:
                select.function()

    def parse_args(self, args, errors, flags):
        free_args_started = False
        while args:
            current = args.pop(0)
            if current.startswith("--") and not free_args_started:
                real = current[2:]
                number_of_equals = real.count("=")
                if number_of_equals == 1:
                    flag_name, flag_value = real.split("=")
                    flags[flag_name] = flag_value
                elif number_of_equals == 0:
                    if args:
                        more = args.pop(0)
                        flags[real] = more
                    else:
                        errors.add_error(
                            f"argument [{real}] needs a follow-up argument"
                        )
                else:
                    errors.add_error(f"can not parse argument [{real}]")
            else:
                self.free_args.append(current)
                free_args_started = True

    def get_html(self) -> str:
        html_gen = HtmlGen()
        main_doc = self.main_description
        html_gen.line("h1", main_doc)
        html_gen.line("h2", "API specifications")
        single_group = len(self.groups) == 1
        with html_gen.tag("ul"):
            for name, group in self.groups.items():
                if not single_group:
                    html_gen.line("li", group.name, title="function group name: ")
                    html_gen.line(
                        "li",
                        group.description,
                        title="function group description: ",
                    )
                with html_gen.tag("li"):
                    for name in sorted(self.functions.keys()):
                        self.get_html_for_function(name, html_gen)
        # return html_gen.document.getvalue()
        return html_gen.document  # type: ignore

    def get_html_for_function(self, name:str, html_gen):
        data = self.functions[name]
        with html_gen.tag("ul"):
            function_doc = get_first_line(data.function, "no description for this function")
            html_gen.line("li", name, title="function name: ")
            html_gen.line("li", function_doc, title="function description: ")
            with html_gen.tag("li"):
                with html_gen.tag("ul"):
                    for config in data.configs:
                        with html_gen.tag("li"):
                            self.get_html_for_config(config, html_gen)

    @classmethod
    def get_html_for_config(cls, config, html_gen):
        if config == Config:
            return
        doc = get_first_line(config, "undocumented config")
        html_gen.line("h3", doc, title="config: ")
        with html_gen.tag("table"):
            for name, param in the_registry.yield_name_data_for_config(config):
                with html_gen.tag("tr"):
                    if param.required:
                        default = "MANDATORY"
                    else:
                        default = param.t2s(param.default)
                    if param.more_help() is None:
                        more_help = "No more help is documented"
                    else:
                        more_help = param.more_help()
                    html_gen.line("td", name)
                    html_gen.line("td", param.help_string)
                    html_gen.line("td", param.get_type_name())
                    html_gen.line("td", default)
                    html_gen.line("td", more_help)

    @classmethod
    def rm_config_file(cls, app_name: str, config_type: ConfigType, config_format: ConfigFormat) -> None:
        filename = cls.get_config(app_name, config_type, config_format)
        if os.path.isfile(filename):
            os.unlink(filename)

    @classmethod
    def write_config_file(cls, filename: str, config_format: ConfigFormat) -> None:
        values: Dict[str, str] = {}
        for config in the_registry.yield_configs():
            for name, param in the_registry.yield_name_data_for_config(config):
                values[name] = param.t2s(param.default)
        with open(filename, "wt") as f:
            if config_format == ConfigFormat.JSON:
                json.dump(values, f, indent=4)
            if config_format == ConfigFormat.YAML:
                yaml.dump(values, f, indent=4)

    def write_config(self, config_type: ConfigType, config_format: ConfigFormat) -> None:
        filename = PytconfConf.get_config(self.app_name, config_type, config_format)
        self.write_config_file(filename, config_format)


_pytconf = PytconfConf()


def get_pytconf():
    return _pytconf


def config_arg_parse_and_launch(
    args=None,
    launch=True,
    do_exit=True,
) -> None:
    get_pytconf().config_arg_parse_and_launch(
        args=args,
        launch=launch,
        do_exit=do_exit,
    )


def get_free_args() -> List[str]:
    return get_pytconf().free_args


def register_function_group(
    name: str,
    description: str,
    show_meta: bool,
    show: bool,
) -> None:
    data = FunctionGroupData(
        name=name,
        description=description,
        show_meta=show_meta,
        show=show,
    )
    get_pytconf().register_function_group(data)


def register_main(
    main_description: str,
    app_name: str,
    version: str,
) -> Callable[[Any], Any]:
    def identity(main_function):
        get_pytconf().register_main(
            main_function=main_function,
            main_description=main_description,
            app_name=app_name,
            version=version,
        )
        return main_function

    return identity


def register_endpoint(
    description: str,
    name: Optional[str] = None,
    configs: Optional[List[Config]] = None,
    suggest_configs: Optional[List[Config]] = None,
    group: str = DEFAULT_FUNCTION_GROUP_NAME,
    allow_free_args: bool = False,
    min_free_args: Optional[int] = None,
    max_free_args: Optional[int] = None,
) -> Callable[[Any], Any]:
    if configs is None:
        configs = []
    if suggest_configs is None:
        suggest_configs = []

    def identity(function):
        if name is None:
            function_name = function.__name__
        else:
            function_name = name
        data = FunctionData(
            name=function_name,
            configs=configs,
            suggest_configs=suggest_configs,
            description=description,
            allow_free_args=allow_free_args,
            min_free_args=min_free_args,
            max_free_args=max_free_args,
            group=group,
            function=function,
        )
        get_pytconf().register_function(data=data)
        return function

    return identity
