from app import db
from sqlalchemy.dialects.postgresql import JSON



class Diagnosis(db.Model):
	procedure = db.Column(db.Integer, primary_key=True)
 	provider_id = db.Column(db.Integer)

	avg_total_payments = db.Column(db.Numeric(precision=2, asdecimal=True))
	avg_medicare_payments = db.Column(db.Numeric(precision=2, asdecimal=True))
	avg_covered_charges = db.Column(db.Numeric(precision=2, asdecimal=True))
	total_discharge = db.Column(db.Numeric(precision=2, asdecimal=True))

	def __init__(self, procedure, provider_id, avg_medicare_payments, avg_total_payments, 
		avg_covered_charges, total_discharge):
		self.procedure = procedure
		self.provider_id = provider_id
		self.avg_total_payments = avg_total_payments
		self.avg_medicare_payments = avg_medicare_payments
		self.avg_covered_charges = avg_covered_charges
		self.total_discharge = total_discharge

'''
Diagnosis Table:

	procedure: 
	provider_id: (Foreign key references id in Provider Table)
	avg_total_payments:
	avg_medicare_payments:
	avg_covered_charges:
	total_discharge: 

'''
class Diagnosis(db.Model):
	procedure = db.Column(db.Integer, primary_key=True)
 	provider_id = db.Column(db.Integer)

	avg_total_payments = db.Column(db.Numeric(precision=2, asdecimal=True))
	avg_medicare_payments = db.Column(db.Numeric(precision=2, asdecimal=True))
	avg_covered_charges = db.Column(db.Numeric(precision=2, asdecimal=True))
	total_discharge = db.Column(db.Numeric(precision=2, asdecimal=True))

	def __init__(self, procedure, provider_id, avg_medicare_payments, avg_total_payments, 
		avg_covered_charges, total_discharge):
		self.procedure = procedure
		self.provider_id = provider_id
		self.avg_total_payments = avg_total_payments
		self.avg_medicare_payments = avg_medicare_payments
		self.avg_covered_charges = avg_covered_charges
		self.total_discharge = total_discharge		