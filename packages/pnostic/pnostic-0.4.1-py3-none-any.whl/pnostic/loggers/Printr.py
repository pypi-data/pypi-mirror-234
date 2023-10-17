from pnostic.structure import Logger, RepoResultObject, RepoObject
import mystring


class app(Logger):
    def __init__(self):
        super().__init__()
        return None

    def message(self, msg: mystring.string) -> bool:
        print(msg)
        return True

    def parameter(self, parameter: RepoObject) -> bool:
        print(parameter)
        return True

    def result(self, result: RepoResultObject) -> bool:
        print(result)
        return True
