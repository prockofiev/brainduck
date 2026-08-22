import sys
from brainfuck import Brainfuck


class CODE_OBJ:
    CODE = ""
    FUNC = {}

    def get_code( self ):
        return self.CODE

    def get_func( self ):
        return self.FUNC


if __name__ == "__main__":
    DEBUG = False
    ONLY_RESULT = False
    SHOW_MEMORY = 100
    code_obj = CODE_OBJ()

    for i in range( 1, len( sys.argv ) ):
        if sys.argv[ i ] in [ "--debug", "-d" ]:
            DEBUG = True
        elif sys.argv[ i ] in [ "--result", "-r" ]:
            ONLY_RESULT = True
        elif sys.argv[ i ] in [ "--show", "-s" ]:
            SHOW_MEMORY = int( sys.argv[ i + 1 ] )
        elif sys.argv[ i ] in [ "--code", "-c" ]:
            code_obj.CODE = sys.argv[ i + 1 ]
    
    intepreter = Brainfuck( DEBUG = DEBUG, ONLY_RESULT = ONLY_RESULT, SHOW_MEMORY = SHOW_MEMORY )
    intepreter.run_code( code_obj = code_obj )
