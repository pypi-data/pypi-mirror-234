import os
import typing
from typing import Any
from pydantic import BaseModel, ConfigDict
from resumer.core.data import ResumerData
from resumer.utils import check_installed, dump_yaml, rename_bkup

class ResumerEngine(BaseModel):
    template : str 
    temporaryPath : str = "temp"
    pandocToType : typing.ClassVar[str]
    
    def model_post_init(self, __context: Any) -> None:
        if not hasattr(self, "pandocToType") or self.pandocToType is None:
            raise RuntimeError("pandocToType is not defined")

    model_config = ConfigDict(
        extra="allow"
    )

    def _internal_generate(self, data : dict, output : str):
        if not check_installed("pandoc"):
            raise RuntimeError("pandoc is not installed")

        if not os.path.exists(self.temporaryPath):
            os.makedirs(self.temporaryPath, exist_ok=True)

        input_path = os.path.join(self.temporaryPath, "input.md")

        rename_bkup(input_path)

        dump_yaml(input_path, data)

        rename_bkup(output)

        os.system(
            f'pandoc "{input_path}" -o "{output}" -f markdown \
            -t {self.pandocToType} --template="{self.template}"'
        )

        self.lastGenerated = output

    def create_output(self, output : str, data : ResumerData):
        raise NotImplementedError
    
    