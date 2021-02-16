# This is a sample Python script.
import os
import sys, threading, time
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from tools.site_monitor import SiteMonitor
from tools.data_reader import MonitorDataReader

# Press the green button in the gutter to run the script.
def run_site_monitor():
    r = SiteMonitor()
    r.run()


def run_monitor_reader():
    r = MonitorDataReader()
    r.run()

if __name__ == '__main__':
    if (len(sys.argv) != 1):

        if (sys.argv[1] == 'reader'):
            print('run write data from kafka topics and store to database', sys.argv[1])
            # ToDo periodic run site_reader
            run_monitor_reader()

        elif (sys.argv[1] == 'monitor'):
            print('run monitor site and produce records', sys.argv[1])
            # ToDo periodic run site_writer
            print(time.ctime())
            run_site_monitor()



        else:
            print('Incrorrect param should be in <reader> or <monitor> and <interval>')
    else:
        print('You should choose what to run from <reader> <monitor> and <interval>')


# See PyCharm help at https://www.jetbrains.com/help/pycharm/

