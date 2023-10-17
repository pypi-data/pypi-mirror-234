

'''
	r.db ('rethinkdb').table ('server_config').get (
		"36be75a0-f329-4140-9262-730ddc6bd850"
	).update ({ name: 'R1' })
	
	
	r.db ('rethinkdb').table ('server_config')
	.filter ({ name: 'NODE-1' })   
	.update ({ name: 'NODE 1' })
'''