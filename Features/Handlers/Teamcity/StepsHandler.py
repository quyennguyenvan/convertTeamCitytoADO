'''
This class help you can handler the block steps in teamcity pipeline
'''
from json import tool
import logging

from numpy import array
import Features.BlockHelper as blockHelper
import Features.Handlers.Utilities as utilities
import Features.Handlers.Teamcity.BlockProcessFilterHandler as blockFilterHandler
import re


class StepHandler:

    adoJobs = {}
    pushStack = []

    def __init__(self, pipelineContent: str):
        self.pipelineContent = pipelineContent
        self.tools = utilities

    def stepsDetect(self) -> dict:
        pipelineContent = self.pipelineContent
        print(pipelineContent)
        logging.info(f'recieved the substring: {pipelineContent}')

        regexPattern = "[a-zA-Z0-9%.\s_\/*]+"

        if blockHelper.steps in pipelineContent:

            print(f'found  {blockHelper.steps}')

            logging.info(f'Detect the block {blockHelper.steps}')

            tool = utilities.Utilities()

            startPosition = tool.getIndexCharacter(
                pipelineContent, blockHelper.steps)

            endPosition = pipelineContent.find(blockHelper.doubleCloseBlock)

            subStr = pipelineContent[startPosition:endPosition]

            subStringFound = re.findall(regexPattern, subStr)

            logging.info(f'sub string detected: {subStringFound}')

            if len(subStringFound) != 0:
                self.jobDetect(subStringFound)

            return {}

    def jobDetect(self, stepsContent: str) -> dict:

        jobLists: dict = {}

        logging.info(f'step list: {stepsContent}')

        tool = utilities.Utilities()

        for item in stepsContent:
            jobName: str = None

            if item.strip() == blockHelper.steps:
                continue

            if item.strip() in blockHelper.stepsList:
                jobName = item.strip()

                jobLists[jobName] = tool.convertToDictionary(self.pushStack)

                self.pushStack = []

                logging.info(f'stack job: { jobLists[jobName]}')

                continue

            if len(item.strip()) != 0:
                self.pushStack.append(item.strip())
