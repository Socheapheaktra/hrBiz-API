from flask import Blueprint, request, jsonify

from models.user import UserModel

from utils.conn import mycursor, mydb
from utils.util import check_email

employee = Blueprint('employee', __name__)

@employee.route('/create', methods=["POST"])
def create_employee():
    if not request.data or not request.is_json:
        response = {
            "status": False,
            "message": "Invalid Data"
        }
        return jsonify(response)

    req = request.get_json()

    if "first_name" not in req or "last_name" not in req or "email" not in req \
            or "password" not in req or "phone" not in req:
        response = {
            "status": False,
            "message": "Invalid Arguments, Incorrect Parameters"
        }
        return jsonify(response)

    if req['email'] == "" or req['password'] == "":
        response = {
            "status": False,
            "message": "Email and Password cannot be empty!"
        }
        return jsonify(response)

    if check_email(req['email']):
        response = {
            "status": False,
            "message": "This email has already been used!"
        }
        return jsonify(response)

    try:
        sql = 'INSERT INTO tblUser(first_name, last_name, email, password, phone) ' \
              'VALUES (%s, %s, %s, %s, %s)'
        values = [req['first_name'], req['last_name'], req['email'], req['password'], req['phone'], ]
        mycursor.execute(sql, values)
    except Exception as err:
        mydb.rollback()
        response = {
            "status": False,
            "message": f"{err}"
        }
        return jsonify(response)
    else:
        mydb.commit()
        response = {
            "status": True,
            "message": "New Employee added!"
        }
        return jsonify(response)
    
@employee.route('/user-detail', methods=['POST'])
def get_user_detail():
    if not request.data or not request.is_json:
        return jsonify({
            "status": False,
            "message": "Invalid Data"
        })
    req = request.get_json()
    if "user_id" not in req:
        return jsonify({
            "status": False,
            "message": "Invalid Arguments"
        })
    try:
        sql = 'SELECT * FROM tblUser ' \
              'WHERE user_id=%s'
        values = [req['user_id'], ]
        mycursor.execute(sql, values)
    except Exception as err:
        return jsonify({
            "status": False,
            "message": f"{err}"
        })
    else:
        user = mycursor.fetchone()
        data = UserModel(
            user_id=user[0],
            role=user[1],
            first_name=user[2],
            last_name=user[3],
            email=user[4],
            password=user[5],
            phone=user[6],
            status=user[7]
        ).to_dict()
        return jsonify({
            "status": True,
            "message": "Success",
            "data": data
        })

@employee.route('/update')
def update_employee():
    if not request.data or not request.is_json:
        return jsonify({
            "status": False,
            "message": "Invalid Data"
        })
    req = request.get_json()
    if "user_id" not in req or "first_name" not in req or "last_name" not in req \
            or "email" not in req or "password" not in req or "phone" not in req:
        return jsonify({
            "status": False,
            "message": "Invalid Arguments"
        })
    try:
        pass
    except Exception as err:
        pass
    else:
        pass

@employee.route('/list-employee', methods=["GET"])
def get_employee_list():
    try:
        sql = 'SELECT tblUser.id,' \
              'tblRole.name,' \
              'tblUser.first_name,' \
              'tblUser.last_name, ' \
              'tblUser.email,' \
              'tblUser.password,' \
              'tblUser.phone,' \
              'tblUser.status ' \
              'FROM tblUser ' \
              'INNER JOIN tblRole ON tblUser.role_id = tblRole.id '
        mycursor.execute(sql)
    except Exception as err:
        response = {
            'status': False,
            'message': f"{err}"
        }
        return jsonify(response)
    else:
        result = mycursor.fetchall()
        data = list()
        for user in result:
            data.append(UserModel(
                user_id=user[0],
                role=user[1],
                first_name=user[2],
                last_name=user[3],
                email=user[4],
                password=user[5],
                phone=user[6],
                status="Active" if user[7] == 1 else "Inactive"
            ).to_dict())
        response = {
            "status": True,
            "message": "Success!",
            "data": data
        }
        return jsonify(response)
