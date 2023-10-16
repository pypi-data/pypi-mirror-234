from copy import deepcopy


# non-data descriptor  (https://github.com/dssg/dickens/blob/2.0.0/src/descriptors.py)
class classproperty:

    def __init__( self, func ):
        self.__func__ = func

    def __get__( self, instance, cls=None ):
        if cls is None:
            cls = type( instance )

        return self.__func__( cls )


# read-only data descriptor
class immutable:

    def __init__( self, value ):
        self.__value__ = value

    def __get__( self, instance, cls=None ):
        return deepcopy( self.__value__ )

    def __set__( self, instance, value ):
        raise AttributeError( "cannot change value" )
