import os, mystring
from typing import List

from pnostic.structure import Logger, RepoResultObject, RepoObject


class app(Logger):
    def __init__(self):
        super().__init__()

    def message(self, msg: mystring.string) -> bool:
        return True

    def parameter(self, parameter: RepoObject) -> bool:
        return True

    def result(self, result: RepoResultObject) -> bool:
        try:
            file_name: mystring.string = self.file_name(result, extraString=result.tool_name, suffix=".csv", newFile=False)
            existed = os.path.exists(file_name)
            with open(file_name, "a+" if existed else "w+") as writer:
                if not existed:
                    writer.write(result.csvHeader()+"\n")

                lines: List[str] = result.csvStrings().split("\n")
                for line in lines:
                    writer.write(result.csv+("\n" if line != lines[-1] else ""))
            return True
        except Exception as e:
            print(e)
            return False
