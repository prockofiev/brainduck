from variables import Variables

MEM_SIZE = 256

class Methods:
    def __init__( self ):
        self.cursor = 0
        self.code = ""


    def setCursor( self, index: int ):
        self.addCode( '>' * ( index - self.cursor ) + '<' * ( self.cursor - index ) )
        self.cursor = index


    def addValue( self, value: int ):
        self.addCode( '+' * value )


    def clearValue( self ):
        self.addCode( '[+]' )


    def setValue( self, value: int ):
        self.clearValue()
        self.addValue( value = value )


    def cycle( self, head: int, body: list[ tuple[ function, dict ] ] ):
        self.setCursor( index = head )
        self.addCode( '[' )

        for command, args in body:
            command( **args )

        self.setCursor( index = head )

        self.addCode( ']' )


    def move( self, src: int, dests: list[ int ] ):
        body = []
        for dest in sorted( dests ):
            body.append( ( self.setCursor, { 'index': dest } ) )
            body.append( ( self.addValue, { 'value': 1 } ) )
        body.append( ( self.setCursor, { 'index': src } ) )

        self.cycle( head = src, body = body )


    def copy( self, src: int, dests: list[ int ], temp: int ):
        self.move( src = src, dests = dests + [ temp ])


    def copyVariables( self, src: Variables, dest: Variables ):
        temp = Variables( None, 1 )

        for i in range( min( src.size, dest.size ) ):
            self.copy( src = src.index, dests = [ dest.index ], temp = temp.index )

        temp.remove()


    def addValueForVariable( self, var: Variables, value: int ):
        i = 0
        while value % MEM_SIZE and i < var.size:
            self.setCursor( index = var.index + i )
            self.addValue( value % 256 )
            value //= 256 


    def clearCode( self ):
        self.code = ""


    def addCode( self, newCode: str ):
        self.code += newCode


    def getCode( self ):
        return self.code