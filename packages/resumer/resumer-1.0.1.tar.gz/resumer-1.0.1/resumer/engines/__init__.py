from resumer.core.engine import ResumerEngine
from resumer.engines.generic import GenericEngine
from resumer.engines.tex import TexEngine
from importlib.util import module_from_spec, spec_from_file_location
import inspect 
import os

engine_mapping = {
    "TexEngine" : TexEngine,
    "GenericEngine" : GenericEngine
}

def resolve_engine(output_path : str):
    if output_path is None:
        raise RuntimeError("output_path is None")
    output_extension = os.path.splitext(output_path)[1]
    match output_extension:
        case ".tex":
            return TexEngine
        case _:
            raise NotImplementedError


def _load_engine(path : str):
    # engine_type_str is path
    spec = spec_from_file_location("CustomEngine", path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    for key, value in inspect.getmembers(module):
        if not inspect.isclass(value):
            continue
        if value == ResumerEngine:
            continue

        if issubclass(value, ResumerEngine):
            return value

def engine_from_dict(data : dict, output : str = None):
    engine_type_str = data.pop("engine_type", None)

    if output is None:
        output = data.pop("output", None)

    if engine_type_str is None:
        engine_type = resolve_engine(output)
    elif engine_type_str in engine_mapping:
        engine_type = engine_mapping[engine_type_str]
    else:
        engine_type = _load_engine(engine_type_str)

    return engine_type(**data), output

        

        
