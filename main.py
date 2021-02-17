# This is a sample Python script.
import sys, time, schedule, logging
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from tasks.site_monitor import SiteMonitor
from tasks.data_reader import MonitorDataReader
import tools.get_config

# Press the green button in the gutter to run the script.
from tools import get_config


def run_site_monitor():
    logger = logging.getLogger('Monitor Running')
    r = SiteMonitor()
    logger.info('Start run monitoring %s', time.ctime())
    r.run()
    logger.info('Finish run monitoring %s ', time.ctime())


def job_shedule_monitor(job_name):
    conf_data = get_config.get_monitor_data()
    minutes = conf_data.get('run_params').get('minutes')
    sh = schedule.Scheduler()
    sh.every(minutes).minutes.do(job_name)
    while True:
        sh.run_pending()
        time.sleep(1)


def run_monitor_reader():
    r = MonitorDataReader()
    r.run()


if __name__ == '__main__':
    if len(sys.argv) != 1:

        if sys.argv[1] == 'reader':
            print('run write data from kafka topics and store to database', sys.argv[1])
            job_shedule_monitor(run_monitor_reader)
            #run_monitor_reader()

        elif sys.argv[1] == 'monitor':
            print('run monitor site and produce records', sys.argv[1])
            print('Start running monitor sites', time.ctime())
            job_shedule_monitor(run_site_monitor)

        else:
            print('Incrorrect param should be in <reader> or <monitor> and <interval>')
    else:
        print('You should choose what to run from <reader> <monitor> and <interval>')


