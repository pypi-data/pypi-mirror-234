from email import parser
from typing import Final
import configparser

parser = configparser.ConfigParser()
parser.read('utility/properties.ini')


class DataConnector:
    SNOWFLAKE: Final = 'snowflake'
    REFRACT_FILE: Final = 'refract'


class StrategyType:
    CONDITIONAL: Final = 'conditional'
    NON_CONDITIONAL: Final = 'non_conditional'




