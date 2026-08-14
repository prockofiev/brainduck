import re
from methods import Methods
from variables import Variables


MEM_SIZE = 256 

method = Methods( MEM_SIZE = MEM_SIZE)


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
    elif re.fullmatch( r"\w+", expression ):
        name = re.match( r"(\w+)", expression ).groups()[ 0 ]

        variable = Variables.getByName( name = name )

        method.copyVariables( src = variable, dest = result )
    elif re.fullmatch( r"&w+", expression ):
        name = re.match( r"&(\w+)", expression ).groups()[ 0 ]

        variable = Variables.getByName( name = name )

        method.addValueForVariable( var = result, value = variable.index)
    


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

        method.moveVariables( src = temp, dest = variable )

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
        runCode( resultCode )

    return resultCode


def runCode( code: str ):
    mem = [ 0 ]
    cursor = 0
    i = 0
    while i < len( code ):
        match code[ i ]:
            case '>':
                if cursor >= len( mem ) - 1:
                    mem.append( 0 )
                cursor += 1
            case '<':
                if cursor == 0:
                    raise IndexError
                cursor -= 1
            case '+':
                mem[ cursor ] = ( mem[ cursor ] + 1 ) % MEM_SIZE
            case '-':
                mem[ cursor ] -= 1
            case '[':
                if not mem[ cursor ]:
                    openBrackets = 0
                    for j in range( i + 1, len( code ) ):
                        if code[ j ] == '[':
                            openBrackets += 1
                        elif code[ j ] == ']' and openBrackets == 0:
                            i = j
                            break
                        elif code[ j ] == ']':
                            openBrackets -= 1
            case ']':
                if mem[ cursor ]:
                    closeBrackets = 0
                    for j in range( i - 1, -1, -1 ):
                        if code[ j ] == ']':
                            closeBrackets += 1
                        elif code[ j ] == '[' and closeBrackets == 0:
                            i = j
                            break
                        elif code[ j ] == '[':
                            closeBrackets -= 1
            case '.':
                print( chr( mem[ cursor ] ) )
            case ',':
                mem[ cursor ] = ord( input() )
        i += 1

        print( ''.join( [ f"<{ mem[ i ] }>" if i == cursor else f"[{ mem[ i ] }]" for i in range( len( mem ) ) ] ) )