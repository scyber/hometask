import json, logging

from kafka import KafkaConsumer, TopicPartition
from tools import get_config, db_utils
from tools.data import Message


# ToDo just started to implement obt to dataclass
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
                             group_id=data.get('group_id'),
                             enable_auto_commit=True,
                             auto_offset_reset='latest',
                             value_deserializer=lambda v: json.loads(v).encode('utf-8'))
    lg.info('Start susbscribe on topic ')
    #consumer.subscribe(topic)
    return consumer

#ToDo here is a bug that we reed data from the very beggining
#It might be save somewhere in DB or could find better solution of it
def transfer_message(lg):
    conf_data = get_config.get_monitor_data()
    consumer = get_consumer(lg, conf_data.get('kafka'))
    topic_partion = TopicPartition(conf_data.get('kafka').get('topic'), 0)
    consumer.assign([topic_partion])
    consumer.seek_to_end(topic_partion)
    last_offset = consumer.position(topic_partion)
    consumer.seek_to_beginning(topic_partion)
    #consumer.seek_to_end(topic_partion)
    #consumer.poll()
    #consumer.seek_to_end()
    try:
        for msg in consumer:
            print('-- start getting messages ---')
            bytes_msg = msg.value.replace(b"'", b'"')
            obj_msg = Message.from_json(bytes_msg)
            lg.info('Start inserting to DB')
            lg.info(obj_msg)
            db_utils.insert_rec(obj_msg)
            lg.info('Finish inserting to DB')
            if msg.offset == last_offset - 1:
                lg.info('Finish reading last offset %s', last_offset)
                break
    except Exception as ex:
        lg.error(ex.args)
    finally:
        consumer.commit()
        consumer.close(10)


class MonitorDataReader:
    def run(self):
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger('DataReader')
        db_con = db_utils.get_pg_conn(logger)
        db_utils.init_db(db_con, logger)
        transfer_message(logger)


#data_reader = MonitorDataReader()
#data_reader.run()
