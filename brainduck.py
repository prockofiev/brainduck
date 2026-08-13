import sys
from helpOutput import helpOutput, versionOutput


if __name__ == "__main__":

    inputFileName = "input.bd"
    outputFileName = "output.bf"
    debug = False

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
        elif sys.argv[ i ] in [ "--version", "-v" ]:
            versionOutput()
            exit( 0 )

