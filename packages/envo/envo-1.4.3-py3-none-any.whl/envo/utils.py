import importlib.machinery
import importlib.util
import sys
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from types import FrameType
from typing import Any, Callable, Dict, Generator, List, Optional, Tuple, Union

from globmatch import glob_match
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

__all__ = [
    "import_from_file",
    "add_source_roots",
    "get_repo_root",
    "dir_name_to_class_name",
    "get_src_root",
    "render_py_file",
    "render_file",
    "colored",
]


from envo.logs import logger


class Callback:
    def __init__(self, func: Optional[Callable[..., Any]] = None) -> None:
        self.func = func

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        if not self.func:
            return
        return self.func(*args, **kwargs)

    def __bool__(self) -> bool:
        return self.func is not None


class InotifyPath:
    def __init__(self, raw_path: Path, root: Path) -> None:
        self.absolute = raw_path.absolute()
        self.relative = self.absolute.relative_to(root)
        self.relative_str = str(self.relative)

        if self.relative.is_dir():
            self.relative_str += "/"

    def match(self, include: List[str], exclude: List[str]) -> bool:
        return not glob_match(self.relative_str, exclude) and glob_match(self.relative_str, include)

    def is_dir(self) -> bool:
        return self.absolute.is_dir()


class EventDispatcher(FileSystemEventHandler):
    observer: Observer
    watchers: List["FilesWatcher"]
    paths: List[Path]

    def __init__(self) -> None:
        self.observer = Observer()
        self.observer.start()
        self.paths = []
        self.watchers = []

    def add(self, watcher: "FilesWatcher") -> None:
        self.watchers.append(watcher)

        for p in watcher.paths:
            if p not in self.paths:
                self.observer.schedule(self, str(p), recursive=False)
                self.paths.append(p)

    def flush(self) -> None:
        self.observer.event_queue.queue.clear()

    def remove(self, watcher: "FilesWatcher") -> None:
        for i, w in enumerate(self.watchers):
            if w is watcher:
                self.watchers.pop(i)
                return

    def on_any_event(self, event: FileSystemEvent):
        for w in self.watchers.copy():
            try:
                relative = Path(event.src_path).relative_to(w.root)
            except ValueError:
                continue
            if w.match(relative):
                w.on_any_event(event)


event_dispatcher = EventDispatcher()


class FilesWatcher:
    @dataclass
    class Sets:
        include: List[str]
        exclude: List[str]
        root: Path
        name: str = "Anonymous"

    @dataclass
    class Callbacks:
        on_event: Callback

    paths: List[Path]

    def __init__(self, se: Sets, calls: Callbacks):
        self.include = [p.lstrip("./") for p in se.include]
        self.exclude = [p.lstrip("./") for p in se.exclude]
        self.root = se.root

        super().__init__()
        self.se = se
        self.calls = calls

        self.paths = []
        self.enabled = True

        for p in self.se.include:
            path = (self.se.root / p).parent
            if not path.exists():
                continue

            if path not in self.paths:
                self.paths.append(path)

        if self.se.root not in self.paths:
            self.paths.append(self.se.root)

        event_dispatcher.add(self)

    def on_any_event(self, event: FileSystemEvent):
        if not self.enabled:
            return
        self.calls.on_event(event)

    def match(self, path: Path) -> bool:
        return not glob_match(str(path), self.exclude) and glob_match(str(path), self.include)

    def stop(self) -> None:
        self.enabled = False
        event_dispatcher.remove(self)


def dir_name_to_class_name(dir_name: str) -> str:
    class_name = dir_name.replace("_", " ")
    class_name = class_name.replace("-", " ")
    class_name = class_name.replace(".", " ")
    s: str
    class_name = "".join([s.strip().capitalize() for s in class_name.split()])

    return class_name


def dir_name_to_pkg_name(dir_name: str) -> str:
    pkg_name = dir_name.replace("_", " ")
    class_name = pkg_name.replace("-", " ")
    class_name = class_name.replace(".", " ")
    s: str
    class_name = "_".join([s.strip() for s in class_name.split()])

    return class_name


def is_valid_module_name(module: str) -> bool:
    from keyword import iskeyword

    return module.isidentifier() and not iskeyword(module)


def render_file(template_path: Path, output: Path, context: Dict[str, Any]) -> None:
    content = template_path.read_text()
    for n, v in context.items():
        content = content.replace(f"{{{{ {n} }}}}", v)

    output.write_text(content, encoding="utf-8")


def render_py_file(template_path: Path, output: Path, context: Dict[str, Any]) -> None:
    render_file(template_path, output, context)


def path_to_module_name(path: Path, package_root: Path) -> str:
    rel_path = path.resolve().absolute().relative_to(package_root.resolve())
    ret = str(rel_path).replace(".py", "").replace("/", ".").replace("\\", ".")
    ret = ret.replace(".__init__", "")
    return ret


def import_from_file(path: Union[Path, str]) -> Any:
    path = Path(path)
    loader = importlib.machinery.SourceFileLoader(str(path), str(path))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)

    return module


def import_env_from_file(path: Union[Path, str]) -> Any:
    # Ensure all env modules are reloaded
    for n, m in sys.modules.copy().items():
        if not hasattr(m, "__file__"):
            continue
        if not m.__file__:
            continue
        # Check if it's env file
        if not Path(m.__file__).name.startswith("env_"):
            continue

        del sys.modules[n]

    ret = import_from_file(path)

    return ret


def get_module_from_full_name(full_name: str) -> Optional[str]:
    parts = full_name.split(".")

    while True:
        module_name = ".".join(parts)
        if module_name in sys.modules:
            return module_name
        parts.pop(0)
        if not parts:
            return None


PLATFORM_WINDOWS = "windows"
PLATFORM_LINUX = "linux"
PLATFORM_BSD = "bsd"
PLATFORM_DARWIN = "darwin"
PLATFORM_UNKNOWN = "unknown"


def get_platform_name():
    if sys.platform.startswith("win"):
        return PLATFORM_WINDOWS
    elif sys.platform.startswith("darwin"):
        return PLATFORM_DARWIN
    elif sys.platform.startswith("linux"):
        return PLATFORM_LINUX
    elif sys.platform.startswith(("dragonfly", "freebsd", "netbsd", "openbsd", "bsd")):
        return PLATFORM_BSD
    else:
        return PLATFORM_UNKNOWN


__platform__ = get_platform_name()


def is_linux():
    return __platform__ == PLATFORM_LINUX


def is_bsd():
    return __platform__ == PLATFORM_BSD


def is_darwin():
    return __platform__ == PLATFORM_DARWIN


def is_windows():
    return __platform__ == PLATFORM_WINDOWS


def add_source_roots(paths: List[Union[Path, str]]) -> None:
    logger.debug(f"Adding source roots {paths}")
    for p in paths:
        if not str(p).strip():
            continue

        if str(p) in sys.path:
            sys.path.remove(str(p))

        sys.path.insert(0, str(p))


def get_src_root(name: str, file: Optional[str] = None) -> Path:
    root = Path(file).parent if file else "."
    path = Path(root).absolute()

    while not list(path.glob(f"*{name}")):
        if path == path.parent:
            raise RuntimeError(f'Cannot find src root (missing "{name}" file?)')
        path = path.parent

    return path


def get_repo_root() -> Path:
    return get_src_root(".git")


def iterate_frames(frame: FrameType) -> Generator[FrameType, None, None]:
    current_frame: Optional[FrameType] = frame
    while current_frame:
        yield current_frame
        current_frame = current_frame.f_back


def colored(inp: str, color: Tuple[int, int, int]) -> str:
    ret = f"\033[38;2;{color[0]};{color[1]};{color[2]}m{inp}\x1b[0m"
    return ret


@contextmanager
def mocked(obj: Any, attr_name: str, target: Any) -> Generator[None, None, None]:
    orig = getattr(obj, attr_name)
    setattr(obj, attr_name, target)
    yield
    setattr(obj, attr_name, orig)
