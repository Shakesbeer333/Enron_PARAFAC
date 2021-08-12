import os
import pandas as pd
import re
import pickle
from dateutil import parser as d_parser
from email.parser import Parser
from configparser import ConfigParser

with open(file=os.path.join(os.getcwd(), 'employees.txt'), 
          encoding='utf-8', 
          mode="r") as f:
    employee_txt = f.readlines()

employee_list = []

for line in employee_txt:
    whitespace = re.search(r'\s', line)
    employee = line[0: whitespace.start()]
    employee_list.append(employee)

f.close()

# Email Parsing
#
#
parser = ConfigParser()
parser.read('dev.ini')
dir_ = 'maildir_filter'

email_path = os.path.join(os.getcwd(), dir_)

email_list = []
# r=root, d=directories, f = files
for r, d, f in os.walk(email_path):
    for file in f:
        # Don't consider pickle
        if '.p' in file:
            continue
        if '.' in file:
            email_list.append(os.path.join(r, file))

for index, p in enumerate(email_list):

    with open(p, 'r', encoding='UTF-8', errors='ignore') as f:
        data = f.read()

    email = Parser().parsestr(data)

    # Date
    #
    date = email['date']
    date_time_obj = d_parser.parse(date)

    if date_time_obj.year != 2001:
        os.remove(p)
        continue

    # From
    #
    user_email = email['from']

    user_name_start = re.search('@', user_email)

    if user_name_start:

        user_name = user_email[0: user_name_start.start()]

        # Only consider important employees
        if user_name not in employee_list:
            os.remove(p)

    if index % 10000 == 0:
        print(index)
