'''
This class help you can handler the block requirement in teamcity pipeline
'''
import logging

import Features.BlockHelper as blockHelper
import Features.Handlers.Utilities as utilities
import re


class VCSHandler:

    pushStack = []

    def __init__(self, pipelineContent: str):
        self.pipelineContent = pipelineContent
        self.tools = utilities

    def vcstDetect(self) -> dict:
        pipelineContent = self.pipelineContent

        regexPattern = '[a-zA-Z0-9-_%.: \/*+()" = ]+'

        if blockHelper.vcs in pipelineContent:

            print(f'found {blockHelper.vcs} block and process now')

            logging.info(f'Detect the block : {blockHelper.vcs}')

            tool = utilities.Utilities()

            startPosition = tool.getIndexCharacter(
                pipelineContent, blockHelper.vcs)

            endPosition = pipelineContent.find(blockHelper.closeBlock)

            subStr = pipelineContent[startPosition:endPosition]

            subStringFound = re.findall(regexPattern, subStr)
            logging.info(
                f'sub string for  {blockHelper.vcs}: {subStringFound}')
            for item in subStringFound:
                if (item != blockHelper.vcs):
                    subItem = item.replace('=', '').replace('"', '').split(' ')
                    for words in subItem:
                        if len(words) > 0 and words != blockHelper.vcs and blockHelper.openParenthesis not in words and blockHelper.closeParenthesis not in words:
                            self.pushStack.append(words)

            if self.pushStack:
                return tool.convertToDictionary(self.pushStack)
