import os
import typing
from pydantic import BaseModel, Field
import tomllib

class ResumerDataBase(BaseModel):
    pass
        
class ResumerEntry(ResumerDataBase):
    tags : typing.List[str] = Field(default_factory=list)
    data : dict

class ResumerData(ResumerDataBase):

    simpleKeyData : typing.Dict[str, typing.Any] = Field(default_factory=dict)
    entries : typing.Dict[str, typing.List[ResumerEntry]] = Field(default_factory=dict)

    def toDict(self):
        output = {}
        for key, value in self.simpleKeyData.items():
            output[key] = value
        for key, value in self.entries.items():
            output[key] = [entry.data for entry in value]
        return output
    
    @classmethod
    def from_toml(cls, filename : str = None, data : dict= None):
        if filename is not None:
            with open(filename, "rb") as file:
                data = tomllib.load(file)

        simplekv = {}
        entries = {}
        for k, v in data.items():
            if not (isinstance(v, list) and all(isinstance(i, dict) for i in v)):
                simplekv[k] = v
                continue

            entries[k] = [ResumerEntry(tags=x.pop("tags", []), data=x) for x in v]

        return ResumerData(simpleKeyData=simplekv, entries=entries)
    
    @classmethod
    def from_multi_toml(cls, *paths):
        rdata : ResumerData = ResumerData()

        pending_paths = list(paths)

        while len(pending_paths) > 0:
            path = pending_paths.pop(0)
            if os.path.isdir(path):
                pending_paths.extend([os.path.join(path, x) for x in os.listdir(path)])
                continue
            elif not path.endswith(".toml"):
                continue

            with open(path, "rb") as file:
                data = tomllib.load(file)

            for k, v in data.items():
                

                if not (isinstance(v, list) and all(isinstance(i, dict) for i in v)):
                    rdata.simpleKeyData[k] = v
                    continue

                if k not in rdata.entries:
                    rdata.entries[k] = []

                for entry in v:
                    tags=entry.pop("tags", [])
                    rdata.entries[k].append(ResumerEntry(tags=tags, data=entry))
            

        return rdata
                
