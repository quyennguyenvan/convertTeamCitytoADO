'''
This class help you can handler the block Params in teamcity pipeline
'''
import logging
from tracemalloc import start

from pandas import offsets
import Features.BlockHelper as blockHelper
import Features.Handlers.Utilities as utilities
import re


class ParamsHandler:

    pushStack = []

    def __init__(self, pipelineContent: str):
        self.pipelineContent = pipelineContent
    '''
        This func help you can detected the block Params of pipeline
    '''

    def paramsDetect(self) -> dict:
        pipelineContent = self.pipelineContent
        offsets = 2

        regexPattern = "[a-zA-Z0-9-_%.:\/]+"

        if blockHelper.params in pipelineContent:

            logging.info(f'Detect the block { blockHelper.params}')

            tool = utilities.Utilities()

            startPosition = tool.getIndexCharacter(
                pipelineContent, blockHelper.params)

            endPosition = pipelineContent.find(blockHelper.closeBlock)

            subStr = pipelineContent[startPosition:endPosition]
            
            subStringFound = re.findall(regexPattern, subStr)

            logging.info(
                f'sub string for  {blockHelper.params}: {subStr}')

            for item in subStringFound:
                if item != blockHelper.params and item != blockHelper.param:
                    self.pushStack.append(item)

            if self.pushStack:
                return tool.convertToDictionary(self.pushStack)
