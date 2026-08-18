import re

def clear_code( code: str ) -> str:
    code = code.replace( '\n', '' )

    return re.sub( r' +', ' ', code )


def blocking( code: str ) -> list[ str ]:
    open_brackets = 0
    result_blocks = []
    current_block = []

    for char in code:
        if char == ';' and open_brackets == 0:
            result_blocks.append( ''.join( current_block ) )
            current_block = []
        else:
            if char == '{':
                open_brackets += 1
            elif char == '}':
                open_brackets -= 1
            current_block.append( char )
            
    result_blocks.append( ''.join( current_block ) )
    return result_blocks


def expression_blocking( block: str ) -> list | str:
    if '(' not in block:
        return block.strip( ' ' )

    blocks = [ [], [], [] ]
    open_brackets = 0
    
    current_idx = 0 
    has_started = False

    for char in block:
        if char == '(':
            if open_brackets == 0:
                if not has_started:
                    has_started = True 
                elif current_idx == 1:
                    current_idx = 2   
            else:
                blocks[ current_idx ].append( char )
            open_brackets += 1
            
        elif char == ')':
            if open_brackets == 1:
                if current_idx == 0:
                    current_idx = 1  
                elif current_idx == 2:
                    break             
            else:
                blocks[ current_idx ].append( char )
            open_brackets -= 1
            
        else:
            if has_started:
                blocks[ current_idx ].append( char )

    b0 = ''.join( blocks[ 0 ] )
    b1 = ''.join( blocks[ 1 ] )
    b2 = ''.join( blocks[ 2 ] )

    if current_idx == 1:
        return [ b0 ]

    return [ expression_blocking( b0 ), b1.strip(), expression_blocking( b2 ) ]


def optimizer_code( code: str ):
    while '><' in code or '<>' in code and '++' in code:
        code = code.replace( '><', '' )
        code = code.replace( '<>', '' )
        code = code.replace( '++', '' )

    return code