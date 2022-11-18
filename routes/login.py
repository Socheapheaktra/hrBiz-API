from flask import Blueprint, request, jsonify
from utils.conn import mycursor
from models.user import UserModel

login = Blueprint('login', __name__)
@login.route("/validate", methods=['POST'])
def validate_user():
    if not request.data or not request.is_json:
        response = {
            "status": False,
            "message": "Invalid Data"
        }
        return jsonify(response)
    req = request.get_json()
    if "email" not in req or "password" not in req:
        response = {
            "status": False,
            "message": "Invalid Arguments. Incorrect Parameter"
        }
        return jsonify(response)
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
              'INNER JOIN tblRole ON tblUser.role_id = tblRole.id ' \
              'WHERE email=%s AND password=%s'
        values = [req['email'], req['password'], ]
        mycursor.execute(sql, values)
    except Exception as err:
        response = {
            "status": False,
            "message": f"{err}"
        }
        return jsonify(response)
    else:
        result = mycursor.fetchone()
        if not result:
            response = {
                "status": False,
                "message": "Invalid Email or Password!"
            }
            return jsonify(response)
        else:
            data = UserModel(
                user_id=result[0],
                role=result[1],
                first_name=result[2],
                last_name=result[3],
                email=result[4],
                password=result[5],
                phone=result[6],
                status=result[7]
            )
            response = {
                "status": True,
                "message": "Validation Success!",
                "data": data.to_dict()
            }
            return jsonify(response)
