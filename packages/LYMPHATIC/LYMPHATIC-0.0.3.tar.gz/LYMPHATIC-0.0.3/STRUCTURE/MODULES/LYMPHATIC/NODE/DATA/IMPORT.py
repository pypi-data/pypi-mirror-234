

'''
	rethinkdb import -f FILE --table DB.TABLE [-c HOST:PORT] [--tls-cert FILENAME] [-p] [--password-file FILENAME]
      [--force] [--clients NUM] [--format (csv | json)] [--pkey PRIMARY_KEY]
      [--shards NUM_SHARDS] [--replicas NUM_REPLICAS]
      [--delimiter CHARACTER] [--custom-header FIELD,FIELD... [--no-header]]
'''

'''
	rethinkdb restore 
		FILE [-c HOST:PORT] 
		[--tls-cert FILENAME] 
		[-p] [--password-file FILENAME] 
		[--clients NUM] 
		[--shards NUM_SHARDS] 
		[--replicas NUM_REPLICAS] 
		[--force] 
		[-i (DB | DB.TABLE)]
'''

'''
	???
		rethinkdb restore 
'''

def RESTORE ():
	return;