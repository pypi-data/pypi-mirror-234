

def CYTE (GROUP):
	import click
	@GROUP.group ("CYTE")
	def GROUP ():
		pass
		
	import click
	@GROUP.command ("EXAMPLE")
	@click.option ('--example-option', default = '', help = '')
	def EXAMPLE (example_option):	
		print ("example option")

	return;