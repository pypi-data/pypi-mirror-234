from typing import List, Dict, Union
from abc import ABC, abstractmethod
import mystring, uuid

try: #Python2
    import __builtin__ as builtins
except:
    import builtins


class RepoSifting(object):
    def __init__(self):
        self.uuid = mystring.string.of(str(uuid.uuid4()))
        self.stage = None

    def staticKeyTypeMap(self) -> Dict[str, type]:
        return {
            **{
                "uuid": mystring.string,
                "stage": mystring.string,
            },
            **self._internal_staticKeyTypeMap()
        }

    @staticmethod
    @abstractmethod
    def _internal_staticKeyTypeMap() -> Dict[str, type]:
        pass

    def toMap(self) -> Dict[str, Union[str, int, bool]]:
        #https://stackoverflow.com/questions/11637293/iterate-over-object-attributes-in-python
        #return {a:getattr(self,a) for a in dir(self) if not a.startswith('__') and not callable(getattr(self, a))}
        output:Dict[str, Union[str, int, bool]] = {}
        for key in self.staticKeyTypeMap().keys():
            output[key] = getattr(self,key)
        return output

    @property
    def frame(self):
        return mystring.frame.from_arr([self.toMap()])

    @property
    def jsonString(self):
        import json
        return json.dumps(self.toMap())

    @property
    def csvString(self):
        #https://stackoverflow.com/questions/9157314/how-do-i-write-data-into-csv-format-as-string-not-file
        import csv,io
        output = io.StringIO()
        writer = csv.writer(output, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(self.toMap().values())
        return output.getvalue()
    
    @property
    def csvHeader(self):
        #https://stackoverflow.com/questions/9157314/how-do-i-write-data-into-csv-format-as-string-not-file
        import csv,io
        output = io.StringIO()
        writer = csv.writer(output, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(self.staticKeyTypeMap.keys())
        return output.getvalue()

    @property
    def csvStrings(self):
        #https://stackoverflow.com/questions/9157314/how-do-i-write-data-into-csv-format-as-string-not-file
        import csv,io
        output = io.StringIO()
        writer = csv.writer(output, quoting=csv.QUOTE_NONNUMERIC)
        for value in self.toMap().values():
            writer.writerow(value)
        return output.getvalue()


class RepoObject(RepoSifting):
    def __init__(self, filename: mystring.string, hash: mystring.string, content: mystring.string, hasVuln: bool, cryVulnId: int, langPattern: mystring.string):
        super().__init__()
        self.filename = filename
        self.hash = hash
        self._content = content
        self.hasVuln = hasVuln
        self.cryVulnId = cryVulnId
        self.langPattern = langPattern

    @staticmethod
    def _internal_staticKeyTypeMap() -> Dict[str, type]:
        return {
            "filename": mystring.string,
            "hash": mystring.string,
            "_content": mystring.string,
            "hasVuln": bool,
            "cryVulnId": int,
            "langPattern": mystring.string
        };

    @property
    def content(self):
        return self._content
    
    @property
    def contentb64(self):
        return self._content.tobase64()


class RepoResultObject(RepoSifting):
    def __init__(self, projecttype: str, projectname: str, projecturl: str, qual_name: str, tool_name: str, Program_Lines: int, Total_Lines: int, Number_of_Imports: int, MCC: int, IsVuln: bool, ruleID: int, cryptolationID: int, CWEId: int, Message: str, Exception:str, llmPrompt:str, llmResponse:str, extraToolInfo:str, fileContent:str, Line: int, correctedCode:str, severity: str=None, confidence: str=None, context: str=None, TP: int=0, FP: int=0, TN: int=0, FN: int=0, dateTimeFormat:str="ISO 8601", startDateTime:str=None, endDateTime:str=None):
        super().__init__()
        self.projecttype = projecttype
        self.projectname = projectname
        self.projecturl = projecturl

        self.qual_name = qual_name
        self.tool_name = tool_name

        self.Program_Lines = Program_Lines
        self.Total_Lines = Total_Lines
        self.Number_of_Imports = Number_of_Imports
        self.MCC = MCC
        self.fileContent = fileContent

        self.IsVuln = IsVuln
        self.ruleID = ruleID
        self.cryptolationID = cryptolationID
        self.CWEId =  CWEId
        self.Message = Message
        self.Line = Line
        self.correctedCode = correctedCode
        self.severity = severity
        self.confidence = confidence
        self.context = context

        self.Exception = Exception
        self.extraToolInfo = extraToolInfo

        self.llmPrompt = llmPrompt
        self.llmResponse = llmResponse
        self.TP = TP
        self.FP = FP
        self.TN = TN
        self.FN = FN

        self.dateTimeFormat=dateTimeFormat
        self.startDateTime = startDateTime
        self.endDateTime = endDateTime

    @staticmethod
    def _internal_staticKeyTypeMap() -> Dict[str, type]:
        return {
            "projecttype": str,
            "projectname": str,
            "projecturl": str,
            "qual_name": str,
            "tool_name": str,
            "Program_Lines": int,
            "Total_Lines": int,
            "Number_of_Imports": int,
            "MCC": int,
            "IsVuln": bool,
            "ruleID": int,
            "cryptolationID": int,
            "CWEId": int,
            "Message": str,
            "Exception":str,
            "llmPrompt":str,
            "llmResponse":str,
            "extraToolInfo":str,
            "fileContent":str,
            "Line": int,
            "correctedCode":str,
            "severity": str,
            "confidence": str,
            "context": str,
            "TP": int,
            "FP": int,
            "TN": int,
            "FN": int,
            "dateTimeFormat":str,
            "startDateTime":str,
            "endDateTime":str
        };

    @staticmethod
    def fromCSVLine(line:mystring.string) -> Union[any,None]:
        numAttributes:int = len(RepoResultObject.staticKeyTypeMap().keys())
        splitLine:List[str] = [x.strip() for x in line.split(",")]

        if len(splitLine) != numAttributes:
            return None

        info:Dict[str, any] = {}
        for keyitr,key,value in enumerate(RepoResultObject.staticKeyTypeMap().items()):
            info[key] = getattr(builtins,value)(splitLine[keyitr])

        return RepoResultObject(**info)


class Runner(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def initialize(self)->bool:
        pass

    @abstractmethod
    def scan(self,filePath: str) -> List[RepoResultObject]:
        pass

    @abstractmethod
    def name(self) -> mystring.string:
        pass

    @abstractmethod
    def clean(self) -> bool:
        pass


class Logger(ABC):
    def __init__(self):
        self.stage:mystring.string = None

    @abstractmethod
    async def message(self, msg:mystring.string)->bool:
        pass

    @abstractmethod
    async def parameter(self,parameter:RepoObject)->bool:
        pass

    @abstractmethod
    async def result(self,result:RepoResultObject)->bool:
        pass

    async def start(self, stage:mystring.string):
        self.stage = stage
        await self.message("Entering the stage: {0}".format(self.stage))
        return self

    async def send(self, msg:Union[mystring.string, RepoObject, RepoResultObject])->bool:
        if isinstance(msg, RepoResultObject):
            return await self.result(msg)
        elif isinstance(msg, RepoObject):
            return await self.parameter(msg)
        else: #if isinstance(msg, mystring.string):
            return await self.message(msg)

    async def stop(self, exc_type, exc_val, exc_tb):
        await self.message("Exiting the stage: {0}".format(self.stage))
        return self


class LoggerSet(ABC):
    def __init__(self):
        self.loggers = []

    def __len__(self):
        return len(self.loggers)

    async def add(self, logger:Logger):
        self.loggers += [logger]

    async def start(self, stage:mystring.string):
        for logger in self.loggers:
            await logger.start(stage)
        return self

    async def send(self, msg:Union[mystring.string, RepoObject, RepoResultObject])->bool:
        for logger in self.loggers:
            await logger.send(msg)

    async def stop(self):
        for logger in self.loggers:
            await logger.stop()
        return self


class RepoObjectProvider(ABC):
    @property
    @abstractmethod
    def files(self) -> List[RepoObject]:
        pass


class contextString(object):
    def __init__(self, lines=List[str], vulnerableLine:str=None, imports:List[str] = []):
        self.lines:List[str] = lines
        self.vulnerableLine:str = vulnerableLine
        self.imports = imports

    @staticmethod
    def fromString(context:str) -> any:
        lines:List[str] = []
        vulnerableLine:str = None
        imports:List[str] = []

        for line in context.split("\n"):
            #001:       println("1")
            #002:       println("1") #!
            num:int = line.split(":")[0]
            content:str = line.split(":")[1]
            vulnerable:bool = content.endswith("#!")

            if vulnerable and vulnerableLine is None:
                vulnerableLine = content

            rawcontent:str = content.replace(line.strip(),'')
            whitespace:str = content.replace(rawcontent,'')
            isImport:bool = "import" in rawcontent
            if isImport:
                imports += [rawcontent]

            lines += [{
                "RawLine":line,
                "LineNum":num,
                "RawContent":rawcontent,
                "IsVulnerable":vulnerable,
                "Whitespace":whitespace,
                "IsImport":isImport
            }]
        
        return contextString(lines=lines, vulnerableLine=vulnerableLine, imports=imports)

    def toString(self) -> str:
        output = []

        for line in self.lines:
            output += "#{0}:{1}{2} {3}".format(
                line['LineNum'],
                line['Whitespace'],
                line['RawContent'],
                '#!' if line['IsVulnerable'] else ''
            )

        return '\n'.join(output)


class BetweenScans(ABC):    
    @abstractmethod
    def exe(self):
        pass

class GenProcedure(ABC):
    def __init__(self, fileProviders:List[RepoObjectProvider], runners:List[Runner], loggersset:List[Logger], perScan:Union[BetweenScans, None] = None, stage:Union[str, None]=None):
        self.fileProviders = fileProviders
        self.runners = runners
        self.loggers = loggersset
        self.loggerSet = LoggerSet()
        self.perScan = perScan
        self.stage = stage
        #https://superfastpython.com/asyncio-async-with/
    
    async def setLoggers(self):
        if len(self.loggerSet) == 0:
            for logger in self.loggers:
                await self.loggerSet.add(logger)
    
    @property
    def files(self) -> List[RepoObject]:
        for fileProvider in self.fileProviders:
            for file in fileProvider.files:
                yield file

    async def __aenter__(self):
        await self.setLoggers()

        if self.stage:
            await self.loggerSet.start(self.stage)
        return self
    
    async def __aexit__(self, _type=None, value=None, traceback=None):
        if self.stage:
            await self.loggerSet.end()
        return self
    
    @property
    def getRunnerProcedure(self):
        class RunnerProcedure(object):
            def __init__(self, runner:Runner, loggerSet):
                self.runner = runner
                self.loggerSet = loggerSet

            def __call__(self) -> Runner:
                return self.runner

            async def __aenter__(self):
                await self.loggerSet.send("Entering the runner {0}".format(self.runner.name()))
                self.runner.initialize()
                await self.loggerSet.send("Initialized the runner {0}".format(self.runner.name()))
                return self

            async def __aexit__(self, _type=None, value=None, traceback=None):
                await self.loggerSet.send("Exiting the runner {0}".format(self.runner.name()))
                self.runner.clean()
                await self.loggerSet.send("Cleaned the runner {0}".format(self.runner.name()))

        return lambda runner:RunnerProcedure(runner=runner, loggerSet=self.loggerSet)

    @abstractmethod
    async def run_procedure(self):
        pass
    
    async def scanFile(self, fileObj:RepoObject, runner:Runner)-> List[RepoResultObject]:
        from ephfile import ephfile
        await self.setLoggers()

        output:List[RepoResultObject] = []
        await self.loggerSet.start("Scanning {0} with {1}".format(fileObj.filename, runner.name()))
        with ephfile("{0}_stub.py".format(runner.name()), fileObj.content) as eph:
            await self.loggerSet.send("Started Scanning File {0}".format(fileObj.filename))

            startTime:datetime.datetime = mystring.timestamp.now()
            output = runner.scan(eph())
            endTime:datetime.datetime = mystring.timestamp.now()

            resultObject: RepoResultObject
            for resultObject in output:
                resultObject.startDateTime = startTime
                resultObject.endDateTime = endTime
                await loggers.send(resultObject)

            await self.loggerSet.send("Ended Scanning File {0}".format(fileObj.filename))
        await self.loggerSet.stop()
        if self.perScan:
            self.perScan.exe()
        return output