import time

from datetime import datetime
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
        x_value[current_time] = self.db_manage.read_ghi_value(current_time)

        while True:

            next_time = current_time + datetime.timedelta(hours=0, minutes=TIME_INTERVAL, seconds=0)
            temp_x = self.db_manage.read_ghi_value(next_time)

            while temp_x == "":

                time.sleep(10)
                temp_x = self.db_manage.read_ghi_value(date_time=next_time)

            x_value[next_time] = temp_x
            x_value = self.get_average_x_value(x_dict=x_value)

        print(current_time)

    def get_average_x_value(self, x_dict):

        if len(x_dict) < AVG_COUNT:

            return x_dict
        else:

            sum_x = 0
            for x in x_dict.values():

                sum_x += int(x)

            avg_x = sum_x / AVG_COUNT
            self.db_manage.insert_average_x_value(x_val=avg_x, t_stamp=x_dict.keys()[-1])
            self.get_y_value()

            x_dict.clear()

            return x_dict

    def get_y_value(self):

        avg_x_value = self.db_manage.read_average_x_value()

        if len(avg_x_value) < COUNTER:

            return

        else:

            y_value = {}
            end_t_stamp = avg_x_value.keys()[-1]
            st_t_stamp = end_t_stamp - datetime.timedelta(hours=0, minutes=(COUNTER * AVG_COUNT), seconds=0)
            for i in range(1, 13):

                y_value[i] = self.constants[0][i]

                for j, avg_x in enumerate(avg_x_value[st_t_stamp:end_t_stamp].values()):

                    y_value[i] += self.constants[j + 1][i] * int(avg_x)

            self.db_manage.insert_y_value(y_value, end_t_stamp)

            return
