import logging
import json
import logging
import os
import pyodbc
import struct
import azure.functions as func
import datetime


def main(msg: func.QueueMessage):
    logging.info('Python queue trigger function processed a queue item.')
    query = 'SELECT TOP (1000) * FROM [dbo].[expense_api_expensedetails] where id=' + str(
        msg.get_body().decode('utf-8'))

    connection_string = os.getenv("sqlConnectionString")
    d1 = datetime.datetime(2000, 1, 31, 00, 00, 00) - \
        datetime.datetime(2000, 1, 1, 00, 00, 00)

    conn = pyodbc.connect(connection_string)

    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()

    for row in rows:
        current_time = datetime.datetime.now()

        if row.approvedStatus == "Pending" and row.approversComments != "RequiresApproval" and (abs(row.date-current_time) > d1) or current_time-row.date != abs(row.date-current_time):
            cursor.execute(
                "update [dbo].[expense_api_expensedetails] set approvedStatus=?  where id=?", "Rejected", row.id)
            cursor.execute(
                "update [dbo].[expense_api_expensedetails] set approversComments=? where id=?", "Rejected", row.id)
        elif row.approvedStatus == "Pending" and row.amount <= 500 and abs(row.date-current_time) < d1:
            cursor.execute(
                "update [dbo].[expense_api_expensedetails] set approvedStatus=? where id=?", "Accepted", row.id)
            cursor.execute(
                "update [dbo].[expense_api_expensedetails] set approversComments=? where id=?", "Accepted", row.id)
        else:
            cursor.execute(
                "update [dbo].[expense_api_expensedetails] set approversComments=? where id=?", "RequiresApproval", row.id)

    cursor.commit()

    result = json.dumps({
        'id': msg.id,
        'body': msg.get_body().decode('utf-8'),
        'dequeue_count': msg.dequeue_count
    })

    logging.info(result)
