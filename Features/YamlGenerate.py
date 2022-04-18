import logging
from operator import contains
from os import walk
import os
from turtle import position
from numpy import block, number
import yaml
import re
import Features.BlockHelper as blockHelper

import Features.Handlers.Teamcity.BlockProcessFilterHandler as blockBodyFilter
import Features.Handlers.Teamcity.ParamsHandler as paramsHandler
import Features.Handlers.Teamcity.RequirementHandler as requirementHandler
import Features.Handlers.Teamcity.VCSHandler as vcsHandler
import Features.Handlers.Teamcity.StepsHandler as stepHandler


class YamlGenerate(object):
    '''
    This class help you can collections all files inside data input (the teamcity pipeline) and convert it to AzureDevOps pipeline
    '''
    files = []
    specialDirPath = None
    sepecialOurDirPath = None
    adoVariables = {}
    adoRequirement = {}
    adoVCS = {}
    adoJobs = {}

    def __init__(self, config):
        self.config = config
        self.specialDirPath = self.config['DataImportDir']
        self.sepecialOurDirPath = self.config['DataOutputDir']

    def dictListed(self):
        arr = os.listdir(self.specialDirPath)
        self.files.append(arr)
        for item in arr:
            print(item)
            self.fileReading(item)

    def fileReading(self, filePath: str):
        try:
            filePathDir = f'{self.specialDirPath}\\{filePath}'
            fileYamlPathdir = f'{self.sepecialOurDirPath}\\{filePath}.yaml'
            print(f"reading the file: {filePathDir}")
            logging.info(f"read file : {filePathDir}")
            with open(filePathDir) as f:
                lines = f.read().replace("\n", "").strip()
                # regex for remove the lines of space
                lines = re.sub(r"\s+", " ", lines)
                logging.info(f'readed content: {lines}')

                # self.generateYamlFile(fileYamlPathdir)
                _blockBodyFilter = blockBodyFilter.BodypipelineDetect(lines)
                _response = _blockBodyFilter.bodyPipelineResponse()
                if _response:
                    logging.info(
                        'detect the body of the pipeline, process for block detector')
                    self.blockDetectHandler(_response)
                else:
                    logging.info('the pipeline empty the body response')
        except:
            logging.exception(f'can not process for : {filePath}')

    '''
        This func help you detect the block of pipeline
    '''

    def blockDetectHandler(self, bodyContext: str):

        print(f'{blockHelper.params} block detector')
        _blockBodyFilter = blockBodyFilter.BodypipelineDetect()
        _content = _blockBodyFilter.blockSplitResponse(
            bodyContext, blockHelper.params, blockHelper.closeBlock)
        _paramsHandler = paramsHandler.ParamsHandler(_content['subString'])
        self.adoVariables = _paramsHandler.paramsDetect()
        logging.info(f'ado variables: {self.adoVariables}')

        print(f'{blockHelper.vcs} block detector')
        _content = _blockBodyFilter.blockSplitResponse(
            _content['newOrigin'], blockHelper.vcs, blockHelper.closeBlock)
        _vcsHandler = vcsHandler.VCSHandler(_content['subString'])
        self.adoVCS = _vcsHandler.vcstDetect()
        logging.info(f'adoVCS: {self.adoVCS}')

        print(f'{blockHelper.steps} block detector')
        _content = _blockBodyFilter.blockSplitResponse(
            _content['newOrigin'], blockHelper.steps, blockHelper.doubleCloseBlock)
        _stepHandler = stepHandler.StepHandler(_content['subString'])
        self.adoJobs = _stepHandler.stepsDetect()
        logging.info(f'adoJobs: {self.adoJobs}')

        # print('Requirement block detector')
        # _content = _blockBodyFilter.blockSplitResponse(
        #     _content['newOrigin'], blockHelper.requirements, blockHelper.closeBlock)
        # _requirementsHandler = requirementHandler.RequirementHandler(
        #     bodyContext)
        # self.adoRequirement = _requirementsHandler.requirementDetect()

    '''
        This func help you can export the yaml file
    '''

    def generateYamlFile(self, filePathOutDir):

        dict_file = [{'sports': ['soccer', 'football', 'basketball', 'cricket', 'hockey', 'table tennis']},
                     {'countries': ['Pakistan', 'USA', 'India', 'China', 'Germany', 'France', 'Spain']}]

        with open(f'{filePathOutDir}', 'w') as file:
            documents = yaml.dump(dict_file, file)
