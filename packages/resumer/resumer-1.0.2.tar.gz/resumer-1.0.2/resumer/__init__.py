
import os
import tomllib
import typing
from resumer.core.data import ResumerData
from resumer.core.engine import ResumerEngine
from resumer.core.filter import ResumerFilter
from resumer.engines import engine_from_dict
from resumer.engines.tex import TexEngine
from resumer.utils.download import download_asset, preset_directory

def auto_generate(
    engine_config : typing.Union[str, dict],
    data : typing.Union[str, dict, typing.List[str]],
    filter_config : typing.Union[str, dict] = None
):
    if isinstance(engine_config, str):
        with open(engine_config, "rb") as file:
            engine_config = tomllib.load(file)

    engine, output = engine_from_dict(engine_config)

    if isinstance(data, list):
        data = ResumerData.from_multi_toml(*data)
    elif isinstance(data, str) and os.path.isdir(data):
        data = ResumerData.from_multi_toml(data)
    elif isinstance(data, str):
        data = ResumerData.from_toml(data)
    else:
        data = ResumerData(**data)

    if isinstance(filter_config, str):
        filter = ResumerFilter.from_toml(filter_config)
    elif isinstance(filter_config, dict):
        filter = ResumerFilter(**filter_config)
    else:
        filter = ResumerFilter()    
    data = filter.filter(data)

    engine.create_output(output, data)
    

def auto_awesome_tex(
    data : typing.Union[str, dict, typing.List[str]],
    filter_config : typing.Union[str, dict] = None,
    output : str = "output/output.pdf",
    template : str = os.path.join(preset_directory, "awesome.tex"),
):
    download_asset()
    engine = TexEngine(
        template=template,
        includeDirs=os.path.abspath(preset_directory)
    )

    if isinstance(data, list):
        data = ResumerData.from_multi_toml(*data)
    elif isinstance(data, str) and os.path.isdir(data):
        data = ResumerData.from_multi_toml(data)
    elif isinstance(data, str):
        data = ResumerData.from_toml(data)
    else:
        data = ResumerData(**data)

    if isinstance(filter_config, str):
        filter = ResumerFilter.from_toml(filter_config)
    elif isinstance(filter_config, dict):
        filter = ResumerFilter(**filter_config)
    else:
        filter = ResumerFilter()    
    data = filter.filter(data)

    engine.create_output(output, data)