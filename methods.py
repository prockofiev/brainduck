from __future__ import annotations
import traceback
from variables import Variables


class Code:
    def __init__( self ):
        self.code = ""
        self.func = {}


    def add_code( self, code: str, func: str ):
        i = len( self.code )
        self.code += code
        self.func[ i ] = func

        self.optimizer_code()


    def get_code( self ):
        return self.code


    def get_func( self ):
        return self.func 


    def optimizer_code( self ):
        pass

    
class Methods:
    def __init__( self):
        self.cursor = 0
        self.code = Code()


    def add_code( self, new_code: str ):
        self.code.add_code( code = new_code, func = '.'.join( [ func.name for func in traceback.extract_stack()[ 3:-1 ] ] ) )


    def get_code( self ):
        return self.code


    def set_cursor( self, index: int ):
        self.add_code( '>' * ( index - self.cursor ) + '<' * ( self.cursor - index ) )
        self.cursor = index


    def add_value( self, value: int ):
        self.add_code( '+' * ( value % 2 ) )


    def clear_value( self ):
        self.add_code( '[+]' )


    def set_value( self, value: int ):
        self.clear_value()
        self.add_value( value = value )


    def add_value_for_index( self, value: int, index: int ):
        self.set_cursor( index = index )
        self.add_value( value = value )

    def set_value_for_index( self, value: int, index: int ):
        self.set_cursor( index = index )
        self.set_value( value = value )


    def cycle( self, head: int, body: list[ tuple[ function, dict ] ] ):
        self.set_cursor( index = head )
        self.add_code( '[' )

        for command, args in body:
            command( **args )

        self.set_cursor( index = head )

        self.add_code( ']' )


    def condition( self, head: int, body: list[ tuple[ function, dict ] ] ):
        temp = Variables( name = None, size = 1 )
        self.copy( src = head, dests = [ temp.index ] )
        body.append( ( self.set_value_for_index, { 'index': temp.index, 'value': 0 } ) )
        self.cycle( head = temp.index, body = body )
        temp.remove()


    def move( self, src: int, dests: list[ int ] ):
        body = [ ( self.add_value_for_index, { 'value': 1, 'index': dest } ) for dest in sorted( dests ) ]

        body.append( ( self.add_value_for_index, { 'value': -1, 'index': src } ) )

        self.cycle( head = src, body = body )


    def copy( self, src: int, dests: list[ int ], temp: int = None ):
        if temp:
            self.move( src = src, dests = dests + [ temp ] )
            self.move( src = temp, dests = [ src ] )
        else:
            temp = Variables( name = None, size = 1 )
            self.move( src = src, dests = dests + [ temp.index ] )
            self.move( src = temp.index, dests = [ src ] )
            temp.remove()


    def set_input_for_index( self, index: int ):
        self.set_cursor( index = index )
        self.add_code( ',' )


    def set_input_for_variable( self, var: Variables ):
        for i in range( var.size ):
            self.set_input_for_index( index = var.index + i )


    def output_for_index( self, index: int ):
        self.set_cursor( index = index )
        self.add_code( '.' )


    def output_for_variable( self, var: Variables ):
        for i in range( var.size ):
            self.output_for_index( index = var.index + i )


    def summ( self, i1: int, i2: int, i3: int, y1: int, y2: int ):
        temp = Variables( name = None, size = 10 )

        for i in range( 3 ):
            self.set_cursor( index = temp.index + i )
            self.add_value( value = 1 )

        for i, el in enumerate( [ i1, i2, i3 ] ):
            self.copy( src = el, dests = [ temp.index + 4 + i ], temp = temp.index + 3 )

        self.set_cursor( temp.index + 4 )

        
        self.add_code( "[>>>>+<<<<<]<[>]>>[>>>+<<<<<]<<[>]>>>[>>+<<<<<]<<<[>]>[>]+[<]>>>>>[+<+>>+<]>[+<+>]<<+<+<+<[>]<+<<<<[>]" )
        self.cursor = temp.index + 3

        self.set_cursor( index = y1 )
        self.clear_value()
        self.move( src = temp.index + 8, dests = [ y1 ] )
        self.set_cursor( index = y2 )
        self.clear_value()
        self.move( src = temp.index + 7, dests = [ y2 ] )

        self.clear_variable( temp )
        temp.remove()


    def invert_variable( self, var: Variables ):
        for i in range( var.size ):
            self.set_cursor( var.index + i )
            self.add_value( value = 1 )


    def change_the_sign_variable( self, var: Variables, result: Variables ):
        temp = Variables( name = None, size = var.size )
        self.add_value_for_variable( var = temp, value = 1 )

        self.copy_variables( src = var, dest = result )
        self.invert_variable( var = result )
        self.sum_variables( var1 = temp, var2 = result, result = result )

        self.clear_variable( temp )
        temp.remove()


    def check_variable( self, var: Variables, result: Variables ):
        self.add_value_for_variable( var = result, value = 1 )
        for i in range( var.size ):
            self.condition( head = var.index + i, body = [ ( self.set_value_for_index, { 'index': result.index, 'value': 0 } ) ] )

        self.invert_variable( var = result )


    def clear_variable( self, var: Variables ):
        for i in range( var.size ):
            self.set_cursor( var.index + i )
            self.clear_value()


    def move_variables( self, src: Variables, dest: Variables ):
        for i in range( min( src.size, dest.size ) ):
            self.move( src = src.index + i, dests = [ dest.index + i ] ) 


    def copy_variables( self, src: Variables, dest: Variables ):
        temp = Variables( None, 1 )

        for i in range( min( src.size, dest.size ) ):
            self.copy( src = src.index + i, dests = [ dest.index + i ], temp = temp.index ) 

        temp.remove()


    def add_value_for_variable( self, var: Variables, value: int ):
        i = 0
        while value > 0 and i < var.size:
            self.set_cursor( index = var.index + var.size - i - 1 )
            self.add_value( value % 2 )
            value //= 2
            i += 1


    def sum_variables( self, var1: Variables, var2: Variables, result: Variables, bias: int = 0 ):
        temp = Variables( name = None, size = 1 )
        temp_null = Variables( name = None, size = 1 )

        for i in range( var1.size - 1, -1, -1 ):
            if i + bias < var2.size:
                self.summ( i1 = var1.index + i, i2 = var2.index + i + bias, i3 = temp.index, y1 = result.index + i, y2 = temp.index )
            else:
                self.summ( i1 = var1.index + i, i2 = temp_null.index, i3 = temp.index, y1 = result.index + i, y2 = temp.index )

        self.clear_variable( temp )
        temp.remove()
        temp_null.remove()


    def cycle_for_variables( self, head: Variables, body: list[ tuple[ function, dict ] ] ):
        temp = Variables( name = None, size = head.size + 2 )
        head_temp = Variables( name = None, size = 1 )

        # Предусловие
        for i in range( head.size ):
            self.copy( src = head.index + i, dests = [ temp.index + 1 + i ], temp = head_temp.index )
            self.set_cursor( index = temp.index + 1 + i )
            self.add_code( '+' )

        self.set_cursor( index = temp.index + 1 )

        self.add_code('[>]+<[<]')
        self.cursor = temp.index

        self.set_cursor( temp.index + 4 )
        self.add_code( '+' )
        
        self.move( src = temp.index + 4, dests = [ head_temp.index ] )
        self.clear_variable( temp )

        self.set_cursor( index = head_temp.index )
        self.add_code( '[' )

        self.clear_variable( var = head_temp )

        for command, args in body:
             command( **args )

        # Постусловие
        for i in range( head.size ):
            self.copy( src = head.index + i, dests = [ temp.index + 1 + i ], temp = head_temp.index )
            self.set_cursor( index = temp.index + 1 + i )
            self.add_code( '+' )

        self.set_cursor( index = temp.index + 1 )

        self.add_code('[>]+<[<]')
        self.cursor = temp.index

        self.set_cursor( temp.index + 4 )
        self.add_code( '+' )

        self.move( src = temp.index + 4, dests = [ head_temp.index ] )
        self.clear_variable( temp )

        self.set_cursor( index = head_temp.index )
        self.add_code( ']' )

        self.clear_variable( var = temp )
        temp.remove()
        self.clear_variable( var = head_temp )
        head_temp.remove()

    def multiplication_variables( self, var1: Variables, var2: Variables, result: Variables ):
        temp = Variables( name = None, size = 2 )
        res = Variables( name = None, size = result.size )

        for i in range( var1.size - 1, -1, -1 ):
            self.copy( src = var1.index + i, dests = [ temp.index ], temp = temp.index + 1  )
            self.set_cursor( index = temp.index )
            self.add_code( '[' )
            self.sum_variables( var1 = result, var2 = var2, result = res, bias = var1.size - 1 - i )
            self.clear_variable( var = temp ) 
            self.clear_variable( var = result )
            self.move_variables( src = res, dest = result)
            self.set_cursor( index = temp.index )
            self.add_code( ']' )

        temp.remove()
        res.remove()