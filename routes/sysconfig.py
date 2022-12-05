from flask import Blueprint, request, jsonify

from models.presale import PresaleModel

from utils.conn import mycursor, mydb

sysconfig = Blueprint('sysconfig', __name__)

@sysconfig.route('/list-sale-presale', methods=['GET'])
def list_sale_presale():
    """
    HTTP GET: http://127.0.0.1:5000/sysconfig/list-sale-presale
    :return: List of all sales / presales from db
    """
    try:
        sql = 'SELECT * FROM tblPresale'
        mycursor.execute(sql)
    except Exception as err:
        return jsonify({
            "status": False,
            "message": f"{err}"
        })
    else:
        results = mycursor.fetchall()
        if results:
            data = list()
            for result in results:
                data.append(PresaleModel(
                    presale_id=result[0],
                    name=result[1],
                    status="Active" if result[2] == 1 else "Inactive"
                ).to_dict())
            return jsonify({
                "status": True,
                "message": "Query Success!",
                "data": data
            })
        else:
            return jsonify({
                "status": True,
                "message": "No Data Found!"
            })

@sysconfig.route('/sale-presale-detail', methods=['POST'])
def get_presale_detail():
    if not request.data or not request.is_json:
        return jsonify({
            "status": False,
            "message": "Invalid Data"
        })
    req = request.get_json()
    print(req)
    if "presale_id" not in req:
        return jsonify({
            "status": False,
            "message": "Invalid Arguments"
        })
    try:
        sql = 'SELECT * FROM tblPresale ' \
              'WHERE tblPresale.id=%s'
        values = [req['presale_id'],]
        mycursor.execute(sql, values)
    except Exception as err:
        return jsonify({
            "status": False,
            "message": f"{err}"
        })
    else:
        result = mycursor.fetchone()
        data = PresaleModel(
            presale_id=result[0],
            name=result[1],
            status="Active" if result[2] == 1 else "Inactive"
        ).to_dict()
        return jsonify({
            "status": True,
            "message": "Success",
            "data": data
        })

@sysconfig.route("/add-sale-presale", methods=['POST'])
def add_sale_presale():
    """
    HTTP POST: http://127.0.0.1:5001/sysconfig/add-sale-presale
    :param name: REQUIRED!, Name of the Sale or Presale
    :return response: status is True if query success
    """
    if not request.data or not request.is_json:
        return jsonify({
            "status": False,
            "message": "Invalid Data"
        })

    req = request.get_json()
    if "name" not in req:
        return jsonify({
            "status": False,
            "message": "Invalid Parameter"
        })

    try:
        sql = "SELECT name from tblPresale"
        mycursor.execute(sql)
    except Exception as err:
        return jsonify({
            "status": False,
            "message": f"{err}"
        })
    else:
        result = mycursor.fetchall()
        names = list()
        for name in result:
            names.append(name[0])
        if req['name'] in names:
            return jsonify({
                "status": False,
                "message": f"{req['name']} already exists"
            })
        else:
            try:
                sql = 'INSERT INTO tblPresale(name) ' \
                      'VALUES (%s)'
                values = [req['name'], ]
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
                    "message": "Query Success!"
                })

@sysconfig.route("/update-sale-presale", methods=['POST'])
def update_sale_presale():
    """
    HTTP POST: http://127.0.0.1:5000/sysconfig/update-sale-presale
    :param <int> id: ID of sale / presale to be updated
    :param <str> name: Name of sale / presale to be updated
    :param <str> status: Active/Inactive
    :return: status True if Query Success else False + Error Msg
    """
    if not request.data or not request.is_json:
        return jsonify({
            "status": False,
            "message": "Invalid Data"
        })

    req = request.get_json()
    if "id" not in req or "name" not in req or "status" not in req:
        return jsonify({
            "status": False,
            "message": "Invalid Parameters"
        })

    try:
        sql = 'UPDATE tblPresale SET ' \
              'name=%s, status=%s ' \
              'WHERE id=%s'
        values = [req['name'], 1 if req['status'].lower() == "active" else 0, req['id'], ]
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
            "message": "Query Success!"
        })

@sysconfig.route("/remove-sale-presale", methods=["POST"])
def remove_sale_presale():
    """
    HTTP POST: http://127.0.0.1:5000/sysconfig/remove-sale-presale
    :param <int> id: ID of sales / presale to be removed
    :return: status True if query is successful else False + Error Message
    """
    if not request.data or not request.is_json:
        return jsonify({
            "status": False,
            "message": "Invalid Data"
        })

    req = request.get_json()
    if "presale_id" not in req:
        return jsonify({
            "status": False,
            "message": "Invalid Parameters"
        })

    try:
        sql = 'UPDATE tblPresale SET ' \
               'status=0 WHERE tblPresale.id=%s'
        values = [req['presale_id'], ]
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
            "message": "Query Successful!"
        })


@sysconfig.route("/get-all-lead", methods=['GET'])
def list_all_lead():
    """
    HTTP GET: http://127.0.0.1:5000/sysconfig/get-all-lead
    :return: status True if Query Successful and result will be in data
    """
    try:
        sql = 'SELECT name FROM tblLead'
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
                data.append(result[0])
            return jsonify({
                "status": True,
                "message": "Query Success!",
                "data": data
            })

        return jsonify({
            "status": True,
            "message": "No Data"
        })


@sysconfig.route('/get-probability', methods=['GET'])
def list_all_probability():
    """
    HTTP GET: http://127.0.0.1:5000/sysconfig/get-probability
    :return: status True if Query Success and result will be in "data"
    """
    try:
        sql = 'SELECT value FROM tblProbability'
        mycursor.execute(sql)
    except Exception as err:
        return jsonify({
            "status": False,
            "message": f"{err}"
        })
    else:
        results = mycursor.fetchall()
        if results:
            data = list()
            for result in results:
                data.append(int(result[0]))
            return jsonify({
                "status": True,
                "message": "Query Success!",
                "data": data
            })
        else:
            return jsonify({
                "status": True,
                "message": "No Data"
            })


@sysconfig.route('/get-deal-registration', methods=['GET'])
def list_all_deal():
    """
    HTTP GET: http://127.0.0.1:5000/sysconfig/get-deal-registration
    :return: status True if Query Success and result will be in "data"
    """
    try:
        sql = 'SELECT name from tblDeal'
        mycursor.execute(sql)
    except Exception as err:
        return jsonify({
            "status": False,
            "message": f"{err}"
        })
    else:
        results = mycursor.fetchall()
        if results:
            data = list()
            for result in results:
                data.append(result[0])
            return jsonify({
                "status": True,
                "message": "Query Successful!",
                "data": data
            })
        else:
            return jsonify({
                "status": True,
                "message": "No Data"
            })


@sysconfig.route('/get-project-status', methods=['GET'])
def list_all_proj_status():
    """
    HTTP GET: http://127.0.0.1:5000/sysconfig/get-project-status
    :return: status True if Query Successful and result will be in "data"
    """
    try:
        sql = 'SELECT name FROM tblStatus'
        mycursor.execute(sql)
    except Exception as err:
        return jsonify({
            "status": False,
            "message": f"{err}"
        })
    else:
        results = mycursor.fetchall()
        if results:
            data = list()
            for result in results:
                data.append(result[0])
            return jsonify({
                "status": True,
                "message": "Query Success!",
                "data": data
            })
        else:
            return jsonify({
                "status": True,
                "message": "No Data"
            })
