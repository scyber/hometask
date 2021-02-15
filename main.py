# This is a sample Python script.
import os
import sys
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.



def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    if(len(sys.argv) != 1):

        if (sys.argv[1] == 'reader'):
            print('run write data from kafka topics and store to database', sys.argv[1])
            #ToDo periodic run site_reader


        elif( sys.argv[1] == 'writer'):
            print('run monitor site and produce records', sys.argv[1])
            #ToDo periodic run site_writer

        else:
            print('Incrorrect param should be in <reader> or <writer>')
    else:
        print('You should choose what to run from <reader> <writer>')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
