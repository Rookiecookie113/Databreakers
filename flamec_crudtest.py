import mysql.connector
from flamec_crud import FlamebackCaterData

# replace with your actual DB credentials
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='bsg_db'
)
cursor = conn.cursor()

q = FlamebackCaterData(cursor, conn)

print(q.get_all_people_cert())
print(q.cnt_cert_person('byp'))

print(q.add_cert_person(2, 7))
conn.commit()

print(q.update_cert(4, 7))
conn.commit()

print(q.delete_cert(4, 7))
conn.commit()

cursor.close()
conn.close()