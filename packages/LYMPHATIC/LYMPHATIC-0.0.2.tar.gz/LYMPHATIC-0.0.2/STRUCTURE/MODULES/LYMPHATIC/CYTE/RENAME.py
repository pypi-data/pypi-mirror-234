



'''
	REPL:
		r.db ('rethinkdb').table ('db_config').filter ({ 
			name: 'B CYTE 1'
		}).update ({ 
			name: 'B-CYTE 1'
		}).run ()
		
		
	DATA EXPLORER:
		r.db ('rethinkdb').
		table ('db_config').
		filter ({ 
			name: 'B CYTE 1' 
		}).
		update ({ 
			name: 'B-CYTE 1'
		})
'''

def RENAME (r, c, PARAMS):
	CURRENT = PARAMS ["CURRENT"]
	NEW = PARAMS ["NEW"]

	r.db (CURRENT).config ().update ({
		name: NEW
	}).run (c)

	return;