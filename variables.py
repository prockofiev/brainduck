class Variables:
    memory = []

    def __init__( self, name: str, size: int ):
        self.name = name
        self.size = size

        for i in range( len( self.memory ) - 1 ):
            start = self.memory[ i ].index + self.memory[ i ].size
            end = self.memory[ i + 1 ].index

            if ( end - start ) >= size:
                self.index = start
                break
        else:
            if self.memory:
                self.index = self.memory[ -1 ].index + self.memory[ -1 ].size
            else:
                self.index = 0

        self.memory.append( self )

        self.memory.sort( key = lambda x: x.index )

    def remove( self ) -> None:
        self.memory.remove( self )

    @staticmethod
    def get_by_name( name: str ) -> Variables | None:
        for variable in Variables.memory:
            if variable.name == name:
                return variable

        return None

    def __str__( self ):
        return f"Name: { self.name }    Size: { self.size }    Index: { self.index }"