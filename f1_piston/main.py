import fastf1
import fastf1.plotting
import streamlit as st
from matplotlib import pyplot as plt

from matplotlib.collections import LineCollection
from matplotlib import cm
import numpy as np

st.set_option("deprecation.showPyplotGlobalUse", False)

fastf1.Cache.enable_cache("./doc_cache")

class App:
    def __init__(self, year: int= 2021, grand_prix: str = "Austrian Grand Prix", session: str = "Q"):
        self.session = fastf1.get_session(year, grand_prix, session)
        self.session.load()

    def pick_fastest_lap(self):
        return self.session.laps.pick_fastest()

    def telemetry(self):
        return self.get_fastest_lap().get_telemetry()

app = App()

st.title("F1 Telemetry")
st.write("This is a demo of the F1 Telemetry data")

lap = app.pick_fastest_lap()
tel = lap.get_telemetry()


x = np.array(tel['X'].values)
y = np.array(tel['Y'].values)

points = np.array([x, y]).T.reshape(-1, 1, 2)
segments = np.concatenate([points[:-1], points[1:]], axis=1)
gear = tel['nGear'].to_numpy().astype(float)
cmap = cm.get_cmap('Paired')
lc_comp = LineCollection(segments, norm=plt.Normalize(1, cmap.N+1), cmap=cmap)
lc_comp.set_array(gear)
lc_comp.set_linewidth(4)
plt.gca().add_collection(lc_comp)
plt.axis('equal')
plt.tick_params(labelleft=False, left=False, labelbottom=False, bottom=False)

title = st.title(
    f"Fastest Lap Gear Shift Visualization\n"
    f"{lap['Driver']} - {app.session.event['EventName']} {app.session.event.year}"
)
cbar = plt.colorbar(mappable=lc_comp, label="Gear", boundaries=np.arange(1, 10))
cbar.set_ticks(np.arange(1.5, 9.5))
cbar.set_ticklabels(np.arange(1, 9))


st.pyplot(plt.show())