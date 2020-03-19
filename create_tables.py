import sqlite3

conn = sqlite3.connect('booking_details.sqlite')

c = conn.cursor()
c.execute('''
          CREATE TABLE delivery_details
          (id INTEGER PRIMARY KEY ASC, 
           customer_id VARCHAR(250) NOT NULL,
           delivery_id VARCHAR(250) NOT NULL,
           pickup VARCHAR(250) NOT NULL,
           destination VARCHAR(250) NOT NULL,
           delivery_weight_in_pounds INTEGER NOT NULL,
           delivery_dimensions_in_feet VARCHAR(250) NOT NULL,
           timestamp VARCHAR(100) NOT NULL,
           date_created VARCHAR(100) NOT NULL)
          ''')

c.execute('''
          CREATE TABLE freight_assignment
          (id INTEGER PRIMARY KEY ASC, 
           freight_company VARCHAR(250) NOT NULL,
           freight_id VARCHAR(250) NOT NULL,
           freight_type_in_feet INTEGER NOT NULL,
           max_weight_in_pounds INTEGER NOT NULL,
           freight_load VARCHAR(250) NOT NULL,
           timestamp VARCHAR(100) NOT NULL,
           date_created VARCHAR(100) NOT NULL)
          ''')

conn.commit()
conn.close()
