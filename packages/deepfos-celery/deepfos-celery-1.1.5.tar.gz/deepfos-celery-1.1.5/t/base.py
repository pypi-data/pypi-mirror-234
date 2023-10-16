import inspect
from collections import defaultdict

import pytest

from typing import *


EXCLUDED = defaultdict(set)


class _WrapMixin:
    @classmethod
    def _wrap_case(cls, case):
        raise NotImplementedError

    @classmethod
    def wrap_case(cls, case):
        if case in EXCLUDED.get(cls, ()):
            return case
        else:
            return cls._wrap_case(case)

    @classmethod
    def exclude(cls, func):
        EXCLUDED[cls].add(func)
        return func


class AsyncMixin(_WrapMixin):
    @classmethod
    def _wrap_case(cls, case):
        if not inspect.iscoroutinefunction(case):
            return case
        return pytest.mark.asyncio(case)


class FlakyMixin(_WrapMixin):
    reruns: int = 5
    resuns_delay: int = 2
    timeout: int = 300

    @classmethod
    def _wrap_case(cls, case):
        flaky = pytest.mark.flaky(
            reruns=cls.reruns,
            reruns_delay=cls.resuns_delay
        )
        timeout = pytest.mark.timeout(timeout=cls.timeout)
        return timeout(flaky(case))


class _AbsTestMeta(type):
    def __new__(mcs, name, bases, namespace: Dict[str, Any]):
        for attr, case in namespace.items():
            if attr.startswith('test'):
                namespace[attr] = mcs.wrap_cases(bases, case)

        return super().__new__(mcs, name, bases, namespace)

    @classmethod
    def wrap_cases(mcs, bases, case):
        for base in bases:
            if isinstance(base, mcs):
                case = base.wrap_cases(base.__bases__, case)
            elif issubclass(base, _WrapMixin):
                case = base.wrap_case(case)

        return case


class AsyncTest(AsyncMixin, metaclass=_AbsTestMeta):
    pass


class FlakyTest(
    FlakyMixin,
    metaclass=_AbsTestMeta
):
    pass


class AsyncFlakyTest(AsyncMixin, FlakyMixin, metaclass=_AbsTestMeta):
    pass
