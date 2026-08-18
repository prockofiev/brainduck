import re
from methods import Methods
from variables import Variables
from brainfuck import Brainfuck
from render_code import clear_code, blocking, expression_blocking, optimizer_code


class Compile:
    def __init__( self, DEBUG: bool, ONLY_RESULT: bool, SHOW_MEMORY: int ):
        self.DEBUG = DEBUG
        self.ONLY_RESULT = ONLY_RESULT
        self.SHOW_MEMORY = SHOW_MEMORY

        self.method = Methods()
        self.intepreter = Brainfuck( DEBUG = DEBUG, ONLY_RESULT = ONLY_RESULT, SHOW_MEMORY = SHOW_MEMORY )

        
    def compile( self, code: str ) -> str:
        code = clear_code( code = code )

        blocks = blocking( code = code )

        for block in blocks:
            self.execute( block = block )

        start_len = len( self.method.code.get_code() )
        self.method.code.code = optimizer_code( self.method.code.get_code() )
        if self.DEBUG:
            print( f"До: { start_len }      После: { len( self.method.code.get_code() ) }   ({ round( len( self.method.code.get_code() ) / start_len, 4 ) })" )

        self.intepreter.run_code( code_obj = self.method.get_code() )
        
        if self.DEBUG:
            print( '\n'.join( [ variable.__str__() for variable in Variables.memory ] ) )
                
        return self.method.get_code().get_code()


    def execute( self, block: str ) -> str:
        if re.fullmatch( r"def\[\d+\]\s*\w+", block ):
            size, name = re.match( r"def\[(\d+)\]\s+(\w+)", block ).groups()
            Variables( name = name, size = int( size ) )

        elif re.fullmatch( r"del\s*\w+", block ):
            name = re.match( r"del\s+(\w+)", block ).groups()[ 0 ]
            Variables.get_by_name( name = name ).remove()

        elif re.fullmatch( r"\w+\s*=\s*.+", block ):
            name, expression = re.match( r"(\w+)\s+=\s+(.+)", block ).groups()

            variable = Variables.get_by_name( name = name )
            temp = Variables( None, size = variable.size )

            self.expression_render( result = temp, expression = expression_blocking( block = expression ) )

            self.method.clear_variable( var = variable )
            self.method.move_variables( src = temp, dest = variable )

            temp.remove()

        return self.method.get_code()


    def expression_render( self, result: Variables, expression: list | str ):
        if type( expression ) == list:
            temp1 = Variables( name = None, size = result.size )
            temp2 = Variables( name = None, size = result.size )

            self.expression_render( result = temp1, expression = expression[ 0 ] )
            self.expression_render( result = temp2, expression = expression[ 2 ] )

            match expression[ 1 ]:
                case '+':
                    self.method.sum_variables( var1 = temp1, var2 = temp2, result = result )
                case '*':
                    self.method.multiplication_variables( var1 = temp1, var2 = temp2, result = result )

            self.method.clear_variable( temp1 )
            temp1.remove()
            self.method.clear_variable( temp2 )
            temp2.remove()

        elif re.fullmatch( r"\d+", expression ):
            value = re.match( r"(\d+)", expression ).groups()[ 0 ]
            self.method.add_value_for_variable( var = result, value = int( value ) )

        elif re.fullmatch( r"\w+", expression ):
            name = re.match( r"(\w+)", expression ).groups()[ 0 ]

            variable = Variables.get_by_name( name = name )

            self.method.copy_variables( src = variable, dest = result )

        elif re.fullmatch( r"&\w+", expression ):
            name = re.match( r"&(\w+)", expression ).groups()[ 0 ]

            variable = Variables.get_by_name( name = name )

            self.method.add_value_for_variable( var = result, value = variable.index )

        elif re.fullmatch( r"\-\w+", expression ):
            name = re.match( r"\-(\w+)", expression ).groups()[ 0 ]
            
            
            variable = Variables.get_by_name( name = name )
            temp = Variables( name = None, size = variable.size )
            self.method.add_value_for_variable( var = temp, value = 1 )

            self.method.copy_variables( src = variable, dest = result )
            self.method.invert_variable( var = result )
            self.method.sum_variables( var1 = temp, var2 = result, result = result )

            self.method.clear_variable( temp )
            temp.remove()

        else:
            print( f"Выражение не распознано: '{ expression }'" )
