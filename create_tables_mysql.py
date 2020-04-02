import mysql.connector

db_conn = mysql.connector.connect(host="ec2-54-203-161-163.us-west-2.compute.amazonaws.com", user="root",
                                  password="password", database="events")

db_cursor = db_conn.cursor()

db_cursor.execute('''
          CREATE TABLE delivery_details
          (id INT NOT NULL AUTO_INCREMENT, 
           customer_id VARCHAR(250) NOT NULL,
           delivery_id VARCHAR(250) NOT NULL,
           pickup VARCHAR(250) NOT NULL,
           destination VARCHAR(250) NOT NULL,
           delivery_weight_in_pounds INT NOT NULL,
           delivery_dimensions_in_feet VARCHAR(250) NOT NULL,
           timestamp VARCHAR(100) NOT NULL,
           date_created VARCHAR(100) NOT NULL,
           CONSTRAINT delivery_details_pk PRIMARY KEY (id))
          ''')

db_cursor.execute('''
          CREATE TABLE freight_assignment
          (id INT NOT NULL AUTO_INCREMENT, 
           freight_company VARCHAR(250) NOT NULL,
           freight_id VARCHAR(250) NOT NULL,
           freight_type_in_feet INT NOT NULL,
           max_weight_in_pounds INT NOT NULL,
           freight_load VARCHAR(250) NOT NULL,
           timestamp VARCHAR(100) NOT NULL,
           date_created VARCHAR(100) NOT NULL,
           CONSTRAINT freight_assignment_pk PRIMARY KEY(id))
          ''')

db_conn.commit()
db_conn.close()
