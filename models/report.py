class ReportModel:
    def __init__(self, report_id, user_id, sale_rep, presale, entry_date, forecast_lead, cus_name, contact_person, position,
                 revenue, project_name, vendor, deal_registration, project_status, probability, status):
        self.report_id = report_id
        self.user_id = user_id
        self.sale_rep = sale_rep
        self.presale = presale
        self.entry_date = entry_date
        self.forecast_lead = forecast_lead
        self.cus_name = cus_name
        self.contact_person = contact_person
        self.position = position
        self.revenue = revenue
        self.project_name = project_name
        self.vendor = vendor
        self.deal_registration = deal_registration
        self.project_status = project_status
        self.probability = probability
        self.status = status

    def to_dict(self):
        return {
            "id": self.report_id,
            "user_id": self.user_id,
            "sale_rep": self.sale_rep,
            "presale": self.presale,
            "entry_date": self.entry_date,
            "forecast_lead": self.forecast_lead,
            "cus_name": self.cus_name,
            "contact_person": self.contact_person,
            "position": self.position,
            "revenue": self.revenue,
            "project_name": self.project_name,
            "vendor": self.vendor,
            "deal_registration": self.deal_registration,
            "project_status": self.project_status,
            "probability": self.probability,
            "status": self.status
        }

class ReportDetail:
    def __init__(self, report_id, sale_rep, presale, entry_date, forecast_lead, cus_name, contact_person, position,
                 revenue, project_name, vendor, deal_registration, project_status, probability):
        self.report_id = report_id
        self.sale_rep = sale_rep
        self.presale = presale
        self.entry_date = entry_date
        self.forecast_lead = forecast_lead
        self.cus_name = cus_name
        self.contact_person = contact_person
        self.position = position
        self.revenue = revenue
        self.project_name = project_name
        self.vendor = vendor
        self.deal_registration = deal_registration
        self.project_status = project_status
        self.probability = probability

    def to_dict(self):
        return {
            "id": self.report_id,
            "sale_rep": self.sale_rep,
            "presale": self.presale,
            "entry_date": self.entry_date,
            "forecast_lead": self.forecast_lead,
            "cus_name": self.cus_name,
            "contact_person": self.contact_person,
            "position": self.position,
            "revenue": self.revenue,
            "project_name": self.project_name,
            "vendor": self.vendor,
            "deal_registration": self.deal_registration,
            "project_status": self.project_status,
            "probability": self.probability
        }
