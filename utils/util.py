from utils.conn import mycursor

# TODO: add functions for checking for duplicated email
def check_email(email):
    try:
        sql = 'SELECT * FROM tblUser ' \
              'WHERE email=%s'
        values = [email, ]
        mycursor.execute(sql, values)
    except Exception as err:
        return False
    else:
        result = mycursor.fetchall()
        if result: # If result exist
            return True
        else:
            return False
