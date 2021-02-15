import re, json, logging, requests
from tools import get_config
from kafka import KafkaProducer
from datetime import datetime
from tools.data import Message
import threading


def get_producer(lg, data):
    brokers = data.get('brokers').split(',')
    producer = KafkaProducer(bootstrap_servers=brokers,
                             security_protocol=data.get('security_protocol'),
                             ssl_cafile=data.get('ssl_cafile_path'),
                             ssl_certfile=data.get('ssl_certfile_path'),
                             ssl_keyfile=data.get('ssl_keyfile_path'),
                             value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    lg.info('connect to broker %s', brokers)
    lg.info('Producer is connected %s ', producer.bootstrap_connected())
    return producer


def parce_text(text, pattern):
    pat = re.compile(pattern)
    m = re.search(pat, text)
    if m is not None:
        return 'Pattern found'
    else:
        return 'Pattern not found'


def process_sites(self, lg, sites_in):
    """This method gets and parces sites details for kafka"""
    lg.info('Start getting Kafka producer settings')
    conf_data = get_config.get_monitor_data()
    prd = get_producer(lg, conf_data.get('kafka'))
    for site in sites_in:
        url = site.get('url')
        lg.info('try connecting to site %s ', url)
        resp = requests.get(url)
        """Parce Data from response"""
        text = requests.get(url).text
        resp_pattern = parce_text(text, site.get('regexp'))
        msg_cls = Message(url, str(resp.elapsed.microseconds / 10 ** 6), str(resp.status_code), str(resp_pattern),
                          str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        lg.info('Sending message %s', msg_cls)
        topic = conf_data.get('kafka').get('topic')
        prd.send(topic, msg_cls.to_json())
    prd.close()


class SiteMonitor:

    # ToDo just implement something to get from data it could be better it depends on case
    # ToDo create main run meithod with interval monitoring
    def run(self):
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger('Writer logger')
        sites = get_config.get_url_data()
        process_sites(self, logger, sites)


site_mon = SiteMonitor()
site_mon.run()
