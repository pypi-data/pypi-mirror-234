#!/opt/thefactory_venv/bin/python

import logging
import socket
import sys
from datetime import datetime
from os import path, makedirs, getenv

import timestring
from dotenv import load_dotenv
from mysql.connector import connect, pooling, Error as MySQLError

"""Holds the master variable names for the factory"""
__version__ = "1.0.3"

if path.exists('/opt/thefactory/credentials/thefactory/.env'):
    load_dotenv('/opt/thefactory/credentials/thefactory/.env')
else:
    load_dotenv()
# load_dotenv()

DB_USERNAME = getenv("DB_USERNAME")
DB_PASSWORD = getenv("DB_PASSWORD")
TRUNC_TABLES = "N"
DB_TESTHOST = "thefactory.mimeanalytics.com"
DB_TESTHOST2 = "testserver.mimeanalytics.com"
DB_LIVEHOST = "localhost" if socket.gethostname() == 'thefactory.mimeanalytics.com' else 'thefactory.mimeanalytics.com'
SMTP_HOST = "thefactory.mimeanalytics.com"
DB_LIVEWEB = "10.0.0.4"
DB_PRODUCTION_HOST = "thefactory.mimeanalytics.com"
LOG_FORMAT = "%(asctime)s.%(msecs)d - %(module)s %(lineno)d:%(levelname)s - %(message)s"
LOGDATEFMT = "%Y-%m-%d %H:%M:%S"
SCHEDULE_PERIOD = 900


def get_key(parent_dict, keys, default=None):
    """Looks inside nested dict to see if a key exists"""
    for key in keys:
        parent_dict = parent_dict.get(key, None)
        if parent_dict is None:
            return default
    return parent_dict


def make_sql(table, fld_dict, ins_type="r"):
    """
    Makes an sql statement from a table name and a list or a dict of fields
    """
    ins = "REPLACE"
    if ins_type == "i":
        ins = "INSERT"
    if isinstance(fld_dict, dict):
        vals = dict.fromkeys(fld_dict)
        columns = "`" + "`, `".join(vals.keys()) + "`"
    else:
        vals = fld_dict
        columns = "`" + "`, `".join(vals) + "`"
    placeholders = ", ".join(["%s"] * len(vals))
    return f"{ins} INTO {table} ( {columns} ) VALUES ( {placeholders} )"


def working_dir(filename):
    """Returns the current path of the running process"""
    return path.abspath(path.dirname(filename))


def setup_logging(log_file_name=None, log_level=logging.INFO):
    log_dir = 'logs/'
    if not path.exists(log_dir):
        makedirs(log_dir)
    if log_file_name is None:
        log_file_name = path.basename(sys.argv[0]).split('.')[0]
    logging.basicConfig(
        filename=f"logs/{log_file_name}.log",
        level=log_level,
        format=LOG_FORMAT,
        datefmt=LOGDATEFMT,
    )
    logger = logging.getLogger()
    return logger


def logging_dir(filename):
    """Returns a 'logs' directory path appended to the current working path.
    If it doesn't exist, it creates it."""
    wkdir = path.abspath(path.dirname(filename))
    log_dir = path.join(wkdir, "logs")
    if not path.exists(log_dir):
        makedirs(log_dir)
    return log_dir


def create_sql_eng(database_name):
    return f"mysql+mysqlconnector://{DB_USERNAME}:{DB_PASSWORD}@{DB_LIVEHOST}/{database_name}"


def safe_str(v, t):
    """Converts to/ensures a value is the desired type"""
    if v is None or v == "":
        return ""
    else:
        if t == "string":
            return v.strip()
        elif t == "int":
            if v in ["false", "False", None]:
                v = 0
            return int(v)
        elif t in ["decimal", "double", "float"]:
            return float(v)
        elif t == "boolean":
            if v:
                return "Y"
            else:
                return "N"
        elif t == "dateTime":
            return f"{timestring.Date(v).date:%Y-%m-%d %H:%M:%S}"

        elif t == "timeStamp":
            return datetime.fromtimestamp(v).strftime("%Y-%m-%d %H:%M:%S")


class DBaseTest:
    def __init__(self):
        self.conn = connect(
            host=DB_TESTHOST,
            user=DB_USERNAME,
            password=DB_PASSWORD,
            database="workshop",
        )
        self.curs = self.conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()


class DBaseLive:
    def __init__(self):
        self.conn = connect(
            host=DB_LIVEHOST,
            user=DB_USERNAME,
            password=DB_PASSWORD,
            database="workshop",
        )
        self.curs = self.conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()


class DBasePool:
    class _ConnectionContext:
        def __init__(self, pool):
            self.pool = pool

        def __enter__(self):
            self.conn = self.pool.get_connection()
            self.curs = self.conn.cursor()
            return self.conn, self.curs

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.curs.close()
            self.conn.close()

    def __init__(self, dbase="workshop"):
        self.pool = pooling.MySQLConnectionPool(
            pool_name="factorypool",
            pool_size=10,
            host=DB_LIVEHOST,
            user=DB_USERNAME,
            password=DB_PASSWORD,
            database=dbase,
        )

    def connection(self):
        return self._ConnectionContext(self.pool)


class DBaseMediaPool:
    def __init__(self, server_ips, db_name='mediaserver', pool_size=10):
        self.pools = {
            ip: pooling.MySQLConnectionPool(
                pool_name=f"mediaserverpool_{ip}",
                pool_size=pool_size,
                host=ip,
                user='thefactory',
                password=DB_PASSWORD,
                database=db_name,
            )
            for ip in server_ips
        }

    def get_pool(self, server_ip):
        return self.pools.get(server_ip)


class DBaseMedia:
    class _ConnectionContext:
        def __init__(self, pool):
            self.pool = pool

        def __enter__(self):
            self.conn = self.pool.get_connection()
            self.curs = self.conn.cursor()
            return self.conn, self.curs

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.curs.close()
            self.conn.close()

    def __init__(self, server_ip, connection_pool, db_name='mediaserver'):
        self.server_ip = server_ip
        self.pool = connection_pool

    def connection(self):
        return self._ConnectionContext(self.pool)

    def ping(self):
        try:
            conn = connect(
                host=self.server_ip,
                user='thefactory',
                password=DB_PASSWORD,
                database='mediaserver'
            )
            conn.close()
            return True
        except MySQLError as err:
            # print(f"Error connecting to DBaseMedia {self.server_ip}: {err}")
            return False


class DBaseWeb:
    def __init__(self):
        self.conn = connect(
            host=DB_LIVEWEB,
            user=DB_USERNAME,
            password=DB_PASSWORD,
            database="wp_laser",
        )
        self.curs = self.conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()


class DBaseLive2:
    def __init__(self):
        self.conn = connect(
            host=DB_LIVEHOST,
            user=DB_USERNAME,
            password=DB_PASSWORD,
            database="workshop",
            use_pure=True,
        )
        self.curs = self.conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()


class DBaseTest2:
    def __init__(self):
        self.conn = connect(
            host=DB_TESTHOST2,
            user=DB_USERNAME,
            password=DB_PASSWORD,
            database="workshop",
            use_pure=True,
        )
        self.curs = self.conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()


def get_logger(name, logfile, level='info'):
    numeric_level = getattr(logging, level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f'Invalid log level: {level}')
    logger = logging.getLogger(name)
    logger.setLevel(numeric_level)  # or whatever level you want

    # Console handler
    if sys.stdout.isatty():
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.DEBUG)  # adjust as needed
        ch.setFormatter(logging.Formatter(LOG_FORMAT, LOGDATEFMT))
        logger.addHandler(ch)

    # File handler
    fh = logging.FileHandler(logfile)
    fh.setLevel(logging.DEBUG)  # adjust as needed
    fh.setFormatter(logging.Formatter(LOG_FORMAT, LOGDATEFMT))
    logger.addHandler(fh)

    return logger
