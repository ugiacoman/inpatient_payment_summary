# inpatient_payment_summary
Inpatient Prospective Payment System Provider Summary for Top 100 Diagnoses FY2011


# How to Setup DB

1. Run python interpretor `$ python` and enter following commands

	```python 
	>>> from models import db
	```

	```python 
	>>> db.create_all()
	```

2. This will setup blank tables. Note: You'll have to change line 6 

	`'postgresql://<user>:<password>@localhost/<dbname>'`

