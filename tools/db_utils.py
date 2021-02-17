import psycopg2, logging, datetime
from tools import get_config

logging.basicConfig(level=logging.INFO)


def insert_rec(recive_msg):
    conn = None
    try:
        rec_time = datetime.datetime.strptime(recive_msg.cur_time, "%Y-%m-%d %H:%M:%S")
        loger = logging.getLogger('DB Insert')
        conn = get_pg_conn(loger)
        loger.info('Connecting to Database')
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO MONITOR (site_name, response_time, response_code, pattern_text, rec_time) VALUES ( %s, %s, %s, %s, %s);",
            (recive_msg.site, float(recive_msg.resp_time), int(recive_msg.resp_code), recive_msg.patterns, rec_time))
        conn.commit()
    except(Exception, psycopg2.DatabaseError) as err:
        loger.error(err)
    finally:
        if conn is not None:
            cur.close()
            conn.close()
            loger.info('Connection to DB closed')


def insert_offset(group, off_set):
    try:
        loger = logging.getLogger('DB Insert')
        conn = get_pg_conn(loger)
        loger.info('Connecting to Database')
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO CONSUMER_OFFSET (group_id, last_offset ) VALUES ( %s, %s);",
            (group, int(off_set)))
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as err:
        loger.error(err)
    finally:
        if conn is not None:
            cur.close()
            conn.close()
            loger.info('Connection to DB closed')


def get_one_record(conn):
    loger = logging.getLogger("Current")
    try:
        loger.info('-- start connecting --')
        loger.info('Connecting to Database')
        cur = conn.cursor()
        cur.execute('SELECT * from monitor')
        rec = cur.fetchone()
        print('DB one record  ', rec)
        loger.info('-- end connecting --')
    except (Exception, psycopg2.DatabaseError) as err:
        loger.error(err)
    finally:
        if conn is not None:
            cur.close()
            conn.close()
            loger.info('Database connection close')


def get_last_offset(group):
    logger = logging.getLogger('Offset Getter')
    try:
        conn = get_pg_conn(logger)
        cur = conn.cursor()
        cur.execute("SELECT LAST_OFFSET FROM CONSUMER_OFFSET WHERE GROUP_ID = %s ORDER BY LAST_OFFSET DESC", [group])
        rec = cur.fetchone()[0]
        logger.info('Last offset return %s ', rec)
        return rec
    except (Exception, psycopg2.DatabaseError) as err:
        logger.error(err)
    finally:
        cur.close()
        conn.close()
        logger.info('Database Select group finished and connection is closed')


def get_pg_conn(lg):
    db_data = get_config.get_monitor_data().get('db_items')
    # print(db_data)
    connection = psycopg2.connect(host=db_data.get('db_host'), port=db_data.get('db_port'),
                                  database=db_data.get('db_name'), user=db_data.get('db_user_name'),
                                  password=db_data.get('db_password'))
    lg.info('Connecting to Database')
    return connection


def init_db(conn, lg):
    cur = conn.cursor()
    try:
        lg.info('Try to create monitor table if not exists')
        cur.execute(
            'CREATE TABLE IF NOT EXISTS monitor ( site_name varchar (50), response_time decimal (10,2), '
            'response_code smallint , pattern_text varchar(50), rec_time timestamp );')
        conn.commit()
        resp_text = cur.fetchone
        cur = conn.cursor()
        lg.info('Result fetch object from cur %s', resp_text)
        lg.info('Try to create consummer_ofsset')
        cur.execute('CREATE TABLE IF NOT EXISTS CONSUMER_OFFSET ( group_id varchar (50), last_offset bigint );')
        conn.commit()
        res = cur.fetchone
        lg.info('Fetch cur object from created offset %s ', res)
    except(Exception, psycopg2.DatabaseError) as error:
        lg.error(error)
    finally:
        lg.info('Init database execution finished')
        cur.close()

# loger = logging.getLogger('Current')
# loger.info('This is')
# lg = logging.getLogger('Python test')
# con = get_pg_conn(lg)
# init_db(con, lg)
# lg.info('Finish init db writing ')

# Test instert and select
# insert_rec()
# get_one_record(con)
