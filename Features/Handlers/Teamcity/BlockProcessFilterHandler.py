'''
    This class help you can sperate the body of the pipeline
'''
import logging
import Features.Handlers.Utilities as utilities
import Features.BlockHelper as blockHelper


class BodypipelineDetect:

    pipelineContent: str

    def __init__(self, pipelineContent: str = None):
        self.pipelineContent = pipelineContent

    '''
        This func help you detect the location of boy pipeline
    '''

    def bodyPipelineResponse(self) -> str:

        logging.info('body detected for pipeline')

        pipelineContent = self.pipelineContent

        tool = utilities.Utilities()

        startPosition = tool.getIndexCharacter(
            pipelineContent, blockHelper.startObject)

        endPosition = pipelineContent.find(blockHelper.closeObject)

        subStr = pipelineContent[startPosition:endPosition +
                                 (len(pipelineContent) - endPosition)]
        logging.info(f'Detected body pipeline with len: {len(subStr)}')

        return subStr
    '''
        This func help you sperate your block of step in side the pipeline
    '''

    def blockSplitResponse(self, originContent: str, startString: str, closeString: str) -> dict:
        try:
            offset = 2
            logging.info(f'revieced the string: {originContent}')
            logging.info(f'revieced the startString: {startString}')
            logging.info(f'revieced the closeString: {closeString}')

            tool = utilities.Utilities()

            startPosition = tool.getIndexCharacter(originContent, startString)
            logging.info(f'start position: {startPosition}')

            endPosition =originContent.find(closeString)
            logging.info(f'end position: {endPosition}')

            subStr = originContent[startPosition:endPosition +offset]
            logging.info(f'subString of {startString}: {subStr}')

            newContent = originContent.replace(subStr, '')
            logging.info(f'new orgin string : {newContent}')

            dictContent = {}
            dictContent['subString'] = subStr
            dictContent['newOrigin'] = newContent
            return dictContent
        except Exception as e:
            logging.error(f'error: {e}')
