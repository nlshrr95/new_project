####################
# STRUCTURAL MODEL #
####################

from besser.BUML.metamodel.structural import (
    Class, Property, Method, Parameter,
    BinaryAssociation, Generalization, DomainModel,
    Enumeration, EnumerationLiteral, Multiplicity,
    StringType, IntegerType, FloatType, BooleanType,
    TimeType, DateType, DateTimeType, TimeDeltaType,
    AnyType, Constraint, AssociationClass, Metadata, MethodImplementationType
)

# Classes
Class_ = Class(name="Class")

# Class class attributes and methods
Class__Attribute: Property = Property(name="Attribute", type=StringType)
Class_.attributes={Class__Attribute}

# Domain Model
domain_model = DomainModel(
    name="Class_Diagram",
    types={Class_},
    associations={},
    generalizations={},
    metadata=None
)
