import sqlite3

conn = sqlite3.connect('booking_details.sqlite')

c = conn.cursor()
c.execute('''
          DROP TABLE delivery_details
          ''')

c.execute('''
          DROP TABLE freight_assignment
          ''')

conn.commit()
conn.close()
