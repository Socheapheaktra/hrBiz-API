from flask import Blueprint, request, jsonify

from models.report import ReportModel, ReportDetail

from utils.conn import mycursor, mydb

report = Blueprint('report', __name__)

@report.route('/report-list', methods=['GET'])
def get_report_list():
    try:
        sql = 'SELECT * FROM tblReport'
        mycursor.execute(sql)
    except Exception as err:
        return jsonify({
            "status": False,
            "message": f"{err}"
        })
    else:
        data = list()
        reports = mycursor.fetchall()
        for report in reports:
            data.append(ReportModel(
                report_id=report[0],
                user_id=report[1],
                sale_rep=report[2],
                presale=report[3],
                entry_date=report[4].strftime("%Y-%m-%d") if report[4] else None,
                forecast_lead=report[5],
                cus_name=report[6],
                contact_person=report[7],
                position=report[8],
                revenue=report[9],
                project_name=report[10],
                vendor=report[11],
                deal_registration=report[12],
                project_status=report[13],
                probability=report[14],
                status=report[15]
            ).to_dict())
        return jsonify({
            "status": True,
            "message": "Success",
            "data": data
        })

# TODO: Fetch report where status is 'Inactive'
@report.route('/report-history', methods=['GET'])
def fetch_history_report():
    try:
        sql = 'SELECT * FROM tblReport ' \
              'WHERE status=0'
        mycursor.execute(sql)
    except Exception as err:
        return jsonify({
            "status": False,
            "message": f"{err}"
        })
    else:
        data = list()
        reports = mycursor.fetchall()
        for report in reports:
            data.append(ReportModel(
                report_id=report[0],
                user_id=report[1],
                sale_rep=report[2],
                presale=report[3],
                entry_date=report[4].strftime("%Y-%m-%d") if report[4] else None,
                forecast_lead=report[5],
                cus_name=report[6],
                contact_person=report[7],
                position=report[8],
                revenue=report[9],
                project_name=report[10],
                vendor=report[11],
                deal_registration=report[12],
                project_status=report[13],
                probability=report[14],
                status=report[15]
            ).to_dict())
        return jsonify({
            "status": True,
            "message": "Success",
            "data": data
        })

# TODO: Insert new report into database
# FIXME: API not ready (Ready for testing)
@report.route('/create', methods=['POST'])
def create_report():
    if not request.data or not request.is_json:
        return jsonify({
            "status": False,
            "message": "Invalid Data"
        })
    req = request.get_json()

    if "user_id" not in req or "sale_rep" not in req or "presale" not in req or "entry_date" not in req \
            or "forecast_lead" not in req or "cus_name" not in req or "contact_person" not in req \
            or "position" not in req or "revenue" not in req or "project_name" not in req or "vendor" not in req \
            or "deal_registration" not in req or "project_status" not in req or "probability" not in req \
            or "status" not in req:
        return jsonify({
            "status": False,
            "message": "Invalid Arguments"
        })

    for key in req.keys():
        if req[f'{key}'] == "":
            req[f'{key}'] = None

    try:
        sql = 'INSERT INTO tblReport(' \
              'user_id, sale_rep, presale, entry_date, forecast_lead, customer_name, contact_person, position, ' \
              'revenue, project_name, vendor, deal_registration, project_status, probability, status) ' \
              'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        values = [req['user_id'], req['sale_rep'], req['presale'], req['entry_date'], req['forecast_lead'],
                  req['cus_name'], req['contact_person'], req['position'], req['revenue'], req['project_name'],
                  req['vendor'], req['deal_registration'], req['project_status'], req['probability'], req['status'], ]
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
            "message": "New Report added successfully!"
        })

# TODO: Update report fields according to inputs
# FIXME: API not ready
@report.route('/edit', methods=['POST'])
def edit_report():
    if not request.data or not request.is_json:
        return jsonify({
            "status": False,
            "message": "Invalid Data"
        })
    req = request.get_json()

    if "user_id" not in req or "sale_rep" not in req or "presale" not in req or "entry_date" not in req \
            or "forecast_lead" not in req or "cus_name" not in req or "contact_person" not in req \
            or "position" not in req or "revenue" not in req or "project_name" not in req or "vendor" not in req \
            or "deal_registration" not in req or "project_status" not in req or "probability" not in req\
            or "status" not in req:
        return jsonify({
            "status": False,
            "message": "Invalid Arguments"
        })

    try:
        sql = 'UPDATE tblReport SET ' \
              'user_id=%s, sale_rep=%s, ' \
              'presale=%s, entry_date=%s, ' \
              'forecast_lead=%s, customer_name=%s, ' \
              'contact_person=%s, position=%s, ' \
              'revenue=%s, project_name=%s, ' \
              'vendor=%s, deal_registration=%s,' \
              'project_status=%s, probability=%s,' \
              'status=%s ' \
              'WHERE id=%s'
        values = [req['user_id'], req['sale_rep'], req['presale'], req['entry_date'],
                  req['forecast_lead'], req['cus_name'], req['contact_person'], req['position'], req['revenue'],
                  req['project_name'], req['vendor'], req['deal_registration'], req['project_status'],
                  req['probability'], req['status'], req['report_id'], ]
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
            "message": "Report Update successfully!"
        })

# TODO: Fetch Report detail after clicking on Edit Report
@report.route('/report-detail', methods=['POST'])
def get_report_detail():
    """
    HTTP POST: http://127.0.0.1:5000/report/report-detail
    :param <str> report_id: ID of the selected report
    :return <dict>: status True if success and result will be in "data"
    """
    if not request.data or not request.is_json:
        return jsonify({
            "status": False,
            "message": "Invalid Data"
        })
    req = request.get_json()
    if "report_id" not in req:
        return jsonify({
            "status": False,
            "message": "Invalid Arguments"
        })
    try:
        sql = 'SELECT tblReport.id,' \
              'tblReport.user_id,' \
              'tblReport.sale_rep,' \
              'tblReport.presale, ' \
              'tblReport.entry_date,' \
              'tblReport.forecast_lead,' \
              'tblReport.customer_name,' \
              'tblReport.contact_person,' \
              'tblReport.position,' \
              'tblReport.revenue,' \
              'tblReport.project_name,' \
              'tblReport.vendor,' \
              'tblReport.deal_registration,' \
              'tblReport.project_status,' \
              'tblReport.probability,' \
              'tblReport.status ' \
              'FROM tblReport ' \
              'WHERE tblReport.id=%s'
        values = [req['report_id'], ]
        mycursor.execute(sql, values)
    except Exception as err:
        return jsonify({
            "status": False,
            "message": f"{err}"
        })
    else:
        report = mycursor.fetchone()
        data = ReportModel(
            report_id=report[0],
            user_id=report[1],
            sale_rep=report[2] if report[2] else None,
            presale=report[3] if report[3] else None,
            entry_date=report[4].strftime("%Y-%m-%d") if report[4] else None,
            forecast_lead=report[5] if report[5] else None,
            cus_name=report[6] if report[6] else None,
            contact_person=report[7] if report[7] else None,
            position=report[8] if report[8] else None,
            revenue=report[9] if report[9] else None,
            project_name=report[10] if report[10] else None,
            vendor=report[11] if report[11] else None,
            deal_registration=report[12],
            project_status=report[13],
            probability=report[14],
            status=report[15],
        ).to_dict()
        return jsonify({
            "status": True,
            "message": "Success",
            "data": data
        })

# TODO: Update report status from active to inactive
# FIXME: API not ready (Ready for testing)
@report.route('/delete', methods=['POST'])
def delete_report():
    if not request.data or not request.is_json:
        return jsonify({
            "status": False,
            "message": "Invalid Data"
        })
    req = request.get_json()

    if "report_id" not in req:
        return jsonify({
            "status": False,
            "message": "Invalid Argument",
        })

    try:
        sql = 'UPDATE tblReport SET status=0 ' \
              'WHERE id=%s'
        values = [req['report_id'], ]
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
            "message": "This report has been moved to history"
        })
