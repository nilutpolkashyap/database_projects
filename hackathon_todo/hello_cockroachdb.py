
import psycopg2 as ps 

conn = ps.connect(database='bank', user='root', sslmode='require', sslrootcert='certs/ca.crt', sslkey='certs/client.root.key', sslcert='certs/client.root.crt', port=26257, host='localhost')

val = 7

# with conn.cursor() as cur:
#     rows = cur.fetchall()
#     print(rows)
#     print(len(rows))
#     temp = rows[1]
#     print(temp)

# with conn.cursor() as cur:
#     cur.execute('upsert into accounts (id, balance) values ({}, 9900)'.format(val))

# conn.commit()

# with conn.cursor() as cur:
#     cur.execute('select id, balance from accounts')
#     rows = cur.fetchall()
#     for row in rows:
#         print([str(cell) for cell in row])

# print(len(rows))

with conn.cursor() as cur:
    cur.execute('select id, balance from accounts')
    rows = cur.fetchall()
    print(rows)
    print(len(rows))
    print(type(rows))
    # print(rows[1][1])
    print("ID : {}, value : {}".format(rows[1][0], rows[1][1]))