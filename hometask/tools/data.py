
import json
from dataclasses import dataclass
from optparse import Option
from unicodedata import decimal

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Message:
    site: str
    resp_time: str
    resp_code: str
    patterns: str
    cur_time: str
