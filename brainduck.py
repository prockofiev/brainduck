import sys
from compile import Compile
from help_output import help_output, version_output



if __name__ == "__main__":

    input_file_name = "input.bd"
    output_file_name = "output.bf"
    DEBUG = False
    ONLY_RESULT = False
    SHOW_MEMORY = 100

    for i in range( 1, len( sys.argv ) ):
        if sys.argv[ i ] in [ "--input", "-i" ]:
            input_file_name = sys.argv[ i + 1 ]
        elif sys.argv[ i ] in [ "--output", "-o" ]:
            output_file_name = sys.argv[ i + 1 ]
        elif sys.argv[ i ] in [ "--debug", "-d" ]:
            DEBUG = True
        elif sys.argv[ i ] in [ "--result", "-r" ]:
            ONLY_RESULT = True
        elif sys.argv[ i ] in [ "--show", "-s" ]:
            SHOW_MEMORY = int( sys.argv[ i + 1 ] )
        elif sys.argv[ i ] in [ "--help", "-h" ]:
            help_output()
            exit( 0 )
        elif sys.argv[ i ] in [ "--version", "-v" ]:
            version_output()
            exit( 0 )

    compile = Compile( DEBUG = DEBUG, ONLY_RESULT = ONLY_RESULT, SHOW_MEMORY = SHOW_MEMORY )
    with open( input_file_name, 'r', encoding = "utf-8" ) as file:
        result_code = compile.compile( code = file.read() )

    with open( output_file_name, 'w', encoding = "utf-8" ) as file:
        file.write( result_code )
