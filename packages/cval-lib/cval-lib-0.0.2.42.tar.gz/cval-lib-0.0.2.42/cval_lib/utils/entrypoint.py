import inspect
from dataclasses import dataclass
from typing import Iterable, Optional, Any

from pydantic import BaseModel


class Entrypoint:
    __not_exposed__ = (
        '_',
        'close',
        'monkey_patch',
        'register_hook',
        'send',
    )

    @dataclass()
    class Endpoint:
        __slots__ = (
            'kwargs',
            'kwargs_not_defaults',
            'request_model',
            'func',
            'name',
            'base',
        )
        kwargs: Iterable
        kwargs_not_defaults: Iterable
        request_model: Optional[BaseModel]
        func: callable
        name: str
        base: object

    @classmethod
    def _get_methods(cls, obj) -> tuple[Endpoint | Any, ...]:
        methods = []
        for name, func in filter(
                lambda x: not any(map(lambda y: x[0].startswith(y), cls.__not_exposed__)),
                inspect.getmembers(obj, inspect.isfunction),
        ):
            _signature_not_defaults = signature_not_defaults(func)
            _signature = signature(func)
            an = dict(func.__annotations__)
            _cls = an.get('return')
            if _cls:
                del an['return']
            _request_model = tuple(filter(lambda x: hasattr(x[1], 'parse_obj'), an.items()))
            methods.append(
                cls.Endpoint(
                    base=obj,
                    func=func,
                    request_model=_request_model[0] if _request_model else None.__class__,
                    kwargs=_signature,
                    kwargs_not_defaults=_signature_not_defaults,
                    name=name,
                )
            )
            if _cls:
                methods.extend(cls._get_methods(_cls))
        return tuple(methods)


class Conflict(ValueError):
    pass


def signature_not_defaults(_func: callable):
    return tuple(
        k for k, v in inspect.signature(_func).parameters.items() if v.default == inspect._empty and k != 'self'
    )[1:]


def signature(_func: callable):
    return tuple(k for k, v in inspect.signature(_func).parameters.items() if k != 'self')
