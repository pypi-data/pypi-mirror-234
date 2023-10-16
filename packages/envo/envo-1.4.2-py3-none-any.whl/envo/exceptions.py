import sys
import traceback
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from types import FrameType, TracebackType
from typing import List, Optional, Tuple

import envo

__all__ = [
    "UserError",
]

from envo.utils import mocked


@dataclass
class UserError(Exception):
    msg: str
    exc: Exception = RuntimeError()

    def __str__(self) -> str:
        return self.msg


@contextmanager
def user_code() -> None:
    package_root = Path(envo.__file__).parent
    orig_walk_tb = traceback.walk_tb

    if sys.version_info < (3, 11):
        def walk_tb(tb: Optional[TracebackType]) -> List[Tuple[FrameType, int]]:
            # With frame reloader enabled there might be frames coming from error handler
            # W remove them here as well other junk
            raw = list(orig_walk_tb(tb))

            frame_to_entry = {}
            for r in raw:
                f: FrameType = r[0]
                if package_root in Path(f.f_code.co_filename).parents:
                    continue

                frame_to_entry[f] = r

            ret = list(frame_to_entry.values())

            return ret

        with mocked(traceback, "walk_tb", walk_tb):
            yield
    else:
        orig = traceback.StackSummary._extract_from_extended_frame_gen

        def _extract_from_extended_frame_gen(frame_gen, *, limit=None, lookup_lines=True,
                                             capture_locals=False):  # obf: ignore frame_gen, capture_locals, limit, lookup_lines
            file_to_tb = {}

            kwargs = {
                "frame_gen": frame_gen,
                "limit": limit,
                "lookup_lines": lookup_lines,
                "capture_locals": capture_locals
            }
            ret_orig = orig(**kwargs)
            ret = traceback.StackSummary()
            for r in ret_orig:
                if package_root in Path(r.filename).parents:
                    continue

                file_to_tb[r.filename] = r

            for r in file_to_tb.values():
                ret.append(r)

            if ret and len(ret) != 1 and ret[0].lineno == 1:
                ret.pop(0)

            return ret

        with mocked(
                traceback.StackSummary,
                "_extract_from_extended_frame_gen",
                _extract_from_extended_frame_gen
        ):
            yield
