import inspect
import re
from dataclasses import dataclass
from typing import *  # type: ignore
from typing import Any

import revel

T = TypeVar("T")
P = ParamSpec("P")


NO_DEFAULT = object()


PATTERN_LONG_FLAG = re.compile(r"--([a-zA-Z0-9\-]+)(=(.*))?")
PATTERN_SHORT_FLAG = re.compile(r"-([a-zA-Z\-]+)(=(.*))?")


@dataclass(frozen=True)
class Parameter:
    name: str
    shorthand: Optional[str]
    type: Type

    is_flag: bool
    is_variadic: bool

    default_value: Any


def parameters_from_function(
    function: Callable,
) -> Iterable[Tuple[inspect.Parameter, Parameter]]:
    """
    Converts the given function's parameter list into a list of `Parameter`s.
    """
    signature = inspect.signature(function)
    type_hints = get_type_hints(function)

    for name, parameter in signature.parameters.items():
        param_type = type_hints.get(name, Any)

        # Parse the name. If it contains a double underscore, use it to split
        # the name into shorthand and name
        splits = name.split("__", maxsplit=1)

        if len(splits) == 1:
            shorthand = None
        else:
            shorthand, name = splits

            if len(shorthand) != 1:
                raise ValueError(
                    f"Shorthands must be exactly one character long, not `{shorthand}`"
                )

        # Default value?
        if parameter.default is inspect.Parameter.empty:
            default_value = NO_DEFAULT
        else:
            default_value = parameter.default

        # What kind of parameter is this?
        if parameter.kind == inspect.Parameter.VAR_POSITIONAL:
            is_variadic = True
            is_flag = False
        elif parameter.kind == inspect.Parameter.POSITIONAL_ONLY:
            is_variadic = False
            is_flag = False
        elif parameter.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD:
            is_variadic = False
            is_flag = False
        elif parameter.kind == inspect.Parameter.KEYWORD_ONLY:
            is_variadic = False
            is_flag = True
        elif parameter.kind == inspect.Parameter.VAR_KEYWORD:
            is_variadic = True
            is_flag = True
        else:
            raise NotImplementedError(f"Unsupported parameter kind: {parameter.kind}")

        # Build the result
        yield parameter, Parameter(
            name=name,
            shorthand=shorthand,
            type=param_type,
            is_flag=is_flag,
            is_variadic=is_variadic,
            default_value=default_value,
        )


def _parse_literal(raw: str, typ: Type) -> str:
    # TODO: Normalize?
    # Assign scores for each match?

    # Find all matches
    possible_values = get_args(typ)
    matches = []

    for possible_value in possible_values:
        # Exact match? This is it
        if raw == possible_value:
            return possible_value

        # Partial match? Keep it
        if raw in possible_value:
            matches.append(possible_value)

    # No matches? Error
    if not matches:
        possible_values_str = "`" + "`, `".join(possible_values) + "`"
        raise ValueError(
            f"`{raw}` is not a valid value for `{typ}`. Use one of: {possible_values_str}"
        )

    # Multiple matches? Ambiguous
    if len(matches) > 1:
        matches_str = "`" + "`, `".join(matches) + "`"
        raise ValueError(
            f"`{raw}` is ambiguous for `{typ}`. It could refer to either of: {matches_str}"
        )

    # Exactly one match? This is it
    return matches[0]


def _parse_bool(raw: str) -> bool:
    raw = raw.lower()

    if raw in ("true", "t", "yes", "y", "1"):
        return True

    if raw in ("false", "f", "no", "n", "0"):
        return False

    raise ValueError(f"`{raw}` is not a valid boolean value. Use `true` or `false`")


def _parse_int(raw: str) -> int:
    try:
        return int(raw)
    except ValueError:
        raise ValueError(f"`{raw}` is not a valid integer number")


def _parse_float(raw: str) -> float:
    try:
        return float(raw)
    except ValueError:
        raise ValueError(f"`{raw}` is not a valid number")


def parse_value(value: str, typ: Type) -> Any:
    type_key = get_origin(typ)
    if type_key is None:
        type_key = typ

    if type_key in (str, Any):
        return str(value)

    if type_key is Literal:
        return _parse_literal(value, typ)

    if type_key is bool:
        return _parse_bool(value)

    if type_key is int:
        return _parse_int(value)

    if type_key is float:
        return _parse_float(value)

    # TODO: Optional, Union?

    raise TypeError(f"`{typ}` is not a supported type")


class Parser:
    def __init__(self, parameters: Iterable[Parameter]):
        self.parameters = list(parameters)

        # All parameters, by their name, shorthand, and position
        self.parameters_by_name: Dict[str, Parameter] = {}
        self.parameters_by_shorthand: Dict[str, Parameter] = {}
        self.positional_parameters: List[Parameter] = []

        for parameter in self.parameters:
            # Positional or flag?
            if parameter.is_flag:
                self.parameters_by_name[parameter.name] = parameter

                if parameter.shorthand is not None:
                    self.parameters_by_shorthand[parameter.shorthand] = parameter
            else:
                self.positional_parameters.append(parameter)

        # Maps already assigned values to parameters
        self.assigned_parameters: Dict[str, List[str]] = {}

        # If not `None`, this is the parameter that is currently looking for a
        # value
        self.current_parameter: Optional[str] = None

        # Whether any more flags are allowed
        self.allow_flags = True

        # Any superfluous values which cannot be assigned to any parameter
        self.rest: List[str] = []

        # Any errors that occurred during parsing
        self.errors: List[str] = []

        # The index of the next positional parameter to assign a value to
        self.next_positional_parameter_index = 0

    def _feed_flags(
        self,
        flag_names: Iterable[str],
        flag_value: Optional[str],
        use_shorthands: bool,
    ) -> None:
        flag_names = list(flag_names)
        flag_by_name_dict = (
            self.parameters_by_shorthand if use_shorthands else self.parameters_by_name
        )

        assert len(flag_names) >= 1, flag_names
        assert (
            not self.current_parameter
        ), "Parsing a flag, while one is still looking for a value?"

        # If multiple short flags are specified in the same value, all but the
        # last one have to be booleans
        for bool_flag in flag_names[:-1]:
            try:
                parameter = flag_by_name_dict[bool_flag]
            except KeyError:
                is_bool_parameter = False
            else:
                is_bool_parameter = parameter.type is bool

            if not is_bool_parameter:
                self.errors.append(f"Missing value for `-{bool_flag}`")
            else:
                existing = self.assigned_parameters.setdefault(bool_flag, [])
                existing.append("true")

        # If a value was specified, use it
        last_flag = flag_names[-1]
        if flag_value is not None:
            existing = self.assigned_parameters.setdefault(last_flag, [])
            existing.append(flag_value)
            return

        # If this parameter is a boolean, the very existence of the flag
        # means it's `True`
        try:
            parameter = self.parameters_by_shorthand[last_flag]
        except KeyError:
            pass
        else:
            if parameter.type == bool:
                existing = self.assigned_parameters.setdefault(last_flag, [])
                existing.append("true")
                return

        # Otherwise, the next value is the value for this flag
        assert self.current_parameter is None, self.current_parameter
        self.current_parameter = last_flag
        return

    def feed_one(self, value: str) -> None:
        """
        Process a single value, updating the parser's state accordingly.
        """

        # If a parameter is still looking for a value, this is the value
        if self.current_parameter is not None:
            existing = self.assigned_parameters.setdefault(self.current_parameter, [])
            existing.append(value)
            self.current_parameter = None
            return

        # These only apply if flags are still accepted
        if self.allow_flags:
            # "--" marks the end of flags
            if value == "--":
                self.allow_flags = False
                return

            # Long flag?
            match = PATTERN_LONG_FLAG.fullmatch(value)
            if match is not None:
                self._feed_flags(
                    flag_names=[match.group(1)],
                    flag_value=match.group(3),
                    use_shorthands=False,
                )
                return

            # Short flag?
            match = PATTERN_SHORT_FLAG.fullmatch(value)
            if match is not None:
                self._feed_flags(
                    flag_names=list(match.group(1)),
                    flag_value=match.group(3),
                    use_shorthands=True,
                )
                return

        # Positional argument
        try:
            param = self.positional_parameters[self.next_positional_parameter_index]
        except IndexError:
            self.rest.append(value)
            return

        # Assign the value to the parameter
        existing = self.assigned_parameters.setdefault(param.name, [])
        existing.append(value)

        # If the parameter isn't variadic, move on to the next one
        if not param.is_variadic:
            self.next_positional_parameter_index += 1

    def feed_many(self, values: Iterable[str]) -> None:
        """
        Process multiple values, updating the parser's state accordingly.
        """

        for value in values:
            self.feed_one(value)

    def finish(self) -> Dict[Parameter, Any]:
        """
        Complete the parsing process and return the assigned values.
        """

        # Make sure no parameter is still looking for a value
        if self.current_parameter is not None:
            self.errors.append(f"Missing value for `{self.current_parameter}`")
            self.current_parameter = None

        # Parse the assigned values
        result = {}

        for param in self.parameters:
            # Has a value been assigned to this parameter?
            try:
                raw_assigned = self.assigned_parameters.pop(param.name)
            except KeyError:
                # Impute the default
                if param.default_value is not NO_DEFAULT:
                    result[param] = param.default_value
                    continue

                # No default, and no value assigned
                self.errors.append(f"Missing value for `{param.name}`")
                continue

            # Make sure the correct number of values has been assigned
            if not param.is_variadic and len(raw_assigned) > 1:
                self.errors.append(f"Too many values for `{param.name}`")
                continue

            # Parse the values
            values = []

            for raw_value in raw_assigned:
                try:
                    value = parse_value(raw_value, param.type)
                except ValueError as e:
                    self.errors.append(f"Invalid value for `{param.name}`: {e}")
                    continue

                values.append(value)

            # Assign the value(s)
            if param.is_variadic:
                result[param] = tuple(values)
            elif values:
                result[param] = values[0]

        # Make sure no superfluous values are left
        if self.assigned_parameters:
            for name, values in self.assigned_parameters.items():
                self.errors.append(f"Unexpected value `{values[0]}`")

        # Done
        return result


def call_function(
    func: Callable[P, T],
    raw_args: Iterable[str],
) -> T:
    # Create a parser
    python_param_to_revel_param: Dict[inspect.Parameter, Parameter] = dict(
        parameters_from_function(func)
    )
    parser = Parser(python_param_to_revel_param.values())

    # Assign the arguments
    parser.feed_many(raw_args)
    assignments = parser.finish()

    # Any errors?
    for err in parser.errors:
        revel.error(err)

    if parser.errors:
        raise ValueError("Invalid arguments")

    # Bring the parameters into a form usable to call the function
    by_position = []
    by_name = {}

    for python_param, revel_param in python_param_to_revel_param.items():
        value = assignments[revel_param]

        if python_param.kind == inspect.Parameter.KEYWORD_ONLY:
            by_name[python_param.name] = value
        else:
            by_position.append(value)

    # Call the function
    return func(*by_position, **by_name)   # type: ignore
