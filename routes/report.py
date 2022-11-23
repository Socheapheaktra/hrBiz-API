from flask import Blueprint, request, jsonify

from models.report import ReportModel

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
                entry_date=report[4].strftime("%d-%m-%Y"),
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
# FIXME: API not ready
@report.route('/report-history', methods=['GET'])
def fetch_history_report():
    pass

# TODO: Insert new report into database
# FIXME: API not ready
@report.route('/create', methods=['POST'])
def create_report():
    pass

# TODO: Update report fields according to inputs
# FIXME: API not ready
@report.route('/edit', methods=['POST'])
def edit_report():
    pass

# TODO: Update report status from active to inactive
# FIXME: API not ready
@report.route('/delete', methods=['POST'])
def delete_report():
    pass
