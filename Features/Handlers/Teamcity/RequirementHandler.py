'''
This class help you can handler the block requirement in teamcity pipeline
'''
import logging
import Features.BlockHelper as blockHelper
import Features.Handlers.Utilities as utilities
import re


class RequirementHandler:

    pushStack = []

    def __init__(self, pipelineContent: str):
        self.pipelineContent = pipelineContent
        self.tools = utilities

    def requirementDetect(self) -> dict:
        pipelineContent = self.pipelineContent

        regexPattern = "[a-zA-Z0-9-_%.: \/]+"

        if blockHelper.requirements in pipelineContent:

            print(f'found  {blockHelper.requirements}')

            logging.info('Detect the block requirement')

            tool = utilities.Utilities()

            startPosition = tool.getIndexOfBlockStarter(
                pipelineContent, blockHelper.requirements)

            endPosition = pipelineContent.find(blockHelper.closeBlock)

            subStr = pipelineContent[startPosition:endPosition+1]

            subStringFound = re.findall(regexPattern, subStr)

            for item in subStringFound:
                if item != blockHelper.requirements:
                    self.pushStack.append(item)
                    print(item)

            if self.pushStack:
                return tool.convertToDictionary(self.pushStack)
