
import json
import logging
from tools.data import Message
from kafka import KafkaConsumer
from tools import db_utils, get_config

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger('Consumer')

#ToDo just started to implement obt to dataclass
def obj_decoder(obj):
    if '__type__' in obj == obj['__type__'] == 'Message':
        return Message(obj['site'], obj['resp_time'], obj['resp_code'], obj['patterns'], obj['cur_time'])
    return obj


def get_consumer(lg, data):
    print('-- staring consumer build --')
    topic = data.get('topic')
    brokers = data.get('brokers').split(',')
    consumer = KafkaConsumer(bootstrap_servers=brokers,
                             security_protocol=data.get('security_protocol'),
                             ssl_cafile=data.get('ssl_cafile_path'),
                             ssl_certfile=data.get('ssl_certfile_path'),
                             ssl_keyfile=data.get('ssl_keyfile_path'),
                             value_deserializer=lambda v: json.loads(v).encode('utf-8'))
    lg.info('Start susbscribe on topic ')
    consumer.subscribe(topic)
    return consumer


def transfer_message(lg):
    conf_data = get_config.get_monitor_data()
    consumer = get_consumer(lg, conf_data.get('kafka'))

    # ToDo parce messages and write to DB
    try:
        for msg in consumer:
            print('-- start getting messages ---')
            bytes_msg = msg.value.replace(b"'", b'"')
            obj_msg = Message.from_json(bytes_msg)

            lg.info('Start inserting to DB')
            lg.info(obj_msg)
            db_utils.insert_rec(obj_msg)
            lg.info('Finish inserting to DB')

    except Exception as er:
        lg.error(er.with_traceback())
    finally:
        consumer.close()

#ToDo check if target database exists and create a table
db_con = db_utils.get_pg_conn(logger)
db_utils.init_db(db_con, logger)
transfer_message(logger)


