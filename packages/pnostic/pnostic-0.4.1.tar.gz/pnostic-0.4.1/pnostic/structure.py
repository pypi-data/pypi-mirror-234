from typing import List, Dict, Union, Callable
from abc import ABC, abstractmethod
import mystring, uuid, threading

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
        }

    def updateContent(self, newContent:mystring.string):
        self._content = newContent
        return self._content

    @property
    def content(self):
        return self._content
    
    @property
    def contentb64(self):
        return self._content.tobase64()


class RepoResultObject(RepoSifting):
    def __init__(self, projecttype: str, projectname: str, projecturl: str, qual_name: str, tool_name: str, Program_Lines: int, Total_Lines: int, Number_of_Imports: int, MCC: int, IsVuln: bool, ruleID: int, cryptolationID: int, CWEId: int, Message: str, Exception:str, llmPrompt:str, llmResponse:str, extraToolInfo:str, fileContent:str, Line: int, correctedCode:str, severity: str=None, confidence: str=None, context: str=None, TP: int=0, FP: int=0, TN: int=0, FN: int=0, dateTimeFormat:str="ISO 8601", startDateTime:str=None, endDateTime:str=None, stage:str=None):
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
        self.stage = stage

    @staticmethod
    def newEmpty(projecttype: str,projectname: str,projecturl: str,qual_name: str,tool_name: str,ExceptionMsg:str=None,stage:str=None,startDateTime:str=None,endDateTime:str=None):
        return RepoResultObject(
            projecttype=projecttype,
            projectname=projectname,
            projecturl=projecturl,
            qual_name=qual_name,
            tool_name=tool_name,
            Program_Lines=None,
            Total_Lines=None,
            Number_of_Imports=None,
            MCC=None,
            IsVuln=False,
            ruleID=None,
            cryptolationID=None,
            CWEId=None,
            Message=None,
            Exception=ExceptionMsg,
            llmPrompt=None,
            llmResponse=None,
            extraToolInfo=None,
            fileContent=None,
            Line=None,
            correctedCode=None,
            severity=None,
            confidence=None,
            context=None,
            TP=0,
            FP=0,
            TN=0,
            FN=0,
            dateTimeFormat="ISO 8601",
            startDateTime=startDateTime,
            endDateTime=endDateTime,
            stage=stage
        )

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
            "endDateTime":str,
            "stage":str
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
    def message(self, msg:mystring.string)->bool:
        pass

    @abstractmethod
    def parameter(self,parameter:RepoObject)->bool:
        pass

    @abstractmethod
    def result(self,result:RepoResultObject)->bool:
        pass

    def file_name(self, result:RepoSifting, extraString:str=None, prefix:str=None, suffix:str=".txt", newFile:bool=True)->str:
        current_file = mystring.string.of("{0}_{1}_{2}_{3}".format(
            prefix,
            result.uuid,
            extraString,
            suffix
        ))

        if newFile:
            ktr = 0
            while os.path.exists(current_file):
                current_file = current_file.replace(suffix, "_{0}{1}".format(ktr, suffix))
                ktr += 1

        return current_file

    def start(self, stage:mystring.string):
        self.stage = stage
        self.send(":>␍ Entering the stage: {0}".format(self.stage))
        return self

    def send(self, msg:Union[mystring.string, RepoObject, RepoResultObject])->bool:
        successful = True
        try:
            if isinstance(msg, RepoResultObject):
                self.result(msg)
            elif isinstance(msg, RepoObject):
                self.parameter(msg)
            else: #if isinstance(msg, mystring.string):
                self.message(msg)
        except Exception as e:
            print("Problem Sending Log From {0}; {1}".format(self.name(), msg.__class__.__name__))
            successful = False
        return successful

    def stop(self):
        self.send(":>␌ Exiting the stage: {0}".format(self.stage))
        return self


class LoggerSet(object):
    def __init__(self, loggers=[], stage:str=None):
        self.loggers = loggers
        self.stage = stage

    def __len__(self):
        return len(self.loggers)

    def add(self, logger:Logger):
        self.loggers += [logger]

    def start(self, stage:mystring.string):
        for logger in self.loggers:
            logger.send(":>␋ sending to logger")
            logger.start(self.stage or stage)
            logger.send(":>␋ ^^^^^ sending to logger")
        return self

    def send(self, msg:Union[mystring.string, RepoObject, RepoResultObject])->bool:
        for logger in self.loggers:
            logger.send(":>␈ sending to logger")
            logger.send(msg)
            logger.send(":>␈ end sending to logger")

    def stop(self):
        for logger in self.loggers:
            logger.send(":>␇ sending to logger")
            logger.stop()
            logger.send(":>␇ end sending to logger")
        return self

    def __enter__(self, stage:Union[mystring.string, None]=None):
        stage = self.stage or stage
        self.start(stage=stage)
        return self

    def __exit__(self, _type=None, value=None, traceback=None):
        self.stop()


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


class GenProcedure(ABC):
    """
class operation(structure.GenProcedure):
	def __init__(self):
		super().__init__(
			fileProviders = [
				SingleFile.app(content="import os,sys;print('Hello World')")
			],
			runners = [
				simple.app(),
			],
			loggersset = [
				Printr.app(),
			],
			perScan = None,
			stage = None
		)

	def run_procedure(self):
		with structure.LoggerSet(loggers=self.loggerSet.loggers, stage="StageOne") as logggg:
			for runnerSvr in self.runners:
				with self.getRunnerProcedure(runnerSvr) as runner:
					for fileObj in self.files:
						firstScanResults: List[RepoResultObject] = self.scanFile(fileObj, runner())
		return
operation().run_procedure()
    """
    def __init__(self, fileProviders:List[RepoObjectProvider], runners:List[Runner], loggersset:List[Logger], perScan:Union[Callable, None] = None, stage:Union[str, None]=None):
        self.fileProviders = fileProviders
        self.runners = runners

        self.perScan = perScan
        self.stage = stage
        #https://superfastpython.com/asyncio-async-with/
        self.loggerSet = LoggerSet()
        for logger in loggersset:
            self.loggerSet.add(logger)            

    def log(self, msg:Union[mystring.string, RepoObject, RepoResultObject]):
        self.loggerSet.send(msg)

    @property
    def files(self) -> List[RepoObject]:
        for fileProvider in self.fileProviders:
            for file in fileProvider.files:
                yield file

    def __enter__(self):
        if self.stage:
            self.loggerSet.start(stage=self.stage)
        return self

    def __exit__(self, _type=None, value=None, traceback=None):
        if self.stage:
            self.loggerSet.end()
        return self

    @property
    def getRunnerProcedure(self):
        class RunnerProcedure(object):
            def __init__(self, runner:Runner, loggerSet, scanr):
                self.runner = runner
                self.loggerSet = loggerSet
                self.scanFile = scanr

            def log(self, msg:Union[mystring.string, RepoObject, RepoResultObject]):
                self.loggerSet.send(":>␄ START LOG")
                self.loggerSet.send(msg)
                self.loggerSet.send(":>␄ END LOG")

            def __call__(self) -> Runner:
                return self.runner

            def scan(self, fileObj):
                self.scanFile(fileObj, self.runner)

            def __enter__(self):
                self.loggerSet.send(":>␅ START")
                self.runner.initialize()
                self.loggerSet.send(":>␅ END START")
                return self

            def __exit__(self, _type=None, value=None, traceback=None):
                self.loggerSet.send(":>␆ START")
                self.runner.clean()

        return lambda runner:RunnerProcedure(runner=runner, loggerSet=self.loggerSet, scanr=self.scanFile)

    def process(self, isAliveMin:int=None):
        with LoggerSet(self.loggerSet.loggers, stage=":>. Starting the overall process") as logy:
            def alive(min:int=None, loggerSet=None):
                import time
                while True:
                    loggerSet.send(":> Still Alive")
                    time.sleep(60 * min)

            aliveThread = None
            if isAliveMin:
                aliveThread = threading.Thread(target=alive, args=(isAliveMin, self.loggerSet), daemon = True)
                aliveThread.start()

            try:
                logy.send(":> Starting the procedure")
                self.run_procedure()
            except Exception as e:
                logy.send(":> Hit an unexpected error {0}".format(e))
            finally:
                logy.send(":> Closing the process")
        sys.exit(0)

    @abstractmethod
    def run_procedure(self):
        pass

    def scanFile(self, fileObj:RepoObject, runner:Runner, stage:mystring.string=None, notHollow:bool=False)-> List[RepoResultObject]:
        from ephfile import ephfile

        exceptionString = None
        output:List[RepoResultObject] = []

        try:
            with LoggerSet(self.loggerSet.loggers, stage="␃ Scanning {0} with {1}".format(fileObj.filename, runner.name())) as logy:
                logy.send("␀ Starting For Loop")
                logy.send(fileObj)
                with ephfile("{0}_stub.py".format(runner.name()), fileObj.content) as eph:
                    logy.send("␁ Started Scanning File {0}".format(fileObj.filename))

                    startTime:datetime.datetime = mystring.timestamp.now()
                    output = runner.scan(eph())
                    endTime:datetime.datetime = mystring.timestamp.now()

                    resultObject: RepoResultObject
                    for resultObject in output:
                        resultObject.startDateTime = startTime
                        resultObject.endDateTime = endTime
                        if stage:
                            resultObject.stage=stage
                        logy.send("␀ Starting Sending For Loop")
                        logy.send(resultObject)
                        logy.send("␀ Ending Sending For Loop")

                    logy.send("␂ Ended Scanning File {0}".format(fileObj.filename))
        except Exception as e:
            exceptionString = str(e)

        if notHollow and len(output) == 0:
            output = [RepoResultObject.newEmpty(
                projecttype=fileObj.filename,
                projectname=fileObj.filename,
                projecturl=None,
                qual_name=None,
                tool_name=runner.name(),
                stage=stage,
                ExceptionMsg=exceptionString,
                startDateTime=None,
                endDateTime=None
            )]

        if self.perScan:
            self.perScan()
        return output
