from variables import Variables

class Methods:
    def __init__( self):
        self.cursor = 0
        self.code = ""


    def setCursor( self, index: int ):
        self.addCode( '>' * ( index - self.cursor ) + '<' * ( self.cursor - index ) )
        self.cursor = index


    def addValue( self, value: int ):
        self.addCode( '+' * ( value % 2 ) )


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


    def summ( self, i1: int, i2: int, i3: int, y1: int, y2: int ):
        temp = Variables( name = None, size = 10 )

        for i in range( 3 ):
            self.setCursor( index = temp.index + i )
            self.addValue( value = 1 )

        for i, el in enumerate( [ i1, i2, i3 ] ):
            self.copy( src = el, dests = [ temp.index + 4 + i ], temp = temp.index + 3 )

        self.setCursor( temp.index + 4 )

        
        self.addCode( "[>>>>+<<<<<]<[>]>>[>>>+<<<<<]<<[>]>>>[>>+<<<<<]<<<[>]>[>]+[<]>>>>>[+<+>>+<]>[+<+>]<<+<+<+<[>]<+<<<<[>]" )
        self.cursor = temp.index + 3

        self.setCursor( index = y1 )
        self.clearValue()
        self.move( src = temp.index + 8, dests = [ y1 ] )
        self.setCursor( index = y2 )
        self.clearValue()
        self.move( src = temp.index + 7, dests = [ y2 ] )

        self.clearVariable( temp )
        temp.remove()
        

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
        while value > 0 and i < var.size:
            self.setCursor( index = var.index + var.size - i - 1 )
            self.addValue( value % 2 )
            value //= 2
            i += 1


    def clearVariable( self, var: Variables ):
        for i in range( var.size ):
            self.setCursor( var.index + i )
            self.clearValue()


    def sumVariables( self, var1: Variables, var2: Variables, result: Variables ):
        temp = Variables( name = None, size = 1 )

        for i in range( var1.size -1, -1, -1 ):
            self.summ( i1 = var1.index + i, i2 = var2.index + i, i3 = temp.index, y1 = result.index + i, y2 = temp.index )

       
        self.clearVariable( temp )
        temp.remove()

    def clearCode( self ):
        self.code = ""


    def addCode( self, newCode: str ):
        self.code += newCode


    def getCode( self ):
        return self.code