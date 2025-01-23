import configparser
import time
import pathlib
from retrying import retry
from arcgis.gis import GIS
import logging


def timeit(method):
    logger = logging.getLogger(__name__)

    def timed(*args, **kw):
        time_start = time.time()
        result = method(*args, **kw)
        time_end = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((time_end - time_start) * 1000)
        else:
            logger.info("%r  %2.2f ms" %
                        (method.__name__, (time_end - time_start) * 1000))
        return result
    return timed

def get_config_parser():
    config_file_path = pathlib.Path(__file__).parent / 'config.ini'
    with open(str(config_file_path)) as file:
        config = configparser.ConfigParser(interpolation=None)
        config.read_file(file)

        return add_config_directories(config)

def add_config_directories(config):
    if not config.has_section('directories'):
        config.add_section('directories')
    config.set('directories', 'storage_dir',
               str(pathlib.Path(__file__).parent / 'storage'))
    config.set('directories', 'log_dir', str(
        pathlib.Path(__file__).parent / 'storage' / 'logs'))
    return config

@retry(wait_fixed=2000, stop_max_attempt_number=2)
def connect_to_gis(url, username, password):
    try:
        return GIS(url, username, password)
    except ConnectionResetError:
        raise