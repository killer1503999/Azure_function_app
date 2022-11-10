import datetime
import logging
import pyodbc
import os

import azure.functions as func


def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    query = 'SELECT * FROM [dbo].[expense_api_expensedetails] '
    connection_string = os.getenv("sqlConnectionString")
    conn = pyodbc.connect(connection_string)

    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    print("test completed")

    for row in rows:
        if row.approvedStatus == "Pending" and row.approversComments == "RequiresApproval":
            cursor.execute(
                "update [dbo].[expense_api_expensedetails] set approvedStatus=? where id=?", "Rejected", row.id)
            cursor.execute(
                "update [dbo].[expense_api_expensedetails] set approversComments=? where id=?", "Rejected due to timer trigger at "+str(datetime.datetime.utcnow()), row.id)
    cursor.commit()

    logging.info(
        'Python timer trigger for daily cleanup function ran at %s', utc_timestamp)
