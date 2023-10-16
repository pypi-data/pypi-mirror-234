from pydantic import BaseModel, Field
import typing

class MatcherBase(BaseModel):
    """
    this class is a base implementation for filters
    """

    tags : typing.List[str] = Field(default_factory=list)
    x_mode : typing.Literal["include", "exclude"] = "include"
    x_scope : typing.Literal["all", "any", "at_least_one"] = "any"

    def __match_include(self, tags: typing.List[str]):
        if self.x_scope == "all" and tags == self.tags:
            return True
        elif self.x_scope == "any" and any([tag in tags for tag in self.tags]):
            return True
        elif self.x_scope != "at_least_one":
            return False
        
        counter = 0
        for tag in tags:
            if tag in self.tags:
                counter += 1
            if counter > 1:
                return True

        return False

    def __match_exclude(self, tags: typing.List[str]):
        if self.x_scope == "all" and tags != self.tags:
            return False
        elif self.x_scope == "any" and not any([tag in tags for tag in self.tags]):
            return False
        elif self.x_scope != "at_least_one":
            return True
        
        counter = 0
        for tag in tags:
            if tag in self.tags:
                counter += 1
            if counter > 1:
                return False

        return True

    def match_tags(self, tags: typing.List[str]):
        """
        Matches the given tags based on the `x_mode` and `x_scope` attribute.

        Args:
            tags (List[str]): The list of tags to match.

        Returns:
            The result of the matching operation.
        """

        if len(self.tags) == 0:
            return True

        if self.x_mode == "include":
            return self.__match_include(tags)
        else:
            return self.__match_exclude(tags)
        
