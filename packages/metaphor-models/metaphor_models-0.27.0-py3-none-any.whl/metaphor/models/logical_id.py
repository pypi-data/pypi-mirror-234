from dataclasses import dataclass
from typing import Optional, Any, TypeVar, Type, cast


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class PersonLogicalID:
    email: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'PersonLogicalID':
        assert isinstance(obj, dict)
        email = from_union([from_str, from_none], obj.get("email"))
        return PersonLogicalID(email)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.email is not None:
            result["email"] = from_union([from_str, from_none], self.email)
        return result


@dataclass
class LogicalID:
    person: Optional[PersonLogicalID] = None

    @staticmethod
    def from_dict(obj: Any) -> 'LogicalID':
        assert isinstance(obj, dict)
        person = from_union([PersonLogicalID.from_dict, from_none], obj.get("person"))
        return LogicalID(person)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.person is not None:
            result["person"] = from_union([lambda x: to_class(PersonLogicalID, x), from_none], self.person)
        return result


def logical_id_from_dict(s: Any) -> LogicalID:
    return LogicalID.from_dict(s)


def logical_id_to_dict(x: LogicalID) -> Any:
    return to_class(LogicalID, x)
