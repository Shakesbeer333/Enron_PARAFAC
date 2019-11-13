import os
import pandas as pd
import re
import pickle

path = os.path.join(os.getcwd(), "maildir")

email_list = []
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
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


    # Message ID

    match_start = re.search("Message-ID: <", t)
    match_end = re.search("Message-ID: .*>", t)

    if match_start and match_end:
        df.at[index, "ID"] = t[match_start.end(): match_end.end() - 1]

    # Date

    match_start = re.search("Date: ", t)
    match_end = re.search("Date: .*", t)

    if match_start and match_end:
        df.at[index, "Date"] = t[match_start.end(): match_end.end()]

    # From

    match_start = re.search("From: ", t)
    match_end = re.search("From: .*", t)

    if match_start and match_end:
        df.at[index, "From"] = t[match_start.end(): match_end.end()]

    # Content

    match_start = re.search("X-FileName: .*", t)

    if match_start and match_end:
        df.at[index, "Content"] = t[match_start.end():]

    # Path

    df.at[index, "Path"] = f.split("maildir")[1]

pickle.dump(df, open(path + "/Data_Pickle/e_mails.p", "wb"))

print(df)