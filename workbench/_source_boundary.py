"""Keep borrowed editable environments from supplying unfinished course modules."""
from importlib.machinery import PathFinder
from pathlib import Path
import sys


class _PersonalSourceBoundary:
    def __init__(self):
        self.root = Path(__file__).resolve().parents[1]

    def find_spec(self, fullname, path=None, target=None):
        package = fullname.split('.', 1)[0]
        if package not in {'workbench', 'eval', 'agent', 'harness_web'}:
            return None
        if '.' in fullname:
            parent = sys.modules.get(fullname.rpartition('.')[0])
            parent_file = getattr(parent, '__file__', None)
            if not parent_file or not Path(parent_file).resolve().is_relative_to(self.root):
                return None
        spec = PathFinder.find_spec(fullname, path)
        locations = [] if spec is None else list(spec.submodule_search_locations or ())
        local = spec is not None and (
            spec.origin is not None and Path(spec.origin).resolve().is_relative_to(self.root)
            or spec.origin is None and bool(locations)
            and all(Path(location).resolve().is_relative_to(self.root) for location in locations))
        if not local:
            raise ModuleNotFoundError(
                f'个人项目尚未实现 {fullname}；拒绝从参考仓库借入该模块', name=fullname)
        return spec


def install():
    if not any(isinstance(finder, _PersonalSourceBoundary) for finder in sys.meta_path):
        sys.meta_path.insert(0, _PersonalSourceBoundary())
