VOID_ELEMENTS = 'br hr img input link meta area base col command embed keygen param source track wbr '.split()

class _TagSource():
	def __getattr__(self,tagName):
		def currentTag(*Contents,Content=None,**attributes):
			if(Content!=None):
				if len(Contents)!=0:
					raise ValueError('You can not have unnamed arguments if you specify Content.')
				else:
					Contents = Content
			opentag =(
				f'<{tagName}' +
				''.join( f' {name}="{attributes[name]}"' for name in attributes )
			)
			if tagName in VOID_ELEMENTS:
				return opentag+'/>'
			else:
				return (
					opentag+'>'+
						''.join(Contents)+
					f'</{tagName}>'
				)
		return currentTag

tagSource = _TagSource()
#with open('tags.txt') as tagFile:
#	for tagName in tagFile.read().split():
#		globals()[tagName] = getattr(tagSource,tagName)

def css(*Selectors,**properties):
	table = str.maketrans('_','-')
	return  ''.join((
		','.join(Selectors), '{', *(
			f"{ key.translate(table) }:{ properties[key] };"
			for key in properties
		), '}'
	))

