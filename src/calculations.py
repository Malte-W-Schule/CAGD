
# I M P O R T
from classes import*

def add_geoObjects(a: GeometricObject, b: GeometricObject):
    """Addiert zwei geometrische Objekte anhand ihrer Koordinaten.

    Args:
        a: first Geometric Object.
        b: second Geometric Object.

    Returns:
        Geometric Object
    """
    x = a.x + b.x
    y = a.y + b.y
    z = a.z + b.z
    return pointVector(x,y,z)

def sub_geoObjects(a: GeometricObject, b: GeometricObject) -> GeometricObject | None:
    """Subtrahiert zwei geometrische Objekte anhand ihrer Koordinaten.
    Args:
        A: Geometric Object
        B: Geometric Object

    Returns:
        Geometric Object
    """
    x = a.x - b.x
    y = a.y - b.y
    z = a.z - b.z
    return pointVector(x,y,z)

def skalar_multiplication(a:Vector,value:float):
    """Multipliziert einen Vektor mit einem Skalar
    Args:
        a: Vector
        value: float
    Returns:
        Geometric Object multiplied by value
    """
    x = a.x * value
    y = a.y * value
    z = a.z * value
    return pointVector(x,y,z)

def skalar_product(a:Vector, b:Vector):
    """Multipliziert zwei Vektoren zu einem Skalar
    Args:
        a: first Vector Object
        b: second Vector Object
    Returns:
        float:(x+y+z)
    """
    x = a.x * b.x
    y = a.y * b.y
    z = a.z * b.z
    return x + y + z

def pointVector(x,y,z):
    """ Prüft anhand der z-Koordinate, ob es sich um einen gültigen Punkt oder Vektor handelt.
    Args:
        x: float
        y: float
        z: float

    Returns:
        Vector or Point Object

    """
    if (z == 0):
        return Vector(x, y)
    if (z == 1):
        return Point(x, y)
    else:
        print("Ungültige Berechnung")
        raise ValueError(f"z-Koordinate hat den Wert: {z}")