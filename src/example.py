import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseButton

# 1. Plot erstellen und sichtbar machen
fig, ax = plt.subplots()
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.set_title("Klicke 2 Punkte ins Fenster")
plt.draw()

# 2. Ersten Klick abfangen
print("Bitte ersten Punkt anklicken...")
punkt1 = plt.ginput(
    n=1,
    timeout=30,
    show_clicks=True,
    mouse_add=MouseButton.LEFT,
    mouse_pop=MouseButton.RIGHT,
    mouse_stop=MouseButton.MIDDLE,
)
print("Erster Punkt:", punkt1)

# 3. Zweiten Klick abfangen
print("Bitte zweiten Punkt anklicken...")
punkt2 = plt.ginput(
    n=1,
    timeout=30,
    show_clicks=True,
    mouse_add=MouseButton.LEFT,
    mouse_pop=MouseButton.RIGHT,
    mouse_stop=MouseButton.MIDDLE,
)
print("Zweiter Punkt:", punkt2)

plt.close(fig)