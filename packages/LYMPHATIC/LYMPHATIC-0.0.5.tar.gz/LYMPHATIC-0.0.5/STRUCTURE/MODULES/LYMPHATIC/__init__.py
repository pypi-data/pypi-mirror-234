



def OPEN_STUDIES ():
	import LYMPHATIC.STUDIES as STUDIES
	STUDIES.OPEN ()
	
	
def CLIQUE ():
	from LYMPHATIC.CYTE.CLIQUE_GROUP import CYTE
	import LYMPHATIC.STUDIES as STUDIES

	def START ():
		import click
		@click.group ()
		def GROUP ():
			pass

		import click
		@click.command ("STUDIES")
		def STUDIES_COMMAND ():	
			STUDIES.OPEN ()

			return;
		GROUP.add_command (STUDIES_COMMAND)

		CYTE (GROUP)
		
		GROUP ()


	START ()