import logging
import os


class Utilities:
    def getIndexCharacter(self, contentPipeline: str, delimiter: str):
        '''
            Return the position of text in the pipeline
        '''
        return contentPipeline.index(delimiter)

    def convertToDictionary(self, lst) -> dict:
        logging.info(f'recieved list : {lst}')
        if len(lst) % 2 != 0:
            logging.error('total elments in array must even')
            return {}
        csDict = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
        return csDict
