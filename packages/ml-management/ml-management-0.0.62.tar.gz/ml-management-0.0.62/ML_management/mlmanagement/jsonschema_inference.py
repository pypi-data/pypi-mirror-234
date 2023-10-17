"""Module for automatic jsonschema inference."""
from copy import copy
from inspect import formatannotation, getfullargspec

from jsonschema import SchemaError
from jsonschema.validators import Draft4Validator
from ML_management.mlmanagement.jsonschema_exceptions import (
    DictKeysMustBeStrings,
    FunctionContainsVarArgs,
    FunctionContainsVarKwArgs,
    InvalidSchema,
    NoAnnotation,
    UnsupportedType,
)

JSON_SCHEMA_DRAFT = "http://json-schema.org/draft-04/schema#"


type_map = {
    "bool": {"type": "boolean"},
    "int": {"type": "integer"},
    "float": {"type": "number"},
    "str": {"type": "string"},
}


def __get_or_raise(type_name):
    if type_name in type_map:
        return copy(type_map[type_name])
    else:
        raise UnsupportedType(annotation=type_name, supported_types=list(type_map.keys()))


def __is_optional(annotation):
    repr_annotation = repr(annotation)
    if repr_annotation.startswith("typing.Optional"):
        return True
    elif repr_annotation.startswith("typing.Union") and repr_annotation.strip("]").endswith("NoneType"):
        # python 3.8 casts Optional to Union[arg, None]
        return True
    else:
        return False


def __get_json_schema_from_annotation(annotation):
    if annotation.__module__ == "typing":
        if __is_optional(annotation):
            return __get_json_schema_from_annotation(
                annotation.__args__[0]
            )  # Optional[int] translates to int, and the field is not required
        else:
            formatted_annotation = formatannotation(annotation)
            annotation_name = formatted_annotation.partition("[")[0]  # this is the only way to reliably get annotation name (e.g. "List")
            if annotation_name == "List":
                return {
                    "type": "array",
                    "items": __get_json_schema_from_annotation(annotation.__args__[0]),
                }
            elif annotation_name == "Dict":
                key_annotation = annotation.__args__[0]
                if hasattr(key_annotation, "__name__"):
                    if key_annotation.__name__ != "str":
                        raise DictKeysMustBeStrings(annotation=formatted_annotation)
                else:
                    raise DictKeysMustBeStrings(annotation=formatted_annotation)
                return {
                    "type": "object",
                    "additionalProperties": __get_json_schema_from_annotation(annotation.__args__[1]),
                }
            elif annotation_name == "Union":
                # Union might represent Optional, in this case it would
                return {"anyOf": [__get_json_schema_from_annotation(ann) for ann in annotation.__args__]}
            else:
                raise UnsupportedType(
                    annotation=formatannotation(annotation),
                    supported_types=list(type_map.keys()),
                )

    elif annotation.__module__ == "builtins":
        if hasattr(annotation, "__name__"):
            return __get_or_raise(annotation.__name__)
    else:
        raise UnsupportedType(
            annotation=formatannotation(annotation),
            supported_types=list(type_map.keys()),
        )


def infer_jsonschema(func):
    """Infer jsonschema from callable by its signature."""
    spec = getfullargspec(func)

    # FullArgSpec(args, varargs, varkw, defaults, kwonlyargs, kwonlydefaults, annotations)
    pos_args_defaults = {}
    if spec.defaults:
        for arg, default in zip(spec.args[-len(spec.defaults) :], spec.defaults):
            pos_args_defaults[arg] = default
    if spec.varargs:
        raise FunctionContainsVarArgs(function_name=func.__name__)
    if spec.varkw:
        raise FunctionContainsVarKwArgs(function_name=func.__name__)
    schema = {
        "$schema": JSON_SCHEMA_DRAFT,
        "type": "object",
        "properties": {},
        "additionalProperties": False,
    }
    # annotations are not inferred from default yet, but i can do it myself from kwonlydefaults
    pos_args = spec.args if spec.args else []
    kw_only_args = spec.kwonlyargs if spec.kwonlyargs else []
    all_args = pos_args + kw_only_args
    kw_only_args_defaults = spec.kwonlydefaults if spec.kwonlydefaults else {}
    all_defaults = {**pos_args_defaults, **kw_only_args_defaults}

    if "self" in all_args:
        all_args.remove("self")
    required = []
    for arg in all_args:
        if arg not in spec.annotations:
            raise NoAnnotation(arg=arg)

        schema["properties"][arg] = __get_json_schema_from_annotation(spec.annotations[arg])
        if arg in all_defaults:
            schema["properties"][arg]["default"] = all_defaults[arg]
        if arg not in all_defaults and not __is_optional(spec.annotations[arg]):
            required.append(arg)

    if required:
        schema["required"] = required
    try:
        Draft4Validator.check_schema(schema)
    except SchemaError as err:
        raise InvalidSchema(schema=schema, original_message=str(err))

    return schema
