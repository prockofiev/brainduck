

class Brainfuck:
    def __init__( self, DEBUG: bool = False, ONLY_RESULT: bool = False, SHOW_MEMORY: int = -1 ):
        self.cursor: int = 0
        self.memory: list[ int ] = [ 0 ]

        self.DEBUG: bool = DEBUG
        self.ONLY_RESULT: bool = ONLY_RESULT
        self.SHOW_MEMORY: int = SHOW_MEMORY


    def run_code( self, code_obj ) -> None:
        input_stream = ''
        output_stream = ''

        code = code_obj.get_code()
        func = code_obj.get_func()

        i = 0
        while i < len( code ):

            if self.DEBUG and not self.ONLY_RESULT and func.get( i ):
                print( func.get( i )
                      )
            char = code[ i ]

            if char == '>':
                if ( self.cursor + 1 ) == len( self.memory ):
                    self.memory.append( 0 )
                self.cursor += 1
            elif char == '<':
                if self.cursor == 0:    
                    raise IndexError
                else:
                    self.cursor -= 1
            elif char == '+':
                self.memory[ self.cursor ] = ( self.memory[ self.cursor ] + 1 ) % 2
            elif char == '[':
                if not self.memory[ self.cursor ]:
                    openBrackets = 0
                    for j in range( i + 1, len( code ) ):
                        if code[ j ] == '[':
                            openBrackets += 1
                        elif code[ j ] == ']':
                            if openBrackets == 0:
                                i = j
                                break
                            else:
                                openBrackets -= 1
            elif char == ']':
                if self.memory[ self.cursor ]:
                    closeBrackets = 0
                    for j in range( i - 1, -1, -1 ):
                        if code[ j ] == ']':
                            closeBrackets += 1
                        elif code[ j ] == '[':
                            if closeBrackets == 0:
                                i = j
                                break
                            else:
                                closeBrackets -= 1
            elif char == '.':
                if len( output_stream ) == 8:
                    print( chr( int( output_stream, 2 ) ), end = '', flush = True )
                    output_stream = ''
                else:
                    output_stream += self.memory[ self.cursor ]
            elif char == ',':
                input_stream += ''.join( [ bin( ord( char ) ).zfill( 8 ) for char in input() ] )
                self.memory[ self.cursor ] = int( input_stream[ 0 ] )
                if len( input_stream ) > 1:
                    input_stream = input_stream[ 1: ]
                else:
                    input_stream = ''

            i += 1
            if self.DEBUG and not self.ONLY_RESULT:
                print( f"{ code [ i - 1 ] } " + " ".join( [ f"\033[1;31m<{ self.memory[ j ] }>\033[0m" if j == self.cursor else f"\033[2m[{ self.memory[ j ] }]\033[0m" for j in range( min( len( self.memory), self.SHOW_MEMORY ) ) ] ) )

        if self.DEBUG or self.ONLY_RESULT:
            print( " ".join( [ f"\033[1;31m<{ self.memory[ j ] }>\033[0m" if j == self.cursor else f"\033[2m[{ self.memory[ j ] }]\033[0m" for j in range( min( len( self.memory), self.SHOW_MEMORY ) ) ] ) )
