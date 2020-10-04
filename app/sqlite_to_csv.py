import sqlite3 as sql
import os
import csv
from sqlite3 import Error


def exportToCSV(table_name):
    try:

        # Connect to database
        conn=sql.connect('app.db')

        # To view table data in table format
        print("Table data")
        cur = conn.cursor()
        cur.execute('SELECT * FROM ' + table_name)
        rows = cur.fetchall()
        
        for row in rows:
            print(row)

        # Export data into CSV file
        print("Exporting data into CSV")
        cursor = conn.cursor()
        cursor.execute("select * from " + table_name)
        with open('./csv/' + table_name + "_data.csv", "w") as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=",")
            csv_writer.writerow([i[0] for i in cursor.description])
            csv_writer.writerows(cursor)

        dirpath = os.getcwd() + '/csv/' + table_name + "_data.csv"
        print("Data exported Successfully into {}".format(dirpath))

    except Error as e:
        print(e)

    # Close database connection
    finally:
        conn.close()
