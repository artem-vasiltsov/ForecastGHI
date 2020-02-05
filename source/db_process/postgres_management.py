import psycopg2

from settings import DB_HOST, DB_NAME, DB_PASSWORD, DB_USER, MEASUREMENT_TABLE_NAME, DB_PORT
from _collections import defaultdict


class PostgresManage:

    def __init__(self):

        self.conn = self.__connect_db()
        self.cur = self.conn.cursor()
        self.__create_table()

    @staticmethod
    def __connect_db():

        conn = psycopg2.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, database=DB_NAME, password=DB_PASSWORD)

        return conn

    def __create_table(self):

        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS public.average_x_value(
                ID SERIAL PRIMARY KEY,
                STATION text NOT NULL, 
                TSTAMP timestamp NOT NULL,
                GHI_10_AVERAGE real NOT NULL
            )
            """
        )

        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS public.y_value(
                ID SERIAL PRIMARY KEY,
                STATION text NOT NULL,
                TSTAMP timestamp NOT NULL,
                y1 real NOT NULL,
                y2 real NOT NULL,
                y3 real NOT NULL,
                y4 real NOT NULL,
                y5 real NOT NULL,
                y6 real NOT NULL,
                y7 real NOT NULL,
                y8 real NOT NULL,
                y9 real NOT NULL,
                y10 real NOT NULL,
                y11 real NOT NULL,
                y12 real NOT NULL
            )
            """
        )

        self.conn.commit()

    def read_ghi_value(self, date_time, station_name):

        select_query = "select ghi_solar_irradiance_avg from {} " \
                       "where tstamp = %s and station_name = %s".format(MEASUREMENT_TABLE_NAME)

        self.cur.execute(select_query, (date_time, station_name,))
        tbl_value = self.cur.fetchone()

        if tbl_value is None:

            ghi_value = 0
        else:
            ghi_value = tbl_value[0]

        return ghi_value

    def read_average_x_value(self):

        avg_x_dict = defaultdict(dict)

        select_query = "select * from average_x_value"
        self.cur.execute(select_query)
        avg_x_records = self.cur.fetchall()

        for row in avg_x_records:

            avg_x_dict[row[2]][row[1]] = row[3]

        return avg_x_dict

    def insert_average_x_value(self, x_val, t_stamp):

        for station in x_val:

            insert_query = """insert into average_x_value (STATION, TSTAMP, GHI_10_AVERAGE) values (%s, %s, %s)"""
            record_insert = (station, t_stamp, x_val[station])
            self.cur.execute(insert_query, record_insert)

            self.conn.commit()

    def insert_y_value(self, y_dict, t_stamp, station):

        insert_query = "insert into y_value (STATION, TSTAMP, y1, y2, y3, y4, y5, y6, y7, y8, y9, y10, y11, y12) " \
                       "values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        record_insert = (station, t_stamp, y_dict[1], y_dict[2], y_dict[3], y_dict[4], y_dict[5], y_dict[6], y_dict[7],
                         y_dict[8], y_dict[9], y_dict[10], y_dict[11], y_dict[12])

        self.cur.execute(insert_query, record_insert)

        self.conn.commit()
