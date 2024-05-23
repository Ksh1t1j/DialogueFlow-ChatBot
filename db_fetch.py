import mysql.connector
from datetime import datetime
import json

global cnx

# Connect to DB
cnx = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='cornell_abstract'
)

def getLastRecommendation(user_id: int):
    # Create cursor object
    cursor = cnx.cursor()

    # Write a query
    query = ("SELECT rec_idx FROM rec_record WHERE userID = %s AND rec_date = (SELECT MAX(rec_date) FROM rec_record WHERE userID = %s)")

    # Execute query
    cursor.execute(query, (user_id, user_id))
    # Fetch the result 
    result = cursor.fetchone()

    cursor.close()

    if result is not None:
        return result[0]
    else:
        return None
    

def save_to_db(uid: int, idx: list, prompt : str):
    try:
        cursor = cnx.cursor()
        # Define the query to insert a row into the table
        query = ("INSERT INTO rec_record (userID, rec_Date, prompt, rec_idx) "
                "VALUES (%s, %s, %s, %s)")

        # Define the values to insert into the table
        rec_Date = datetime.now()
        rec_idx = json.dumps(idx)

        # Execute the query with the values
        cursor.execute(query, (uid, rec_Date, prompt, rec_idx))

        # Commit the changes to the database
        cnx.commit()

        # Close the cursor
        cursor.close()

        # print("Row insterted successfully!")

        return 1
    except mysql.connector.Error as err:
        print(f"Error inserting row: {err}")

        cnx.rollback()
        return -1
    except Exception as e:
        print(f"An error occured: {e}")

        cnx.rollback()
        return -1