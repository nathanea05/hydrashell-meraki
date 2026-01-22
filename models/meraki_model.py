from __future__ import annotations

from dataclasses import dataclass, fields, MISSING
from typing import Any, ClassVar, Dict, Mapping, Optional, Type, TypeVar, get_args, get_origin

T = TypeVar("T", bound="MerakiModel")


def camel_to_snake(name: str) -> str:
    out = []
    for i, ch in enumerate(name):
        if ch.isupper() and i != 0:
            out.append("_")
        out.append(ch.lower())
    return "".join(out)


def snake_to_camel(name: str) -> str:
    parts = name.split("_")
    return parts[0] + "".join(p[:1].upper() + p[1:] for p in parts[1:])


def is_optional_type(tp: Any) -> bool:
    # Optional[T] is Union[T, NoneType]
    origin = get_origin(tp)
    if origin is None:
        return False
    if origin is not type(Optional[str]):  # ignore; we’ll do generic union check
        pass
    if origin is list or origin is dict:
        return False
    if origin is type(Optional[str]):
        return True
    if origin is None:
        return False
    if origin is type(Optional[str]):
        return True
    if origin is getattr(__import__("typing"), "Union", None):
        return type(None) in get_args(tp)
    return False


def unwrap_optional(tp: Any) -> Any:
    if get_origin(tp) is getattr(__import__("typing"), "Union", None):
        args = [a for a in get_args(tp) if a is not type(None)]
        return args[0] if args else Any
    return tp


@dataclass
class MerakiModel:
    """
    Base class for Meraki resources.

    Default behavior:
      - For each dataclass field `foo_bar`, read JSON key `fooBar`
      - Unknown keys are ignored
      - Missing keys are allowed unless marked required

    Override behavior:
      - __field_map__: snake_case_field -> json_key (string) OR dotted path ("cloud.region.name")
      - __required_fields__: set of snake_case_field names required for from_dict()
    """

    __field_map__: ClassVar[Dict[str, str]] = {}
    __required_fields__: ClassVar[set[str]] = set()

    @classmethod
    def _json_key_for_field(cls, field_name: str) -> str:
        return cls.__field_map__.get(field_name, snake_to_camel(field_name))

    @classmethod
    def _get_value(cls, payload: Mapping[str, Any], key: str) -> Any:
        """
        Supports dotted paths in mapping overrides, e.g. "cloud.region.host.name".
        """
        if "." not in key:
            return payload.get(key, MISSING)

        cur: Any = payload
        for part in key.split("."):
            if not isinstance(cur, Mapping):
                return MISSING
            cur = cur.get(part, MISSING)
            if cur is MISSING:
                return MISSING
        return cur

    @classmethod
    def from_dict(cls: Type[T], payload: Mapping[str, Any]) -> T:
        if not isinstance(payload, Mapping):
            raise TypeError(f"{cls.__name__}.from_dict expected a mapping, got {type(payload)!r}")

        kwargs: Dict[str, Any] = {}

        for f in fields(cls):
            # Skip internal / classvar-like fields (dataclasses fields only include real instance fields)
            name = f.name
            json_key = cls._json_key_for_field(name)
            raw = cls._get_value(payload, json_key)

            required = (name in cls.__required_fields__)

            if raw is MISSING:
                # Missing field
                if required:
                    raise ValueError(f"Missing required field '{name}' (json key '{json_key}') for {cls.__name__}")

                # If dataclass provides a default/default_factory, skip and let dataclass fill it
                has_default = (f.default is not MISSING) or (f.default_factory is not MISSING)  # type: ignore
                if has_default:
                    continue

                # If Optional[T], set None; otherwise also set None (since you want required default=false)
                kwargs[name] = None
                continue

            # Present field: try to coerce nested MerakiModel if annotated
            tp = f.type
            opt = is_optional_type(tp)
            base_tp = unwrap_optional(tp) if opt else tp

            # Nested object
            if isinstance(base_tp, type) and issubclass(base_tp, MerakiModel) and isinstance(raw, Mapping):
                kwargs[name] = base_tp.from_dict(raw)
                continue

            # List of nested objects
            origin = get_origin(base_tp)
            if origin is list:
                (item_tp,) = get_args(base_tp) if get_args(base_tp) else (Any,)
                item_base = unwrap_optional(item_tp)
                if isinstance(item_base, type) and issubclass(item_base, MerakiModel) and isinstance(raw, list):
                    kwargs[name] = [
                        item_base.from_dict(x) if isinstance(x, Mapping) else x
                        for x in raw
                    ]
                    continue

            kwargs[name] = raw

        return cls(**kwargs)  # type: ignore[arg-type]