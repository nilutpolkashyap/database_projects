import psycopg2 as ps
import time
import random
import logging
from argparse import ArgumentParser, RawTextHelpFormatter
from psycopg2.errors import SerializationFailure

table_head = ("ID", "               HACKATHON NAME                  ", "   MODE   ", "  START_DATE  ", "   END_DATE   ", "REGISTERED", " SUBMITTED")
# table_head[1] = table_head[1].center()

conn = ps.connect(database='bank', user='root', sslmode='require', sslrootcert='certs/ca.crt', sslkey='certs/client.root.key', sslcert='certs/client.root.crt', port=26257, host='localhost')

# with conn.cursor() as cur:
#     cur.execute('select id, balance from accounts')
#     rows = cur.fetchall()
#     print(rows)
#     print(len(rows))
#     print(type(rows))
#     # print(rows[1][1])
#     print("ID : {}, value : {}".format(rows[1][0], rows[1][1]))


def create_table(conn):
    with conn.cursor() as cur:
        cur.execute(
            "CREATE TABLE IF NOT EXISTS hackathons (ID int not null PRIMARY KEY, HACKATHON varchar(255) not null, MODE varchar(50) default 'ONLINE', START_DATE varchar(30) default '00-00-0000', END_DATE varchar(30) default '00-00-0000', REGISTERED varchar(20) default 'NO', SUBMITTED varchar(20) default 'NO' )"
        )
        # cur.execute("UPSERT INTO accounts (id, balance) VALUES (1, 1000), (2, 250)")
        logging.debug("create_accounts(): status message: %s", cur.statusmessage)
    conn.commit()

def insert_table(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM hackathons")
        rows = cur.fetchall()
        conn.commit()
        row_num = len(rows)
        cur.execute("INSERT INTO hackathons (ID, HACKATHON) VALUES ({}, 'Hack GT')".format(row_num+1))
        # cur.execute("INSERT INTO hackathons (ID, HACKATHON) VALUES (1, 'Trans-Atlantic Hackathon - INTEL'), (2, 'Penn Apps Hackathon')")
    conn.commit()

def insert_table_full(conn, name, mode, start_date, end_date, registered, submitted):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM hackathons")
        rows = cur.fetchall()
        conn.commit()
        row_num = len(rows)
        cur.execute("UPSERT INTO hackathons (ID, HACKATHON, MODE, START_DATE, END_DATE, REGISTERED, SUBMITTED) VALUES ({}, {}, {}, {}, {}, {}, {})".format((row_num+1), name, mode, start_date, end_date, registered, submitted))
        # cur.execute("INSERT INTO hackathons (ID, HACKATHON) VALUES (1, 'Trans-Atlantic Hackathon - INTEL'), (2, 'Penn Apps Hackathon')")
        # cur.execute("INSERT INTO hackathons (ID, HACKATHON, MODE, START_DATE, END_DATE, REGISTERED, SUBMITTED) VALUES ({}, 'HackRice', 'ONLINE', '17-09-2021', '19-09-2021', 'NO', 'NO')".format((row_num+1)))
    conn.commit()

def update_table(conn, id_num, column, value):
    with conn.cursor() as cur:
        # cur.execute("SELECT * FROM hackathons")
        # rows = cur.fetchall()
        # conn.commit()
        # row_num = len(rows)
        # id_num = 1
        if(column == 1):
            cur.execute("UPDATE hackathons set HACKATHON = '{}' where ID = {}".format(value, id_num))
        elif(column == 2):
            cur.execute("UPDATE hackathons set MODE = '{}' where ID = {}".format(value, id_num))
        elif(column == 3):
            cur.execute("UPDATE hackathons set START_DATE = '{}' where ID = {}".format(value, id_num))
        elif(column == 4):
            cur.execute("UPDATE hackathons set END_DATE = '{}' where ID = {}".format(value, id_num))
        elif(column == 5):
            cur.execute("UPDATE hackathons set REGISTERED = '{}' where ID = {}".format(value, id_num))
        elif(column == 6):
            cur.execute("UPDATE hackathons set SUBMITTED = '{}' where ID = {}".format(value, id_num))

        # cur.execute("UPDATE hackathons set HACKATHON = 'Teachers Hack' where ID = {}".format(id_num))
        # cur.execute("INSERT INTO hackathons (ID, HACKATHON) VALUES (1, 'Trans-Atlantic Hackathon - INTEL'), (2, 'Penn Apps Hackathon')")
    conn.commit()


def drop_table(conn):
    with conn.cursor() as cur:
        cur.execute(
            "drop table hackathons"
        )
        # cur.execute("UPSERT INTO accounts (id, balance) VALUES (1, 1000), (2, 250)")
        logging.debug("drop_table(): status message: %s", cur.statusmessage)
    conn.commit()

def display_table(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM hackathons")
        # logging.debug("print_balances(): status message: %s", cur.statusmessage)
        rows = cur.fetchall()
        conn.commit()
        print("No of rows : {}".format(len(rows)))
        print("-----------------------------------------------------------------------------------------------------------------------------------------")
        print(table_head)
        print("-----------------------------------------------------------------------------------------------------------------------------------------")
        # print(f"Hackathons as of {time.asctime()}:")
        for row in rows:
            l_row = list(row)

            temp = l_row[1]
            l_row[1] = temp.center(50)
            temp = l_row[2]
            l_row[2] = temp.center(10)
            temp = l_row[3]
            l_row[3] = temp.center(14)
            temp = l_row[4]
            l_row[4] = temp.center(14)           
            temp = l_row[5]
            l_row[5] = temp.center(10)
            temp = l_row[6]
            l_row[6] = temp.center(10)

            print(l_row)
            # print("\n")


if __name__ == "__main__":
    create_table(conn)
    # drop_table(conn)
    # insert_table(conn)
    # update_table(conn)
    # display_table(conn)

    print("####################################################")

    print("Welcome to your own TO-DO List to keep track of upcoming Hackathons")
    print("------------------------------------------------------")
    print("Choose an Option from the Menu Below")
    print("####################################################")

    temp = '        1. Display List of hackathons             '
    print("#{}#".format(temp))
    temp = '        2. Enter a new Hackathon entry            '
    print("#{}#".format(temp))
    temp = '        3. Update detail of particular entry      '
    print("#{}#".format(temp))

    choice = int(input("Enter a choice :  "))

    if(choice == 1):
        display_table(conn)
    elif(choice == 2):
        name = input("Enter Hackathon Name :  ")
        mode = input("Enter Mode of Conduct (ONLINE/OFFLINE) :  ")
        start_date = input("Enter Date of Start (DD-MM-YYYY) :  ")
        end_date = input("Enter Date of End (DD-MM-YYYY) :  ")
        registered = input("Have you registered for it :  ")
        submitted = input("have you submitted a project :  ")

        insert_table_full(conn, name, mode, start_date, end_date, registered, submitted)

    elif(choice == 3):
        display_table(conn)
        id_num = int(input("Please enter ID for the entry you want to change :  "))
        print("1. Hackathon  2. Mode  3. Start_date  4. End_date  5. Register status  6.  Submission Status")
        column = int(input("Please enter the column you want to change :  "))
        print(column)
        value = input("Enter the new value :  ")
        print(value)
        update_table(conn, id_num, column, value)
        # update_table(conn)
