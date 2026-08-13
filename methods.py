from variables import Variables

class Methods:
    def __init__( self, MEM_SIZE: int ):
        self.cursor = 0
        self.code = ""

        self.MEM_SIZE = MEM_SIZE


    def setCursor( self, index: int ):
        self.addCode( '>' * ( index - self.cursor ) + '<' * ( self.cursor - index ) )
        self.cursor = index


    def addValue( self, value: int ):
        self.addCode( '+' * value + '-' * ( -value ) )


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
        body.append( ( self.addValue, { 'value': -1 } ) )

        self.cycle( head = src, body = body )


    def copy( self, src: int, dests: list[ int ], temp: int ):
        self.move( src = src, dests = dests + [ temp ] )
        self.move( src = temp, dests = [ src ] )


    def moveVariables( self, src: Variables, dest: Variables ):
        for i in range( min( src.size, dest.size ) ):
            self.move( src = src.index + i, dests = [ dest.index + i ] ) 


    def copyVariables( self, src: Variables, dest: Variables ):
        temp = Variables( None, 1 )

        for i in range( min( src.size, dest.size ) ):
            self.copy( src = src.index + i, dests = [ dest.index + i ], temp = temp.index ) 

        temp.remove()


    def addValueForVariable( self, var: Variables, value: int ):
        i = 0
        while value % self.MEM_SIZE and i < var.size:
            self.setCursor( index = var.index + i )
            self.addValue( value % 256 )
            value //= 256 
            i += 1


    def clearCode( self ):
        self.code = ""


    def addCode( self, newCode: str ):
        self.code += newCode


    def getCode( self ):
        return self.code