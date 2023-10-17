from typing import Tuple, List, Dict, Union
from pnostic.structure import Logger, RepoResultObject, RepoObject, RepoSifting

class app(Logger):
    def __init__(self):
        super().__init__()

    def message(self, msg: str) -> bool:
        return True

    def parameter(self, parameter: RepoObject) -> bool:
        parameter.frame.to_pkl(
            self.file_name(parameter, parameter.filename, suffix=".pkl")
        )
        return True

    def result(self, result: RepoResultObject) -> bool:
        result.frame.to_pkl(
            self.file_name(result, result.tool_name, suffix=".pkl")
        )
        return True
