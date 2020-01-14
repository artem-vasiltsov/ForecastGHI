import time

import datetime
from settings import TIME_INTERVAL, AVG_COUNT, COUNTER, START_TIME, STATIONS
from source.db_process.postgres_management import PostgresManage
from utilis.constants import load_constants_y
from utilis.date_time import convert_datetime


class ForecastGHI:

    def __init__(self):

        self.db_manage = PostgresManage()
        self.constants = load_constants_y()

    def extract_station_ghi_value(self, dt_time):

        station_value = {}
        for station in STATIONS:
            station_value[station] = self.db_manage.read_ghi_value(date_time=dt_time, station_name=station)

        return station_value

    def extract_time_ghi_value(self, dt_time):

        time_value = self.extract_station_ghi_value(dt_time=dt_time)
        str_dt_time = convert_datetime(dt_time)

        cur_index = 0
        while not any(time_value.values()):

            cur_index += 1
            time.sleep(10)
            time_value = self.extract_station_ghi_value(dt_time=dt_time)
            if cur_index > 9:
                break

        return time_value, str_dt_time

    def forecast_y_value_ghi(self):

        x_value = {}

        last_record_time = self.db_manage.read_average_x_value()

        if last_record_time == {}:
            current_time = START_TIME
        else:
            current_time = list(last_record_time.keys())[-1] + \
                           datetime.timedelta(hours=0, minutes=TIME_INTERVAL, seconds=0)

        st_ghi_value, str_dt_time = self.extract_time_ghi_value(dt_time=current_time)
        x_value[str_dt_time] = st_ghi_value

        next_time = current_time + datetime.timedelta(hours=0, minutes=TIME_INTERVAL, seconds=0)

        while True:
            temp_x, str_next_time = self.extract_time_ghi_value(dt_time=next_time)

            x_value[str_next_time] = temp_x
            x_value = self.get_average_x_value(x_dict=x_value)
            next_time += datetime.timedelta(hours=0, minutes=TIME_INTERVAL, seconds=0)
            # print(x_value)

    def get_average_x_value(self, x_dict):

        avg_x = {}
        sum_x = {}
        if len(x_dict) < AVG_COUNT:

            return x_dict
        else:

            for station in STATIONS:
                sum_x[station] = 0

            for x in x_dict:

                for station_term in x_dict[x]:
                    sum_x[station_term] += float(x_dict[x][station_term])

            for y in sum_x:
                avg_x[y] = sum_x[y] / AVG_COUNT

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
            for station_term in STATIONS:

                for i in range(1, 13):

                    y_value[i] = self.constants[0][i]

                    for j, avg_x_key in enumerate(list(avg_x_value)[-COUNTER:]):
                        y_value[i] += self.constants[COUNTER - j][i] * \
                                      float(avg_x_value[avg_x_key][station_term])

                print("station:{}".format(station_term))
                print("current time:{}".format(end_t_stamp))
                print("Y values:{}".format(y_value))

                self.db_manage.insert_y_value(y_dict=y_value, t_stamp=end_t_stamp, station=station_term)

            return
