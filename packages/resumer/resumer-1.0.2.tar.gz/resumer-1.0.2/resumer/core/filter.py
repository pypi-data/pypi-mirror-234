
import tomllib
import typing
from pydantic import ConfigDict, Field
from resumer.base.check_func import CheckFuncBase
from resumer.base.match import MatcherBase
from resumer.core.data import ResumerData, ResumerEntry
from resumer.utils.string import parse_string

class ResumerFilterBase(MatcherBase):
    model_config = ConfigDict(
        extra="allow"
    )

class ResumerFilterUnit(ResumerFilterBase, CheckFuncBase):
    drills : typing.List[str] = Field(default_factory=list)
    stop_at_first_check : bool = False

    def __eq__(self, __value: object) -> bool:
        if self.drills != __value.drills:
            return False
        
        if self.tags != __value.tags:
            return False
        
        if self.x_mode != __value.x_mode:
            return False
        
        if self.x_scope != __value.x_scope:
            return False
        
        if self.check_func_mapping != __value.check_func_mapping:
            return False

        return True

    def filter(self, entry: ResumerEntry) -> bool:
        if not self.match_tags(entry.tags):
            return False
        
        for k, v in self.check_func_mapping[1].items():
            ev = entry.data.get(k, None)
            if ev is None:
                return False
            if v != ev:
                return False
            
        if not self._run_check(entry, self.stop_at_first_check):
            return False

        return True
    
class ResumerFilter(ResumerFilterBase):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True
    )

    entries : typing.Dict[str, typing.Union[bool, ResumerFilterUnit]] = Field(default_factory=dict)
    exclude_keys : typing.List[str] = Field(default_factory=list)
    drills : typing.List[str] = Field(default_factory=list)

    def __parse_drill(self, data : typing.Union[str,list, dict], drills : typing.List[str]):
        if isinstance(data, str):
            res = parse_string(data, drills)
            return res[0]
        elif isinstance(data, list):
            for i, item in enumerate(data):
                data[i] = self.__parse_drill(item, drills)
            return data
        elif isinstance(data, dict):
            for k, v in data.items():
                data[k] = self.__parse_drill(v, drills)
            return data
        elif isinstance(data, ResumerEntry):
            newEntry = data.copy()
            newEntry.data = self.__parse_drill(data.data, drills)
            return newEntry
        else:
            return data

    def filter(self, data: ResumerData) -> ResumerData:
        new_data = ResumerData()
        for key, value in data.simpleKeyData.items():
            if key not in self.exclude_keys:
                new_data.simpleKeyData[key] = self.__parse_drill(value, self.drills)
        
        for key, listdata in data.entries.items():
            filter_ = self.entries.get(key, None)
            if filter_ is False:
                continue
            
            if key not in new_data.entries:
                new_data.entries[key] = []

            drills = self.drills + filter_.drills if filter_ else self.drills

            for entry in listdata:
                if not self.match_tags(entry.tags):
                    continue
                if isinstance(filter_, ResumerFilterUnit) and not filter_.filter(entry):
                    continue

                new_data.entries[key].append(self.__parse_drill(entry, drills))

        if len(new_data.entries[key]) == 0:
            del new_data.entries[key]

        return new_data
    
    @classmethod
    def from_toml(cls, filename : str = None, config : dict= None):
        if filename is not None:
            with open(filename, "rb") as file:
                config = tomllib.load(file)

        return cls(**config)
    