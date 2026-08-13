import re
from variables import Variables

def blocking( code: str ) -> list[ str ]:
    openBrackets = 0
    resultBlocks = [""]

    for char in code:
        if char == ';' and openBrackets == 0:
            resultBlocks.append( '' )
        else:
            if char == '{':
                openBrackets += 1
            elif char == '}':
                openBrackets -= 1
            resultBlocks[ -1 ] += char

    return resultBlocks


def clearCode( code: str ) -> str:
    code = code.replace( '\n', '' )

    while '  ' in code:
        code = code.replace( '  ', ' ' )

    return code


def execute( block: str ) -> str:
    result = ''
    if re.fullmatch( r"def\[\d+\]\s+\w+", block ):
        size, name = re.match( r"def\[(\d+)\]\s+(\w+)", block ).groups()
        Variables( name = name, size = int( size ) )
    elif re.fullmatch( r"del\s+\w+", block ):
        name = re.match( r"del\s+(\w+)", block ).groups()[ 0 ]
        Variables.getByName( name = name ).remove()

    return result
        

def compile( code: str, debug: bool ) -> str:
    resultCode = ""

    code = clearCode( code = code )

    blocks = blocking( code = code )

    cnt = 1
    for block in blocks:
        if debug:
            print( f"{ cnt }> { block }" )

            resultCode += execute( block = block )
        
        cnt += 1

    if debug:
        print( '\n'.join( [ variable.__str__() for variable in Variables.memory ] ) )

    return resultCode