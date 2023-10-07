import asyncio, threading, mystring as mys
from typing import List, Dict, Union
from datetime import datetime
from ephfile import ephfile
from pnostic.structure import RepoObject, RepoResultObject, RepoObjectProvider, Runner, LoggerSet, Logger
import type_enforced

async def perRunnerDoubleRunCorrect(repoFiles: RepoObjectProvider, runners:List[Runner], loggersset:List[Logger]):
    print("Entered")
    loggers:LoggerSet = LoggerSet()
    for x in loggersset:
        await loggers.add(x)

    waiting = lambda:True
    print("Prepped Globally")
    for runnerSvr in runners:
        print("Runner {0}".format(runnerSvr.name))
        runnerSvr.initialize()
        await loggers.__enter__("Runner {0}".format(runnerSvr.name))
        await loggers.send("Runner {0}".format(runnerSvr.name))
        for fileObj in repoFiles.files:
            print("File {0}".format(fileObj.filename))

            await loggers.send(fileObj)

            firstScanResults: List[RepoResultObject] = None
            print("Pre Scan")
            firstScanResults = await perFile(fileObj, runnerSvr, loggersset)
            await loggers.send("Got the 1st results from file {0}".format(fileObj.filename))
            for x in firstScanResults:
                await loggers.send(x)
            print("Post Scan")

            vulnRepoResults:List[RepoResultObject] = [x for x in firstScanResults if x.IsVuln]
            await loggers.send("Has a vulnerability? : {0}".format(len(vulnRepoResults) > 0))

            if len(vulnRepoResults) > 0:
                print("Second Scan")
                secondScanResults: List[RepoResultObject] = None

                fileObj.content = vulnRepoResults[0].correctedCode
                print("Pre Scan")
                secondScanResults = await perFile(fileObj, runnerSvr, loggersset)
                for x in secondScanResults:
                    await loggers.send(x)
                await loggers.send("Got the 2nd results from file {0}".format(fileObj.filename))
                print("Post Scan")

                vulnRepoResultsTwo:List[RepoResultObject] = [x for x in secondScanResults if x.IsVuln]
                await loggers.send("Has a vulnerability? : {0}".format(len(vulnRepoResultsTwo) > 0))

            await loggers.send("Running the waiter")
            print("Running the waiter")
            waiting()

        await loggers.__exit__(None,None,None)
        print("Exiting")
        runnerSvr.clean()


async def perFile(fileObj:RepoObject, runner:Runner, loggersset:List[Logger])-> List[RepoResultObject]:
    loggers:LoggerSet = LoggerSet()
    for x in loggersset:
        await loggers.add(x)

    output:List[RepoResultObject] = []
    await loggers.__enter__("Scanning {0} with {1}".format(fileObj.filename, runner.name()))
    with ephfile("{0}_stub.py".format(runner.name()), fileObj.content) as eph:
        await loggers.send("Started Scanning File {0}".format(fileObj.filename))

        startTime:datetime.datetime = datetime.now().astimezone().isoformat()
        output = await runner.scan(eph())
        endTime:datetime.datetime = datetime.now().astimezone().isoformat()

        resultObject: RepoResultObject
        for resultObject in RepoResultObject:
            resultObject.startDateTime = startTime
            resultObject.endDateTime = endTime
            await loggers.send(resultObject)

        await loggers.send("Ended Scanning File {0}".format(fileObj.filename))
    await loggers.__exit__(None,None,None)
    return output