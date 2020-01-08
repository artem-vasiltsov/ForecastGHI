import psycopg2

from settings import DB_HOST, DB_NAME, DB_PASSWORD, DB_USER


class PostgresManage:

    def __init__(self):

        conn = self.__connect_db()
        self.cur = conn.cursor()

    @staticmethod
    def __connect_db():

        conn = psycopg2.connect(host=DB_HOST, user=DB_USER, database=DB_NAME, password=DB_PASSWORD)

        return conn

    def read_ghi_value(self, date_time):

        select_query = "select ghi_solar_irradiance_avg from measurements_v1 where tstamp = %s"
        self.cur.execute(select_query, (date_time,))
        ghi_value = self.cur.fetchall()

        return ghi_value

    def read_average_x_value(self):
        pass

    def create_table(self):
        pass

    def insert_average_x_value(self, x_val, t_stamp):
        pass

    def insert_y_value(self, y_dict, t_stamp):
        pass
