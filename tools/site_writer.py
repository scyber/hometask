import re, json, logging, requests
from tools import get_config
from kafka import KafkaProducer
from datetime import datetime
from tools.data import Message

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger('Writer logger')


def getProducer(lg, data):
    brokers = data.get('brokers').split(',')
    print(brokers)
    producer = KafkaProducer(bootstrap_servers=brokers,
                             security_protocol=data.get('security_protocol'),
                             ssl_cafile=data.get('ssl_cafile_path'),
                             ssl_certfile=data.get('ssl_certfile_path'),
                             ssl_keyfile=data.get('ssl_keyfile_path'),
                             value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    log_message = 'producer connected ', producer.bootstrap_connected()
    lg.info(log_message)
    return producer


# ToDo just implement something to get from data it could be better it depends on case
def parce_text(text, pattern):
    pat = re.compile(pattern)
    m = re.search(pat, text)
    if m is not None:
        return 'Pattern found'
    else:
        return 'Pattern not found'


def process_sites(lg, sites_in):
    """This method gets and parces sites details for kafka"""
    lg.info('Start getting Kafka producer settings')
    conf_data = get_config.get_monitor_data()
    prd = getProducer(lg, conf_data.get('kafka'))
    for site in sites_in:
        url = site.get('url')
        lg.info('try connecting to site')
        resp = requests.get(url)
        """Parce Data from response"""
        text = requests.get(url).text
        resp_pattern = parce_text(text, site.get('regexp'))
        msg_cls = Message(url, str(resp.elapsed.microseconds / 10 ** 6), str(resp.status_code), str(resp_pattern),
                          str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        msg_cls_info = 'send msg_cls', str(msg_cls)
        lg.info(msg_cls_info)
        topic = conf_data.get('kafka').get('topic')
        prd.send(topic, msg_cls.to_json())
    prd.close()


# ToDo create main run meithod with interval monitoring

sites = get_config.get_url_data()
process_sites(logger, sites)
