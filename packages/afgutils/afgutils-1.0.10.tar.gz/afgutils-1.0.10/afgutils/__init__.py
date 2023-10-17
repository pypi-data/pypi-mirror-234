import atexit
from dotenv import load_dotenv as _load_dotenv
from .db import DB, sql
from .email import send_email
from .s3 import save_to_s3, get_from_s3
from .utils import *
from .trandata import *

_load_dotenv()
atexit.register(DB.close_connections)
