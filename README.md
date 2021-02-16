### This is a test project for running monitoring sites

Before run you should add your sits in the sites.ml file as two examples
Second config data_config.yml provides information about kafka/database postgres settings
This project from beginning was done in docker environment and docker-env configuration with image settings provided
Before run you need install python virtual env and add it to your Pycharm or similar ide
It could be done initially in your home or similar directory

### Prepare virtual env for run

$ mkdir /tmp/task

$ cd /tmp/task

$ virtualenv task_env

$ source task_env/bin/activate

### Next you need add all extra libraries to the project from pip or from ide per request
amqp
appdirs           
asgiref           
autoflake        
billiard          
black             
celery            
certifi           
chardet           
click            
click-didyoumean  
click-plugins     
click-repl       
com2ann           
dataclasses-json  
Django            
django-scheduler  
icalendar         
idna              
isort            
jsons           
kafka-python      
kombu  
libcst  
marshmallow    
marshmallow-enum  
mypy-extensions   
pathspec          
pip              
prompt-toolkit   
psycopg2-binary   
pybetter          
pyemojify        
pyflakes          
Pygments        
python-dateutil   
pytz              
pyupgrade         
PyYAML           
regex             
requests         
setuptools        
shed             
six              
sqlparse         
stringcase        
timeloop        
tokenize-rt       
toml              
typed-ast         
typing-extensions  
typing-inspect    
typish            
urllib3   
vine  
wcwidth  
wheel            

### How to run

python main reader or monitor

