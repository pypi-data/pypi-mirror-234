from email import parser
from typing import Final
import configparser

parser = configparser.ConfigParser()
parser.read('utility/properties.ini')

class DataType:
    TABULAR_DATA: Final = "tabular"
    TEXT_DATA: Final = "text"
    IMAGE_DATA: Final = "image"
    VIDEO_DATA: Final = "video"
    AUDIO_DATA: Final = "audio"

class DataConnector:
    SNOWFLAKE: Final = 'snowflake'
    REFRACT_DATASETS: Final ='refract datasets'
    REFRACT_LOCAL_FILES: Final  = 'local data files'
    REFRACT_FILE: Final = 'refract'

class Constants:
    max_row_count=parser['constants']['max_row_count']

