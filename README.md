# This is a test project for running monitoring sites

Before run you should add your sits in the sites.ml file as two examples
Second config data_config.yml provides information about kafka/database postgres settings
This project from beginning was done in docker environment and docker-env configuration with image settings provided
Before run you need install python virtual env and add it to your Pycharm or similar ide
It could be done initially in your home or similar directory

#Prepare virtual env for run

$ mkdir /tmp/task
$ cd /tmp/task
$ virtualenv task_env
$ source task_env/bin/activate

# Next you need add all extra libraries to the project from pip or from ide per request
amqp              5.0.5
appdirs           1.4.4
asgiref           3.3.1
autoflake         1.4
billiard          3.6.3.0
black             20.8b1
celery            5.0.5
certifi           2020.12.5
chardet           4.0.0
click             7.1.2
click-didyoumean  0.0.3
click-plugins     1.1.1
click-repl        0.1.6
com2ann           0.1.1
dataclasses-json  0.5.2
Django            3.1.6
django-scheduler  0.9.3
icalendar         4.0.7
idna              2.10
isort             5.7.0
jsons             1.4.0
kafka-python      2.0.2
kombu             5.0.2
libcst            0.3.17
marshmallow       3.10.0
marshmallow-enum  1.5.1
mypy-extensions   0.4.3
pathspec          0.8.1
pip               21.0.1
prompt-toolkit    3.0.16
psycopg2-binary   2.8.6
pybetter          0.3.6.1
pyemojify         0.2.0
pyflakes          2.2.0
Pygments          2.8.0
python-dateutil   2.8.1
pytz              2021.1
pyupgrade         2.10.0
PyYAML            5.4.1
regex             2020.11.13
requests          2.25.1
setuptools        52.0.0
shed              0.3.2
six               1.15.0
sqlparse          0.4.1
stringcase        1.2.0
timeloop          1.0.2
tokenize-rt       4.1.0
toml              0.10.2
typed-ast         1.4.2
typing-extensions 3.7.4.3
typing-inspect    0.6.0
typish            1.9.1
urllib3           1.26.3
vine              5.0.0
wcwidth           0.2.5
wheel             0.36.2

#How to run
python main reader/monitor

