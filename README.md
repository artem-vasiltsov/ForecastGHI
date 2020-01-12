# ForecastGHI

## Description

This project is to forecast y value by GHI values gained in real time.

## Installation

    python 3.6
    postgresql 12.0 
    
To install dependencies, run following command in terminal

    pip3 install -r requirements.txt

Note: In Ubuntu 18.04, before installing dependencies, install libpq-dev for psycopg2

    sudo apt install libpq-dev python3-dev 
    
## Configuration

In settings.py, configure various options including database.

Here, TIME_INTERVAL is time interval that GHI values are gained. It's default value is 1 min.

AVG_COUNT is a time that it takes to obtain average value of GHI values. It's default value is 10 minutes.

COUNTER is number of terms necessary for calculating y value. It's value is 75 and don't change it.

## Execution

In terminal, run following command.

    python3 main.py

## Output

Output of this project is two tables in your postgresql database, whose names are average_x_value and y_value.

Table "average_x_value" contains average value of x every 10 minutes. And Table "y_value" contains 12 y_values 
after 75 steps.