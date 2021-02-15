import yaml, logging

loger = logging.getLogger('Yaml logger')


def get_monitor_data():
    """This method gets data from yml infrastructure kafka, database ets"""
    try:
        with open('config/data_config.yml') as data_file:
            mon_data = yaml.load(data_file, Loader=yaml.FullLoader)
            loger.info('data for configs successfully loaded')
            return mon_data
    except Exception as ex:
        loger.error(ex.args)
        print(ex.args)


def get_url_data():
    """This method gets data from yml file for sites to be requested from monitoring"""
    try:
        with open('config/sites.yml') as sites_file:
            url_data = yaml.load(sites_file, Loader=yaml.FullLoader)
            loger.info('data for url successfully loader')
            return url_data
    except Exception as ex:
        loger.error(ex.args)
