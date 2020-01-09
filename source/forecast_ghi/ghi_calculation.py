import time

import datetime
from settings import TIME_INTERVAL, AVG_COUNT, COUNTER, START_TIME
from source.db_process.postgres_management import PostgresManage
from utilis.constants import load_constants_y


class ForecastGHI:

    def __init__(self):

        self.db_manage = PostgresManage()
        self.constants = load_constants_y()

    def forecast_y_value_ghi(self):

        x_value = {}
        current_time = START_TIME
        # current_time = datetime.datetime(2019, 9, 1, 11, 50, 0)
        x_value[current_time] = self.db_manage.read_ghi_value(current_time)
        next_time = current_time + datetime.timedelta(hours=0, minutes=TIME_INTERVAL, seconds=0)

        while True:

            temp_x = self.db_manage.read_ghi_value(next_time)

            while temp_x == "":

                time.sleep(1)
                temp_x = self.db_manage.read_ghi_value(date_time=next_time)

            x_value[next_time] = temp_x
            x_value = self.get_average_x_value(x_dict=x_value)
            next_time += datetime.timedelta(hours=0, minutes=TIME_INTERVAL, seconds=0)

    def get_average_x_value(self, x_dict):

        if len(x_dict) < AVG_COUNT:

            return x_dict
        else:

            sum_x = 0
            for x in x_dict.values():

                sum_x += float(x)

            avg_x = sum_x / AVG_COUNT
            self.db_manage.insert_average_x_value(x_val=avg_x, t_stamp=list(x_dict.keys())[-1])
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
            for i in range(1, 13):

                y_value[i] = self.constants[0][i]

                for j, avg_x_key in enumerate(list(avg_x_value)[-COUNTER:]):

                    y_value[i] += self.constants[COUNTER - j][i] * float(avg_x_value[avg_x_key])

            print(y_value)

            self.db_manage.insert_y_value(y_value, end_t_stamp)

            return
