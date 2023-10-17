from typing import List
import mystring
from pnostic.structure import RepoResultObject, Runner


class app(Runner):
    def __init__(self):
        super().__init__()

    def initialize(self) -> bool:
        print("Initializing")
        return True

    def scan(self, filePath: str) -> List[RepoResultObject]:
        print("Going to scan {0}".format(filePath))
        return []

    def name(self) -> mystring.string:
        return mystring.string.of("SimpleRunner")

    def clean(self) -> bool:
        print("Cleaning")
        return True
