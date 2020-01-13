import os
import datetime

now = datetime.datetime.now()

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CONSTANTS_FILE = os.path.join(ROOT_DIR, 'constants', 'GHI forecastng coefficients.xlsx')

TIME_INTERVAL = 1
AVG_COUNT = 10
COUNTER = 75
START_TIME = datetime.datetime(2019, 9, 1, 11, 50, 0)

DB_HOST = "localhost"
DB_NAME = "postgres"
DB_PORT = "5432"
DB_USER = "postgres"
DB_PASSWORD = "123"
MEASUREMENT_TABLE_NAME = "measurements_v1"
