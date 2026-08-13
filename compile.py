import re
from methods import Methods
from variables import Variables


method = Methods()


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


def expressionRender( result: Variables, expression: str ):
    if re.fullmatch( r"\d+", expression ):
        value = re.match( r"(\d+)", expression ).groups()[ 0 ]
        method.addValueForVariable( var = result, value = int( value ) )


def execute( block: str ) -> str:
    if re.fullmatch( r"def\[\d+\]\s+\w+", block ):
        size, name = re.match( r"def\[(\d+)\]\s+(\w+)", block ).groups()
        Variables( name = name, size = int( size ) )
    elif re.fullmatch( r"del\s+\w+", block ):
        name = re.match( r"del\s+(\w+)", block ).groups()[ 0 ]
        Variables.getByName( name = name ).remove()
    elif re.fullmatch( r"\w+\s+=\s+.+", block ):
        name, expression = re.match( r"(\w+)\s+=\s+(.+)", block ).groups()

        variable = Variables.getByName( name = name )
        temp = Variables( None, size = variable.size )

        expressionRender( result = temp, expression = expression )

        method.copyVariables( src = temp, dest = variable )

        temp.remove()

    return method.getCode()
        

def compile( code: str, debug: bool ) -> str:
    resultCode = ""

    code = clearCode( code = code )

    blocks = blocking( code = code )

    cnt = 1
    for block in blocks:
        if debug:
            print( f"{ cnt }> { block }" )

        method.clearCode()
        resultCode += execute( block = block )
        
        cnt += 1

    if debug:
        print( '\n'.join( [ variable.__str__() for variable in Variables.memory ] ) )

    return resultCode