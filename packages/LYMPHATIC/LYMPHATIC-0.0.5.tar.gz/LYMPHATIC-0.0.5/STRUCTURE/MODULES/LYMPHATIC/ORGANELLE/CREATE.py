

'''
	{ GOAL }
		import LYMPHATIC.ORGANELLE.CREATE as ORGANELLE_CREATOR
		ORGANELLE_CREATOR.CREATE (C, DB, TABLE, )
		
		# WITH:
			* PIES
			** PIES
			
			FOR:
				shards
				replicas
'''

'''
	SOURCES:
		https://rethinkdb.com/api/python/table_create
		https://www.roswellpark.org/cancertalk/202007/types-white-blood-cells-what-numbers-may-mean
		https://en.wikipedia.org/wiki/Basophil
		https://my.clevelandclinic.org/health/body/23256-basophils
'''

'''
	REPL:
		r.db ('BASOPHIL 9473').table_create ('CYTOPLASM', primary_key = 'ACCESS').run (c)

	DATA EXPLORER:
		r.db ('BASOPHIL 1391').tableCreate ('GRANULES', { primaryKey: 'GRANULE' }).run (c)
'''



def CREATE (r, c, PARAMS):
	r.db (DB).table_create (
		TABLE, 
		shards = 2, 
		replicas = 3
	).run (c)
