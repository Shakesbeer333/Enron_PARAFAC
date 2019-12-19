import os
import pandas as pd
pd.set_option('display.max_columns', 6)
import re
import pickle
from dateutil import parser
from email.parser import Parser
from configparser import ConfigParser

with open(file= os.path.join(os.getcwd(), 'employees.txt'), encoding="utf-8", mode="r") as f:
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
dir_ = parser.get('Parsing', 'dir_', fallback = 'maildir')

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

df = pd.DataFrame(
    columns=["ID", "Date", "From", "Subject", "Content", "Path"])

for index, p in enumerate(email_list):

    with open(p, 'r', encoding= 'UTF-8', errors = 'ignore') as f:

        data = f.read()

    email = Parser().parsestr(data)

    # Message ID
    #
    df.at[index, "ID"] = email['message-id']

    # From
    #
    user_email = email['from']

    user_name_start = re.search('@', user_email)

    if user_name_start:

        user_name = user_email[0: user_name_start.start()]

        # Only consider important employees
        if user_name in employee_list:
            df.at[index, "From"] = user_name
            pass
        else:
            continue

    else:
        print('No valid E-Mail')


    # Date
    #
    date = email['date']
    date_time_obj = d_parser.parse(date)

        if date_time_obj.year == 2001:
            df.at[index, "Date"] = date
        else:
            df.drop([index], inplace=True)
            continue

    # Subject
    #
    df.at[index, "Subject"] = email['subject']

    # Content
    #
    df.at[index, "Content"] = email.get_payload()

        print(email.get_payload())
        print('-----------------------------------------------------------------')


    # Path
    #
    df.at[index, "Path"] = p.split(dir_)[1]

df.dropna(axis = 0, inplace = True)
df.reset_index(drop = True, inplace = True)

pickle.dump(df, open(email_path + "/Data_Pickle/e_mails.p", "wb"))

