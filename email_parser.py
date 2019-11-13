import os
import pandas as pd
import re
import pickle
from dateutil import parser


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
#path = os.path.join(os.getcwd(), "maildir")
## Testing path
#
email_path = os.path.join(os.getcwd(), 'subfolder_email')

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
    columns=["ID", "Date", "From", "Content", "Path"])

for index, f in enumerate(email_list):

    try:
        t = open(file=f, encoding="utf-8", mode="r").read()
    except UnicodeDecodeError:
        print(f)
        # t = open(file = f, encoding="utf-16", mode="r").read()

    # From

    match_start = re.search("From: ", t)
    match_end = re.search("From: .*", t)

    if match_start and match_end:

        # Option 1: Consider just within-Enron communication --> @enron
        # Option 2: Consider entire communication

        user_email = t[match_start.end(): match_end.end()]

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

    # Message ID

    match_start = re.search("Message-ID: <", t)
    match_end = re.search("Message-ID: .*>", t)

    if match_start and match_end:
        df.at[index, "ID"] = t[match_start.end(): match_end.end() - 1]


    # Date

    match_start = re.search("Date: ", t)
    match_end = re.search("Date: .*", t)

    if match_start and match_end:
        date = t[match_start.end(): match_end.end()]
        date_time_obj = parser.parse(date)

        if date_time_obj.year == 2001:
            df.at[index, "Date"] = date
        else:
            df.drop([index], inplace = True)
            continue

    # Content

    match_start = re.search("X-FileName: .*", t)

    if match_start and match_end:
        df.at[index, "Content"] = t[match_start.end():]

    # Path

    #df.at[index, "Path"] = f.split('maildir')[1]
    df.at[index, "Path"] = f.split('subfolder_email')[1]



pickle.dump(df, open(email_path + "/Data_Pickle/e_mails.p", "wb"))

print(df)