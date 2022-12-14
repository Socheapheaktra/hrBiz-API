from flask import Blueprint, request, jsonify, send_file

from models.user import UserModel, EmployeeExportModel
from models.presale import PresaleModel

from utils.conn import mycursor, mydb
from utils.util import check_email

import pandas as pd

from datetime import datetime

employee = Blueprint('employee', __name__)

# TODO: Insert new employee into database
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

# TODO: Edit employee detail and update to database
@employee.route('/edit', methods=['POST'])
def edit_employee():
    if not request.data or not request.is_json:
        return jsonify({
            "status": False,
            "message": "Invalid Data"
        })
    req = request.get_json()
    if "first_name" not in req or "last_name" not in req or "email" not in req \
            or "password" not in req or "phone" not in req or "user_id" not in req:
        return jsonify({
            "status": False,
            "message": "Invalid Arguments"
        })
    try:
        sql = 'UPDATE tblUser SET ' \
              'first_name=%s, last_name=%s, ' \
              'email=%s, password=%s, ' \
              'phone=%s ' \
              'WHERE id=%s'
        values = [req['first_name'], req['last_name'], req['email'], req['password'],
                  req['phone'], req['user_id'], ]
        mycursor.execute(sql, values)
    except Exception as err:
        mydb.rollback()
        return jsonify({
            "status": False,
            "message": f"{err}"
        })
    else:
        mydb.commit()
        return jsonify({
            "status": True,
            "message": "Success"
        })

# TODO: Delete employee from database with user_id
@employee.route('/delete', methods=['POST'])
def delete_employee():
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
        sql = 'UPDATE tblUser ' \
              'SET status=0 ' \
              'WHERE id=%s'
        values = [req['user_id'], ]
        mycursor.execute(sql, values)
    except Exception as err:
        mydb.rollback()
        return jsonify({
            "status": False,
            "message": f"{err}"
        })
    else:
        mydb.commit()
        return jsonify({
            "status": True,
            "message": "Success"
        })

# TODO: Fetch User detail after clicking on Edit User
@employee.route('/user-detail', methods=['POST'])
def get_user_detail():
    if not request.data or not request.is_json:
        return jsonify({
            "status": False,
            "message": "Invalid Data"
        })
    req = request.get_json()
    print(req)
    if "user_id" not in req:
        return jsonify({
            "status": False,
            "message": "Invalid Arguments"
        })
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
              'WHERE tblUser.id=%s'
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
            status="Active" if user[7] == 1 else "Inactive"
        ).to_dict()
        return jsonify({
            "status": True,
            "message": "Success",
            "data": data
        })

# TODO: Fetch all employees from database
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

# TODO: Fetch Sales/Presales Name from database
@employee.route('/get-sale-presale', methods=["GET"])
def get_sale_presale():
    """
    :HTTP GET: http://127.0.0.1:5000/employee/get-sale-presale
    :return data: List of Presale Names.
    """
    try:
        sql = 'SELECT * FROM tblPresale ' \
              'WHERE status=1'
        mycursor.execute(sql)
    except Exception as err:
        return jsonify({
            "status": False,
            "message": f"{err}"
        })
    else:
        results = mycursor.fetchall()
        data = list()
        if results:
            for result in results:
                data.append(PresaleModel(
                    presale_id=result[0],
                    name=result[1],
                    status="Active" if result[2] == 1 else "Inactive"
                ).to_dict())
            return jsonify({
                "status": True,
                "message": "Success",
                "data": data
            })
        else:
            return jsonify({
                "status": False,
                "message": "No Data",
            })

# TODO: Export Employee_List as Excel format
@employee.route("/export", methods=['GET'])
def export_to_excel():
    """
    HTTP GET: http://127.0.0.1:5001/employee/export
    :return:
        :parameter:
            :param: status
            :type: boolean
            :description: return True
        :parameter:
            :param: message
            :type: string
            :description: Message showing query success
        :parameter:
            :param: data
            :type: list
            :description: List of employees
    :except:
        :parameter:
            :param: status
            :type: boolean
            :description: return False
        :parameter:
            :param: message
            :type: string
            :description: Failed Message
    """
    try:
        sql = """
        SELECT 
        tblUser.id,
        tblUser.first_name,
        tblUser.last_name,
        tblRole.name,
        tblUser.email,
        tblUser.phone,
        tblUser.status 
        FROM tblUser 
        INNER JOIN tblRole ON tblUser.role_id = tblRole.id
        """
        mycursor.execute(sql)
    except Exception as err:
        return jsonify({
            "status": False,
            "message": f"SQL Error:{err}"
        })
    else:
        result = mycursor.fetchall()
        if not result:
            return jsonify({
                "status": False,
                "message": f"No Employees found!"
            })
        data = list()
        for item in result:
            data.append(EmployeeExportModel(
                user_id=item[0],
                first_name=item[1],
                last_name=item[2],
                role=item[3],
                email=item[4],
                phone=item[5],
                status="Active" if item[6] == 1 else "Inactive"
            ).to_dict())

        return jsonify({
            "status": True,
            "message": "Query Successful!",
            "data": data
        })

        # file_name = f"Employee_List_{datetime.now().strftime('%d-%m-%Y')}"
        # try:
        #     """ Create DataFrame """""
        #     data = pd.DataFrame(data)
        #
        #     """ Write to Excel """
        #     xlsx_file = pd.ExcelWriter(
        #         file_name,
        #         engine="xlsxwriter"
        #     )
        #
        #     data.to_excel(xlsx_file, sheet_name=f"{datetime.now().strftime('%d-%m-%Y')}", index=False)
        #
        #     xlsx_file.save()
        # except Exception as err:
        #     return jsonify({
        #         "status": False,
        #         "message": f"Cannot Export to Excel: {err}"
        #     })
        # else:
        #     return send_file(xlsx_file,
        #                      as_attachment=True,
        #                      download_name=f"{file_name}.xlsx",
        #                      mimetype='xlsx')
