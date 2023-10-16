from copy import deepcopy
import functools

from objects.utils import classproperty, immutable


# Metaclass for Object to facilitate class-level magic methods.
# Part of the Object subclass API.
# All methods accept strings (canonical_name) or objects (instances of self).
class ObjectType( type ):


    def __contains__( self, item ):
        return str( item ) in self._objdir


    def __getitem__( self, item ):
        return deepcopy( self._objdir.get( str( item ) ) )


    def __iter__( self ):
        return iter( self.all )


    def __len__( self ):
        return len( self._objdir )


@functools.total_ordering
class Object( metaclass=ObjectType ):


    ##
    ##  Object API
    ##


    @classmethod
    def define( cls, name, *args, **kwargs ):

        # create subclass
        subcls = type(
            name,                   # subclass name
            ( cls, ),               # superclass
            dict( _objdir={} ),     # subclass attributes
        )

        # create subclass instances
        subcls.populate( *args, **kwargs )

        return subcls


    ##
    ##  Object subclass API
    ##


    @classproperty
    def all( cls ):
        return deepcopy( cls._objects )


    @classproperty
    def all_cn( cls ):
        return list( cls._objdir.keys() )


    @classmethod
    def filter( cls, func ):
        assert callable( func )
        return deepcopy( [ obj for obj in cls._objects if func( obj ) ] )


    @classmethod
    def get( cls, **kwargs ):
        results = cls._select( **kwargs )
        if len( results ) != 1:
            raise ValueError( f"select( { kwargs } ) found { len( results ) } results instead of 1" )
        return deepcopy( results[ 0 ] )


    @classproperty
    def max_length( cls ):
        if cls._objects:
            return max( len( obj ) for obj in cls._objects )
        return 0


    # Form 1:  populate( "cn1", "cn2", ... )
    # Form 2:  populate( cn1=label1, cn2=label2, ... )
    # Form 3:  populate( cn1=dict( attr1=val1, attr2=val2 ), ... )
    @classmethod
    def populate( cls, *args, **kwargs ):

        # Form 1
        for arg in args:
            assert isinstance( arg, str )
            cls._create( arg )

        for cn, payload in kwargs.items():

            # Form 2
            if isinstance( payload, str ):
                cls._create( cn, label=payload )

            # Form 3
            elif isinstance( payload, dict ):
                cls._create( cn, **payload )

            else:
                raise Exception( f"invalid payload - { type( payload ) }:{ payload }" )


    @classmethod
    def select( cls, **kwargs ):
        return deepcopy( cls._select( **kwargs ) )


    ##
    ##  Instance API
    ##


    def __init__( self, canonical_name, **kwargs ):

        # set canonical name
        self.canonical_name = canonical_name

        # set arbitrary attributes
        for k, v in kwargs.items():
            setattr( self, k, v )


    def __eq__( self, other ):
        return self.canonical_name == str( other )


    def __hash__( self ):
        return hash( self.canonical_name )


    def __len__( self ):
        return len( self.canonical_name )


    def __lt__( self, other ):
        return self.canonical_name < str( other )


    def __repr__( self ):
        return self.canonical_name


    def __str__( self ):
        return self.canonical_name


    @property
    def cn( self ):
        return self.canonical_name


    @property
    def cn_lower( self ):
        return self.canonical_name.lower()


    @property
    def cn_title( self ):
        return self.canonical_name.replace( "_", " " ).title()


    @property
    def ordinal( self ):
        return self._objects.index( self ) + 1


    ##
    ##  PRIVATE
    ##


    @classmethod
    def _create( cls, canonical_name, **kwargs ):

        # create instance
        obj = cls( canonical_name, **kwargs )

        # add instance to class as attribute
        setattr( cls, canonical_name, immutable( obj ) )

        # add instance to class's object directory
        cls._objdir[ canonical_name ] = obj

        return obj


    # Returns True if all kwargs exist and all values match, else False.
    def _is_match( self, **kwargs ):
        for k, v in kwargs.items():
            if not hasattr( self, k ):
                return False
            if getattr( self, k ) != v:
                return False
        return True


    # Returns list of original objects - not copies.
    # Remember to make copies before returning from public API.
    @classproperty
    def _objects( cls ):
        return list( cls._objdir.values() )


    # Returns list of original objects - not copies.
    # Remember to make copies before returning from public API.
    @classmethod
    def _select( cls, **kwargs ):
        return [ obj for obj in cls._objects if obj._is_match( **kwargs ) ]
