class PresaleModel:
    def __init__(self, presale_id, name, status):
        self.presale_id = presale_id
        self.name = name
        self.status = status

    def to_dict(self):
        return {
            "id": self.presale_id,
            "name": self.name,
            "status": self.status
        }