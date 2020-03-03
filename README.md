# ForecastGHI

## Overview

This project is to forecast y value by GHI values gained in real time.

## Installation

- Environment
    Ubuntu 18.04, python 3.6 postgresql 12.0 
    
- To install dependencies, run following command in terminal

    ```
        pip3 install -r requirements.txt
    ```    

- Note: In Ubuntu 18.04, before installing dependencies, install libpq-dev for psycopg2

    ```
        sudo apt install libpq-dev python3-dev
    ```        
    
## Configuration

In settings.py, configure various options including database settings.

- Here, TIME_INTERVAL is time interval that GHI values are gained. It's default value is 1 min.

- AVG_COUNT is a time that it takes to obtain average value of GHI values. It's default value is 10 minutes.

- COUNTER is number of terms necessary for calculating y value. It's value is 75 and can be changed manually, but must
be less than 76.

- Also START_TIME can be configured, that can be easily changed by year, month, day, hour, minute as you like.
But at this point, second, where is set as 0, can never be changed as long as tstamp field of measurement table doesn't 
change.

- DELAY_TIME shows the max time that it takes for each station to get the GHI value and send it to the server. It's 
default value is 30 min.

- BASE_SOLAR_ANGLES is the threshold value for y1_corrected. If the value of solar angle is greater than this threshold
value for each measurement time, the value of y1_corrected is equal to the value of y1, else 0. It's default value is 80.

## Execution

- In terminal, run the following command.

    ```
        python3 main.py
    ``` 

## Output

Output of this project is two tables in your postgresql database, whose names are average_x_value and y_value.

Table "average_x_value" contains average value of x every 10 minutes. And Table "y_value" contains 12 y_values 
after 75 steps.