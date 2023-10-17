
'''

'''

'''
	SOURCES:
		https://healthjade.net/eosinophils/
'''
def INSERT_EPISODE ():
	
	PRIMARY_KEY = "EPISODE"
	DB = "EOSINOPHILS"
	TABLE = "CHEMOKINE RECEPTORS"
	
	FIELDS = {}

	r.db (DB).table (TABLE).insert ({
		PRIMARY_KEY: (
			r.expr (
				r.db (DB).table (TABLE).max (PRIMARY_KEY).getField (
					PRIMARY_KEY
				).coerceTo ('number')
			).add (1)
		),
		
		...FIELDS
	})