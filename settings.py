import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CONSTANTS_FILE = os.path.join(ROOT_DIR, 'constants', 'GHI forecastng coefficients.xlsx')
TIME_INTERVAL = 60
AVG_COUNT = 10
COUNTER = 75
DB_HOST = "localhost"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "123"
