# main.py
# =================================
# === I M P O R T ===
# =================================
import sys
from os import remove

from matplotlib.backend_bases import MouseButton
from matplotlib.pyplot import ginput

from calculations import*
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseButton
from classes import*

# =================================
# === C O D E ===
# =================================

# ===========================================
# INIT Objects
# ===========================================
testObject = GeometricObject(1,2,3)

vector01 = Vector(1,2)

point01 = Point(2,4)
point02 = Point(3,4)
# ======================================
print("====Global Lists====")

CS = CoordinateSystem()

CS.createPolyline("testObj01.obj")

CS.addPoint(point01)
CS.addPoint(point02)

# print polyline
print(CS.getActivePolyline())

curve1 = BezierCurve(CS.getActivePolyline())
CS.addBezierCurve(curve1)

print(matplotlib.__version__)
testObject = add_geoObjects(point01, vector01)
testObject = sub_geoObjects(point02, point01)
# ===========================================
# Math Plot Erstellen
# ===========================================

# 1. Plot erstellen und sichtbar machen
fig, ax = plt.subplots()

# ===========================================
# helper functions
# ======================================

def findNearestPoint(point: Point, max_distance: float = 1.0):
    tmpPoints = CS.points.copy()
    for line in CS.polylines:
        tmpPoints.extend(line.points)

    if not tmpPoints:
        return None

    minPoint = None
    minLength = float("inf")

    # shortest distance
    for p in tmpPoints:
        richtungsvektor = sub_geoObjects(point, p)
        currentLength = lenght_geoObject(richtungsvektor)

        if currentLength < minLength:
            minLength = currentLength
            minPoint = p

    # only return if in range max_distance
    if minLength <= max_distance:
        return minPoint
    return None



# ===========================================
# interactive mathplot window
# ======================================
def redraw():
    """Zeichnet das Fenster neu und passt den Bildausschnitt an alle Punkte an (min/max +- 10)."""
    ax.cla()
    ax.grid(True, linestyle="--", alpha=0.5)

    # 1. Alle aktuell vorhandenen Punkte sammeln
    current_points = list(CS.points)
    for line in CS.polylines:
        current_points.extend(line.points)

    for bezier in CS.beziercurves:
        current_points.extend(bezier.bezier_points)

    # 2. Bounding Box berechnen (min/max +- 10)
    if current_points:
        xs = [p.x for p in current_points]
        ys = [p.y for p in current_points]

        margin = 50
        ax.set_xlim(min(xs) - margin, max(xs) + margin)
        ax.set_ylim(min(ys) - margin, max(ys) + margin)
    else:
        # Fallback, falls gar keine Punkte existieren
        ax.set_xlim(-10, 10)
        ax.set_ylim(-10, 10)

    # 3. Geometrie zeichnen
    for line in CS.polylines:
        line.draw(ax)
    for p in CS.points:
        p.draw(ax, color="blue", marker="o", size=8)

    curve1.draw(ax)
    curve1.bezierMitdeCasteljau(steps=0.2)
    curve1.draw_castel(ax,2.0,size=5,color="orange")
    curve1.draw_castel(ax,-1.0,size=5,color="pink")

    ax.set_title(
        f"Modus: {current_mode.upper()}  | [P]an [B]addPoint [A]dd  [M]ove  [D]elete  [ESC] Normal"
    )
    fig.canvas.draw_idle()


current_mode = "idle"  # Mögliche Modi: 'idle', 'add', 'addPoint' 'delete', 'move_select', 'move_place'
selected_point = None

def on_key(event):
    global current_mode, selected_point


    if event.key in ("a", "d", "m","b"):
        current_mode = event.key
        selected_point = None
        ax.set_title(f"Modus: {current_mode.upper()} - Klicke ins Fenster (Esc zum Abbrechen)")
        fig.canvas.draw_idle()
    elif event.key in ("escape","p"):
        current_mode = "idle"
        selected_point = None
        ax.set_title("Modus: Normal (Pan/Zoom aktiv)")
        fig.canvas.draw_idle()

def on_click(event):
    global current_mode, selected_point
    # Klicks ignorieren, wenn außerhalb der Achsen oder die Toolbar im Pan/Zoom-Modus ist
    if event.inaxes != ax or fig.canvas.manager.toolbar.mode != "":
        return

    clicked = Point(event.xdata, event.ydata)

    if current_mode == "b":

        CS.points.append(clicked)
        redraw()

    if current_mode == "a":
        # Zu erster Polyline hinzufügen

        if CS.polylines:

            CS.getActivePolyline().points.append(clicked)
            # index von neu hinzugefügtem punkt
            indexOfAddedPoint = CS.getActivePolyline().lastPointIndex()
            print(indexOfAddedPoint)

            print("Index in face: ", end="", flush=True)
            idx_line = int(sys.stdin.readline().strip())
            CS.getActivePolylineFace().add_index(idx_line,indexOfAddedPoint)

            redraw()

    elif current_mode == "p":
        current_mode = "idle"

    elif current_mode == "d":
        target = findNearestPoint(clicked)
        if target:
            if target in CS.points:
                CS.points.remove(target)

            line = CS.getActivePolyline()
            if target in line.points:
                idx_line = line.points.index(target)
                for f in line.faces:
                    f.remove_value(idx_line)

            redraw()

    elif current_mode == "m":
        target = findNearestPoint(clicked)
        if target:
            selected_point = target
            current_mode = "move_place"
            ax.set_title("Zielposition anklicken")
            fig.canvas.draw_idle()

    elif current_mode == "move_place":
        if selected_point:
            selected_point.x = clicked.x
            selected_point.y = clicked.y
            selected_point = None
            current_mode = "idle"
            ax.set_title("Bereit")
            redraw()

# Event-Handler verknüpfen (kein while True, kein ginput mehr nötig!)
fig.canvas.mpl_connect("key_press_event", on_key)
fig.canvas.mpl_connect("button_press_event", on_click)

redraw()
plt.show()