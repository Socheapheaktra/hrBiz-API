class UserModel:
    def __init__(self, user_id, role, first_name, last_name, email, password, phone, status):
        self.user_id = user_id
        self.role = role
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.phone = phone
        self.status = status

    def to_dict(self):
        return {
            "id": self.user_id,
            "role": self.role,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "password": self.password,
            "phone": self.phone,
            "status": self.status
        }

class EmployeeExportModel:
    def __init__(self, user_id, first_name, last_name, role, email, phone, status):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.role = role
        self.email = email
        self.phone = phone
        self.status = status

    def to_dict(self):
        return {
            "id": self.user_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "role": self.role,
            "email": self.email,
            "phone": self.phone,
            "status": self.status
        }