from simpleset.utils import classproperty


class Error( Exception ):


    @classmethod
    def define_children( cls, *child_names ):
        cls.children = []

        # create class for each child error
        for child_name in child_names:

            child_class = type(
                child_name,         # subclass name
                ( cls, ),           # superclass
                {},                 # subclass attributes
            )

            # add to parent class as attribute
            setattr( cls, child_name, child_class )

            # add to index for lookup & iteration
            cls.children.append( child_class )

        return cls.children


    @classmethod
    def define_family( cls, parent_name, *child_names ):
        parent_class = cls.define_children( parent_name )[ 0 ]
        parent_class.define_children( *child_names )
        return parent_class


    @classproperty
    def name( cls ):
        return cls.__name__


    @classproperty
    def parent( cls ):
        return cls.__bases__[ 0 ]
