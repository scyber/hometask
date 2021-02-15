# This is a sample Python script.
import os
import sys
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from tools.site_monitor import SiteMonitor
from tools.data_reader import MonitorDataReader



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    if(len(sys.argv) != 1):

        if (sys.argv[1] == 'reader'):
            print('run write data from kafka topics and store to database', sys.argv[1])
            #ToDo periodic run site_reader
            r = MonitorDataReader()
            r.run()

        elif( sys.argv[1] == 'monitor'):
            print('run monitor site and produce records', sys.argv[1])
            #ToDo periodic run site_writer
            r = SiteMonitor()
            r.run()


        else:
            print('Incrorrect param should be in <reader> or <monitor>')
    else:
        print('You should choose what to run from <reader> <monitor>')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
