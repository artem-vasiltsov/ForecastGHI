import time

import datetime
from settings import TIME_INTERVAL, AVG_COUNT, COUNTER, START_TIME
from source.db_process.postgres_management import PostgresManage
from utilis.constants import load_constants_y
from utilis.date_time import convert_datetime


class ForecastGHI:

    def __init__(self):

        self.db_manage = PostgresManage()
        self.constants = load_constants_y()

    def forecast_y_value_ghi(self):

        x_value = {}

        last_record_time = self.db_manage.read_average_x_value()

        if last_record_time == {}:
            current_time = START_TIME
        else:
            current_time = list(last_record_time)[-1]

        str_dt_time = convert_datetime(current_time)
        x_value[current_time] = self.db_manage.read_ghi_value(str_dt_time)

        cur_index = 0
        while not x_value[current_time]:

            cur_index += 1
            time.sleep(10)
            x_value[current_time] = self.db_manage.read_ghi_value(str_dt_time)
            if cur_index > 9:
                current_time += datetime.timedelta(hours=0, minutes=TIME_INTERVAL, seconds=0)
                str_dt_time = convert_datetime(current_time)
                cur_index = 0

        next_time = current_time + datetime.timedelta(hours=0, minutes=TIME_INTERVAL, seconds=0)

        while True:

            str_next_time = convert_datetime(next_time)
            temp_x = self.db_manage.read_ghi_value(next_time)

            interval_index = 0
            while not temp_x:

                interval_index += 1
                time.sleep(10)
                temp_x = self.db_manage.read_ghi_value(date_time=str_next_time)
                if interval_index > 9:
                    next_time += datetime.timedelta(hours=0, minutes=TIME_INTERVAL, seconds=0)
                    str_next_time = convert_datetime(next_time)
                    interval_index = 0

            x_value[next_time] = temp_x
            x_value = self.get_average_x_value(x_dict=x_value)
            next_time += datetime.timedelta(hours=0, minutes=TIME_INTERVAL, seconds=0)
            # print(x_value)

    def get_average_x_value(self, x_dict):

        if len(x_dict) < AVG_COUNT:

            return x_dict
        else:

            sum_x = 0
            for x in x_dict.values():

                sum_x += float(x[1])

            avg_x = sum_x / AVG_COUNT
            self.db_manage.insert_average_x_value(x_val=avg_x, t_stamp=list(x_dict.keys())[-1],
                                                  station=list(x_dict.values())[-1][0])
            self.get_y_value()

            x_dict.clear()

            return x_dict

    def get_y_value(self):

        avg_x_value = self.db_manage.read_average_x_value()

        if len(avg_x_value) < COUNTER:

            return

        else:

            y_value = {}
            end_t_stamp = list(avg_x_value.keys())[-1]
            station = list(avg_x_value.values())[-1][0]
            for i in range(1, 13):

                y_value[i] = self.constants[0][i]

                for j, avg_x_key in enumerate(list(avg_x_value)[-COUNTER:]):

                    y_value[i] += self.constants[COUNTER - j][i] * float(avg_x_value[avg_x_key][1])
            print("current time:{}".format(end_t_stamp))
            print("Y values:{}".format(y_value))

            self.db_manage.insert_y_value(y_value, end_t_stamp, station=station)

            return
