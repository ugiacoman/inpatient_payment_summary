from app import db
from sqlalchemy.dialects.postgresql import JSON

class Incident(db.Model):
	incident_id = db.Column(db.Integer, primary_key=True)
	type = db.Column(db.String(100))

	def __init__(self, incident_id, type):
		self.incident_id = incident_id
		self.type = type