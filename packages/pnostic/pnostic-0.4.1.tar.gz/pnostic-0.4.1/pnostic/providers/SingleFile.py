import mystring as mys
from typing import List

from pnostic.structure import RepoObjectProvider, RepoObject


class app(RepoObjectProvider):
    def __init__(self, content:str, vulnId:int=-1, langPattern:str=""):
        self.content = mys.string(content)
        self.vulnId = vulnId
        self.hasVuln = self.vulnId is not -1
        self.langPattern = langPattern
        self.filename = "stub.py"

    @property
    def files(self) -> List[RepoObject]:
        yield RepoObject(
            filename=self.filename,
            hash=self.content.tohash(),
            content=self.content,
            hasVuln=self.hasVuln,
            cryVulnId=self.vulnId,
            langPattern=self.langPattern
        )
