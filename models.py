from app import db
from sqlalchemy.dialects.postgresql import JSON

class Diagnosis(db.Model):
	procedure = db.Column(db.Integer, primary_key=True)
	avg_total_payments = db.Column(db.Money)
	avg_total_payments = db.Column(db.Money) 
	provider_id = db.Column(db.Integer)

	def __init__(self, incident_id, type):
		self.incident_id = incident_id
		self.type = type
