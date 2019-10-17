import os
import pandas as pd
import re

path = os.path.join(os.getcwd(), "maildir")

email_list = []
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        if '.' in file:
            email_list.append(os.path.join(r, file))

# todo Cc und Bcc gibt es nicht immer
df = pd.DataFrame(
    columns=["ID", "Date", "From", "To", "Subject", "Cc", "Mime-Version", "Content-Type", "Content-Transfer-Encoding",
             "Bcc", "Content"])

for index, f in enumerate(email_list[:2]):

    ObjRead = open(f, "r")

    t = ObjRead.read()

    # print(t)

    # Message ID

    match_start = re.search("Message-ID: <", t)
    match_end = re.search("Message-ID: .*>", t)

    if match_start and match_end:
        df.at[index, "ID"] = t[match_start.end(): match_end.end() - 1]

        # todo delete
        print(t[match_start.end(): match_end.end() - 1])

    # Date

    match_start = re.search("Date: ", t)
    match_end = re.search("Date: .*", t)

    if match_start and match_end:
        df.at[index, "Date"] = t[match_start.end(): match_end.end()]

        # todo delete
        print(t[match_start.end(): match_end.end()])

    # From

    match_start = re.search("From: ", t)
    match_end = re.search("From: .*", t)

    if match_start and match_end:
        df.at[index, "From"] = t[match_start.end(): match_end.end()]

        # todo delete
        print(t[match_start.end(): match_end.end()])

    # To

    match_start = re.search("To: ", t)
    match_end = re.search("Subject: .*", t)

    if match_start and match_end:
        df.at[index, "To"] = t[match_start.end(): match_end.start() - 1]

        # todo delete
        print(t[match_start.end(): match_end.start() - 1])

    # Subject

    match_start = re.search("Subject: ", t)
    match_end = re.search("Cc: .*", t)
    match_end_alternative = re.search("Mime-Version: .*", t)

    if match_start and match_end:
        df.at[index, "Subject"] = t[match_start.end(): match_end.start() - 1]

        # todo delete
        print(t[match_start.end(): match_end.start() - 1])

    elif match_start and match_end_alternative:
        df.at[index, "Subject"] = t[match_start.end(): match_end_alternative.start() - 1]

        # todo delete
        print(t[match_start.end(): match_end_alternative.start() - 1])

    # Cc

    match_start = re.search("Cc: ", t)
    match_end = re.search("Mime-Version: .*", t)

    if match_start and match_end:
        df.at[index, "Cc"] = t[match_start.end(): match_end.start() - 1]

        # todo delete
        print(t[match_start.end(): match_end.start() - 1])

    # Mime-Version

    match_start = re.search("Mime-Version: ", t)
    match_end = re.search("Mime-Version: .*", t)

    if match_start and match_end:
        df.at[index, "Mime-Version"] = t[match_start.end(): match_end.end()]

        # todo delete
        print(t[match_start.end(): match_end.end()])

    ObjRead.close()

    # Content-Type

    match_start = re.search("Content-Type: ", t)
    match_end = re.search("Content-Type: .*", t)

    if match_start and match_end:
        df.at[index, "Content-Type"] = t[match_start.end(): match_end.end()]

        # todo delete
        print(t[match_start.end(): match_end.end()])

    # Content-Transfer-Encoding

    match_start = re.search("Content-Transfer-Encoding: ", t)
    match_end = re.search("Content-Transfer-Encoding: .*", t)

    if match_start and match_end:
        df.at[index, "Content-Transfer-Encoding"] = t[match_start.end(): match_end.end()]

        # todo delete
        print(t[match_start.end(): match_end.end()])

    # Bcc

    match_start = re.search("Bcc: ", t)
    match_end = re.search("X-From: .*", t)

    if match_start and match_end:
        df.at[index, "Bcc"] = t[match_start.end(): match_end.start() - 1]

        # todo delete
        print(t[match_start.end(): match_end.start() - 1])

    # Content

    match_start = re.search("X-FileName: .*", t)

    if match_start and match_end:
        df.at[index, "Content"] = t[match_start.end():]

        # todo delete
        print(t[match_start.end():])

    print("")
    print("")

print(df)
