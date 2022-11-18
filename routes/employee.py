from flask import Blueprint, request, jsonify
from models.user import UserModel
from utils.conn import mycursor

employee = Blueprint('employee', __name__)

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
