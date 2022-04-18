import logging
import json

from Containers.Containers import Configs, YamlGenerateServices

# init logging
logging.basicConfig(format='%(asctime)s %(process)d %(levelname)s %(name)s %(message)s',
                    level=logging.INFO, filename="log.txt")
logger = logging.getLogger(__name__)
logger.info('Logger init ... OK')

if __name__ == "__main__":

    logger.info('Starting service')

    appConfig = open("appconfigs.json")
    # injection config data
    Configs.config.override(json.load(appConfig))

    yamlServices = YamlGenerateServices.yamlGenerateServices()
    yamlServices.dictListed()
