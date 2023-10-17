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
            file_name: mystring.string = self.file_name(result, extraString=result.tool_name, suffix="_compressed.csv", newFile=False)
            existed = os.path.exists(file_name)
            with open(file_name, "a+" if existed else "w+") as writer:
                if not existed:
                    writer.write("UUID,Base64\n")
                writer.write(result.uuid+","+mystring.string.of(result.jsonString).tobase64(prefix=True)+"\n")
            return True
        except Exception as e:
            print(e)
            return False
