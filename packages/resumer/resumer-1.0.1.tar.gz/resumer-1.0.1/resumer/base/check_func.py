
from functools import cached_property
from pydantic import BaseModel, Field, ConfigDict, model_validator
import typing

from resumer.utils import def_constructor

class CheckFuncBase(BaseModel):
    FUNC_FORMAT : typing.ClassVar[str] = "check_"
    FUNC_TYPE : typing.ClassVar[typing.Literal["prefix", "suffix"]] = "prefix"
    
    @classmethod
    def __is_check_func(cls, func_name : str):
        if cls.FUNC_TYPE == "prefix" and func_name.startswith(cls.FUNC_FORMAT):
            return True
        if cls.FUNC_TYPE == "suffix" and func_name.endswith(cls.FUNC_FORMAT):
            return True
        return False

    checks : typing.Dict[str, typing.Tuple[list, typing.Callable]] = Field(default_factory=dict,exclude=True)

    model_config = ConfigDict(
        extra="allow",
        ignored_types=(cached_property,)
    )

    @cached_property
    def check_func_mapping(self):
        is_ = {}
        is_not = {}
        for k, v in self.model_extra.items():
            if self.__is_check_func(k):
                is_[k] = v
            else:
                is_not[k] = v
        return is_, is_not


    @model_validator(mode="after")
    def __validate_vars_to_check(self):
        for k, v in self.check_func_mapping[0].items():
                
            if not isinstance(v, str):
                raise ValueError(f"{k} should be a string")
            
            self.checks[k] = def_constructor(v)

        return self
    
    def _run_check(self, entry, stop_at_first_true : bool = False):
        for (func, params_list) in self.checks.values():
            filtered_params = {k:v for k,v in entry.data.items() if k in params_list}
            
            if "self" in params_list:
                filtered_params["self"] = entry.data

            if "_entry_" in params_list:
                filtered_params["_entry_"] = entry
            
            if len(filtered_params) != len(params_list):
                return False

            if not func(**filtered_params):
                return False
            
            if stop_at_first_true:
                return True

        return True

