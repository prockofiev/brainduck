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

        elif re.fullmatch( r"while\s*\(.+\)\s*\{.+\}", block ):
            head, body = re.match( r"while\s*\((.+?)\) \{(.+)\}", block ).groups()

            variable = Variables.get_by_name( name = head )
            
            condition = Variables( name = None, size = 1 )

            self.method.check_variable( var = variable, result = condition )
            self.method.set_cursor( index = condition.index )

            self.method.add_code( '[' )

            blocks = blocking( code = body )
            for block in blocks:
                self.execute( block = block.strip() )

            self.method.clear_variable( var = condition )
            self.method.check_variable( var = variable, result = condition )
            self.method.set_cursor( index = condition.index )

            self.method.add_code( ']' ) 

            condition.remove()

        elif re.fullmatch( r"if\s*\(.+\)\s*\{.+\}", block ):
            head, body = re.match( r"if\s*\((.+?)\) \{(.+)\}", block ).groups()

            variable = Variables.get_by_name( name = head )
            
            condition = Variables( name = None, size = 1 )

            self.method.check_variable( var = variable, result = condition )
            self.method.set_cursor( index = condition.index )

            self.method.add_code( '[' )

            blocks = blocking( code = body )
            for block in blocks:
                self.execute( block = block.strip() )

            self.method.clear_variable( var = condition )
            self.method.set_cursor( index = condition.index )

            self.method.add_code( ']' ) 

            condition.remove()

        elif re.fullmatch( r"\.input\s+>>\s+\w+", block ):
            name = re.match( r"\.input\s+>>\s+(\w+)", block ).groups()[ 0 ]

            variable = Variables.get_by_name( name = name )
            self.method.set_input_for_variable( var = variable )

        elif re.fullmatch( r"\.output\s+<<\s+\w+", block ):
            name = re.match( r"\.output\s+<<\s+(\w+)", block ).groups()[ 0 ]

            variable = Variables.get_by_name( name = name )
            self.method.output_for_variable( var = variable )
        
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
                case '==':
                    temp3 = Variables( name = None, size = result.size )
                    temp4 = Variables( name = None, size = result.size )
                    head = Variables( name = None, size = 1 )

                    self.method.change_the_sign_variable( var = temp2, result = temp3 )

                    self.method.sum_variables( var1 = temp1, var2 = temp3, result = temp4 )
                    self.method.check_variable( var = temp4, result = head )
                    self.method.invert_variable( var = head )
                    self.method.copy_variables( src = head, dest = result )

                    self.method.clear_variable( var = temp3 )
                    temp3.remove()
                    self.method.clear_variable( var = temp4 )
                    temp4.remove()
                    self.method.clear_variable( var = head )
                    head.remove()

                case '!=':
                    temp3 = Variables( name = None, size = result.size )
                    temp4 = Variables( name = None, size = result.size )
                    head = Variables( name = None, size = 1 )

                    self.method.change_the_sign_variable( var = temp2, result = temp3 )

                    self.method.sum_variables( var1 = temp1, var2 = temp3, result = temp4 )
                    self.method.check_variable( var = temp4, result = head )
                    self.method.copy_variables( src = head, dest = result )

                    self.method.clear_variable( var = temp3 )
                    temp3.remove()
                    self.method.clear_variable( var = temp4 )
                    temp4.remove()
                    self.method.clear_variable( var = head )
                    head.remove()

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

            self.method.change_the_sign_variable( var = variable, result = result )

        elif re.fullmatch( r'\".+\"', expression ):
            string = expression[ 1:-1 ].encode().decode('unicode_escape')

            self.method.add_value_for_variable( var = result, value = int( ''.join( [ bin( ord( char ) )[ 2: ].zfill( 8 ) for char in string ] ), 2 ) )

        else:
            print( f"Выражение не распознано: '{ expression }'" )
