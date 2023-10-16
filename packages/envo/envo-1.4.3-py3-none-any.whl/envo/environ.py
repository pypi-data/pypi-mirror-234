from typing import Optional

import envium
from envium import env_var

__all__ = ["Environ", "environ", "TestType"]


class TestType:
    UNIT = "unit"
    E2E = "e2e"


class Environ(envium.Environ):
    test_type: Optional[str] = env_var()
    stickybeak: bool = env_var(default=False)
    colors: bool = env_var(default=True)
    stage: Optional[str] = env_var()


environ = Environ(name="envo", load=True)
