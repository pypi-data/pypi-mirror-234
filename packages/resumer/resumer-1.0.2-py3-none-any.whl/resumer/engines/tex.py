
import typing
from resumer.core.data import ResumerData
from resumer.core.engine import ResumerEngine
from resumer.utils import check_installed
import os

class TexEngine(ResumerEngine):
    pandocToType : typing.ClassVar[str]= "latex"

    includeDirs : str = None

    def create_output(self, output: str, data: ResumerData):
        temp_output = output
        gen_pdf = False
        output_dir = os.path.dirname(output)

        if output_dir == "":
            output_dir = os.getcwd()

        if output.endswith(".pdf"):
            temp_output = output[:-4] + ".tex"
            gen_pdf = True

        self._internal_generate(data.toDict(), temp_output)

        if not gen_pdf:
            return

        if not check_installed("xelatex"):
            raise RuntimeError("xelatex is not installed")
        
        cmd = f"xelatex {temp_output} -output-directory={output_dir}"

        if self.includeDirs is not None:
            cmd += f" -include-directory={self.includeDirs}"

        os.system(cmd)
        self.lastGenerated = output