import json, logging

from kafka import KafkaConsumer, TopicPartition
from tools import get_config, db_utils
from tools.data import Message


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
                             auto_commit_interval_ms=100,
                             enable_auto_commit=True,
                             auto_offset_reset='latest',
                             value_deserializer=lambda v: json.loads(v).encode('utf-8'))
    lg.info('Start susbscribe on topic ')
    # consumer.subscribe(topic)
    return consumer


def transfer_message(lg):
    """First get last offset from DB table CONSUMER_OFFSET"""

    conf_data = get_config.get_monitor_data()
    group = conf_data.get('kafka').get('group_id')
    db_offset = db_utils.get_last_offset(group)
    consumer = get_consumer(lg, conf_data.get('kafka'))
    topic_partition = TopicPartition(conf_data.get('kafka').get('topic'), 0)
    lg.info('topic partition value %s', topic_partition)
    consumer.assign([topic_partition])
    last_offset = consumer.end_offsets([topic_partition])[topic_partition]
    lg.info('last offset messages %s', last_offset)
    if db_offset is None:
        consumer.seek_to_beginning(topic_partition)
    else:
        consumer.seek(topic_partition, db_offset)
    try:
        for msg in consumer:
            lg.info("current message offset %s ", msg.offset)
            print('-- start getting messages ---')
            lg.info('Message offset %s Last offset %s', msg.offset, last_offset)
            bytes_msg = msg.value.replace(b"'", b'"')
            obj_msg = Message.from_json(bytes_msg)
            lg.info('Start inserting to DB')
            lg.info(obj_msg)
            db_utils.insert_rec(obj_msg)
            lg.info('topic partition value %s', topic_partition)
            if msg.offset >= last_offset -1:
                #
                lg.info('Finish reading last offset %s', last_offset)
                db_utils.insert_offset(group, msg.offset)
                lg.info('msg offset value %s ', msg.offset)
                break

    except Exception as ex:
        consumer.commit()
        consumer.close()
        lg.error(ex.args)
    finally:
        lg.info('Finish connection')
        consumer.commit()
        consumer.close()


class MonitorDataReader:
    def run(self):
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger('DataReader')
        try:
            db_con = db_utils.get_pg_conn(logger)
            db_utils.init_db(db_con, logger)
            transfer_message(logger)
        except Exception as e:
            logger.error("There is an error %s ", e.with_traceback())
