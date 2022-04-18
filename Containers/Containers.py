from dependency_injector import containers, providers
from dependency_injector.wiring import Provide

from Features.YamlGenerate import YamlGenerate


class Configs (containers.DeclarativeContainer):
    config = providers.Configuration('config')


class YamlGenerateServices (containers.DeclarativeContainer):
    yamlGenerateServices = providers.Factory(YamlGenerate, Configs.config)
