import psycopg2 as ps
import time
import random
import logging
from argparse import ArgumentParser, RawTextHelpFormatter
from psycopg2.errors import SerializationFailure

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

def update_table(conn):
    with conn.cursor() as cur:
        # cur.execute("SELECT * FROM hackathons")
        # rows = cur.fetchall()
        # conn.commit()
        # row_num = len(rows)
        id_num = 2
        cur.execute("UPDATE hackathons set START_DATE = '10-09-2021' where ID = {}".format(id_num))
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
        print(f"Hackathons as of {time.asctime()}:")
        for row in rows:
            l_row = list(row)
            temp = l_row[1]
            l_row[1] = temp.center(45)
            # row[1] = temp.center(30)
            # row[1] = (row[1]).center(30)
            print(l_row)
            # print("\n")


if __name__ == "__main__":
    create_table(conn)
    # drop_table(conn)
    # insert_table(conn)
    update_table(conn)
    display_table(conn)