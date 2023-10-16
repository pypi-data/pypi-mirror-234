
from resumer.core.data import ResumerData
from resumer.core.engine import ResumerEngine


class GenericEngine(ResumerEngine):
    pandocToType : str

    def create_output(self, output: str, data: ResumerData):
        return self._internal_generate(data.toDict(), output)