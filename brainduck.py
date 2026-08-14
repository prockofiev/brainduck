import sys
from compile import compile
from helpOutput import helpOutput, versionOutput



if __name__ == "__main__":

    inputFileName = "input.bd"
    outputFileName = "output.bf"
    debug = False
    onlyResult = False

    for i in range( 1, len( sys.argv ) ):
        if sys.argv[ i ] in [ "--input", "-i" ]:
            inputFileName = sys.argv[ i + 1 ]
        elif sys.argv[ i ] in [ "--output", "-o" ]:
            outputFileName = sys.argv[ i + 1 ]
        elif sys.argv[ i ] in [ "--debug", "-d" ]:
            debug = True
        elif sys.argv[ i ] in [ "--help", "-h" ]:
            helpOutput()
            exit( 0 )
        elif sys.argv[ i ] in [ "--result", "-r" ]:
            onlyResult = True
        elif sys.argv[ i ] in [ "--version", "-v" ]:
            versionOutput()
            exit( 0 )

    with open( inputFileName, 'r', encoding = "utf-8" ) as file:
        resultCode = compile( code = file.read(), debug = debug, onlyResult = onlyResult )

    with open( outputFileName, 'w', encoding = "utf-8" ) as file:
        file.write( resultCode )
