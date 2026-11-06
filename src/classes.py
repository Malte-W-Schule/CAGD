import csv
from math import sqrt

from numpy.polynomial.polynomial import polyline


# geometry.py

# ==================================================
# === C L A S S E S ===
# ==================================================

class CoordinateSystem:
    polylines = []
    beziercurves= []
    points = []

    def __init__(self):
        self.points = []
        self.polylines = []

    def addPoint(self,point:Point):
        self.points.append(point)

    def addPolyline(self, polyline:Polyline):
        self.polylines.append(polyline)

    def addBezierCurve(self, beziercurve:BezierCurve):
        self.beziercurves.append(beziercurve)

    def createPolyline(self,filename:str):
        poly = Polyline()
        poly.readFile(filename)
        self.addPolyline(poly)

    def getActivePolyline(self):
        return self.polylines[-1] # retuns last polyline

    def getActivePolylineFace(self):
        return self.polylines[-1].faces[0]

class BezierCurve:

    def __init__(self, polyline:Polyline):
        self.polyline = polyline
        self.decastel_points = []
        self.bezier_points = []
        self.t_min = -1.0
        self.t_max = 2.0

    def calcCastelPoint(self,a:Point, b:Point, t:float):
        # -1 < t < 2
        true_t = max(self.t_min,(min(self.t_max,t)))

        x = (1 - true_t) * a.x + true_t * b.x
        y = (1 - true_t) * a.y + true_t * b.y
        return Point(x,y)
        """
        # Via Vector 
        vec = sub_geoObjects(b,a)
        vec_len = skalar_multiplication(vec,true_t)
        new_point = add_geoObjects(a,vec_len)
        return new_point
        """

    def draw(self,ax,color="green",size=1):
        last_point = None
        for point in self.bezier_points:
            print(point)
            point.draw(ax,color=color,size=size)

            if last_point is not None:
                # Linie zwischen letztem und aktuellem Punkt ziehen:
                ax.plot(
                    [last_point.x, point.x],
                    [last_point.y, point.y],
                    color=color,
                    linestyle="-",
                )
            last_point = point



    def draw_castel(self, ax,t:float,size=8,color="green"):
        self.deCasteljau(t)
        for stage in self.decastel_points:
            for point in stage:
                print(point)
                point.draw(ax, color=color,size=size)



    def bezierMitdeCasteljau(self,steps=0.1):
        self.bezier_points = []
        scale = 100
        for i in range(int(self.t_min * scale),int(self.t_max*(scale)),int(steps*scale)):
            self.deCasteljau(i/scale,)
        print(f"castelLen: {len(self.bezier_points)}")


    def deCasteljau(self, t:float):
        deCastelPoints = [list(self.polyline.points)]
        #print(deCastelPoints)

        while len(deCastelPoints[-1]) > 1:
            current_points = deCastelPoints[-1]
            next_points = []

            for i in range(len(current_points) - 1): # 0 ... len-1
                current_point = current_points[i]
                next_point = current_points[i+1]

                next_points.append(self.calcCastelPoint(current_point, next_point, t))
                # i - i+1
            deCastelPoints.append(next_points)
        self.decastel_points = deCastelPoints
        #print(self.decastel_points)
        self.bezier_points.append((deCastelPoints[-1][-1]))




class GeometricObject:
    def __init__(self,x:float,y:float,z:int):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self) -> str:
        return (
            f" {type(self).__name__} X: {self.x} Y: {self.y} Z: {self.z}"
        )

class Vector(GeometricObject):
    def __init__(self, x: float, y: float):
        super().__init__(x, y, 0)

class Point(GeometricObject):
    def __init__(self, x: float, y:float):
        super().__init__(x, y, 1)

    def draw(self, ax, color="red", marker="o", size=8):
        """Zeichnet den Punkt direkt auf das übergebene Axes-Objekt."""
        ax.plot(self.x, self.y, marker=marker, color=color, markersize=size)

class Polyline:
    points = []
    faces = []

    def __init__(self):
        self.points = []
        self.faces = []

    def readFile(self, filename):
        with open(filename) as f:
            for line in f:
                if line.split()[0] == "v":
                    x = float(line.split()[1])
                    y = float(line.split()[2])
                    self.points.append(Point(x, y))
                if line.split()[0] == "f":
                    self.faces.append(self.create_face(line.split()[1:]))# cut from 1-end

    def recreateLine(self,list):
        self.points = []    # liste leeren
        self.faces = []

        face_index_list = []
        for point in list:
            self.points.append(point)
            face_index_list.append(len(self.points)-1)
        face = Face(face_index_list)
        self.faces.append(face)
        

    def __str__(self) -> str:
        # printed points list

        points_str = " [".join(str(p)+"]" for p in self.points)
        faces_str = "; ".join(str(f) for f in self.faces)

        return (
            f"=== POLYLINE ==="
            f"Points: [{points_str}\n"
            f"{faces_str}\n"
            f"================"
        )

    def lastPointIndex(self):
        return int(len(self.points)-1)

    def create_face(self,faceblueprintline:list):
        """
        Args:
            faceblueprintline: list of lines des Punk

        Return:
             Face
        """
        indexlist = []
        for element in faceblueprintline:
            indexlist.append((int(element)-1))
        return Face(indexlist)

    def addPoint(self,index:int,point:Point):
        """Fuegt einen vorhandenen Punkt anhand des Index in den Polygonzug ein.

            Args:
                index: where to insert point
                point: Point
            """
        self.points.insert(index,point)

    def addPointWithCoords(self,index:float,x:float,y:int):
        """Erstellt einen neuen Punkt und fuegt ihn anhand des Index in den Polygonzug ein.
        Args:
            index: where to insert point
            x: x value
            y: y value
        """
        self.points.insert(index,Point(x,y))

    def removePoint(self, index):
        """Löscht einen Punkt aus dem Polygonzug
        Args:
             index: index where to remove point
        """
        self.points.pop(index)

    def movePointWithVector(self,index:int,vector:Vector):
        """Addiert einen Vector auf den durch Index angegebenen Punkt
                Args:
                    index: where to insert point
                    vector: to adding Vector
        """
        self.points[index] = add_geoObjects(self.points[index],vector)

    def movePointWithCoords(self, index:int, x:float, y:float):
        """Erstellt einen Vektor und addiert ihn durch den anhand des Index angegebenen Punktes
        Args:
             index: which point to add values too
             x: x value to add to the point of index
             y: y value to add to the point of index
        """
        self.points[index] = add_geoObjects(self.points[index],Vector(x,y))

    def setPointWithCoords(self,index:int,x:float,y:float):
        """Setzt die Koordinaten des Punktes neu.
        Args:
             index: which point to set
             x: new x value
             y: new y value
        """
        self.setPointWithPoint(index,Point(x,y))

    def setPointWithPoint(self,index:int,point:Point):
        """Überschreibt die Koordinaten des Punktes neu.
        Args:
             index: which point to set
             point: new Point
        """
        self.points[index] = point

    def draw(self, ax, color="red", marker="o", size=8):

        for f in self.faces:

            last_point = None
            for index in f.indexList:
                # index
                current_point = self.points[index]
                current_point.draw(ax, color=color, marker=marker, size=size)
                if last_point is not None:
                    # Linie zwischen letztem und aktuellem Punkt ziehen:
                    ax.plot(
                        [last_point.x, current_point.x],
                        [last_point.y, current_point.y],
                        color=color,
                        linestyle="-",
                    )
                last_point = current_point


class Face:
    def __init__(self,indexList:list):
        self.indexList = indexList

    def add_index(self,index:int,value:int):
        self.indexList.insert(index,value)

    def remove_index(self,index:int):
        self.indexList.pop(index)

    def remove_value(self,value:int):
        self.indexList = [x for x in self.indexList if x != value]
        print(self.indexList)

    def __str__(self) -> str:
        # Ruft str(p) für jeden Punkt auf und trennt sie mit Zeilenumbruch
        index_str = "; ".join(str(p) for p in self.indexList)
        return (
            f"=== {type(self).__name__} ({len(self.indexList)} Points): "
            f"{index_str}"
        )


def lenght_geoObject(obj: GeometricObject):
    """"
    Args:
        obj: GeometricObject
    Returns:
        length of vector
    """
    return sqrt(obj.x ** 2 + obj.y ** 2 + obj.z ** 2)

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