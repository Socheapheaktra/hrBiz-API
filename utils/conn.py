import mysql.connector

""" For Vercel hosting """
# mydb = mysql.connector.connect(
#     host="biuiqt9vcr43twewhrqp-mysql.services.clever-cloud.com",
#     user="u3rckg4djongbn4r",
#     password="K8yF3hRh9g3G9eCIC2Xo",
#     database="biuiqt9vcr43twewhrqp",
# )

""" For Local Uses """
mydb = mysql.connector.connect(
    host='localhost',
    user="root",
    password="",
    database="hrdb",
)
""" 
import SQL via CLI (Command Line)
mysql -u <username> -p <database_name> < <database.sql>
"""

mycursor = mydb.cursor()
