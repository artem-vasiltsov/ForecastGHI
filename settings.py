import os
from datetime import datetime

now = datetime.now()

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CONSTANTS_FILE = os.path.join(ROOT_DIR, 'constants', 'GHI forecastng coefficients.xlsx')

TIME_INTERVAL = 1
AVG_COUNT = 2
COUNTER = 20
START_TIME = now

DB_HOST = "localhost"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "123"
MEASUREMENT_TABLE_NAME = "measurements_v1"
