import os

import fastf1
import fastf1.plotting
import numpy as np
import streamlit as st
from matplotlib import cm
from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection

st.set_option("deprecation.showPyplotGlobalUse", False)
st.set_page_config(page_title="F1 Piston", page_icon="🏎️", layout="centered")
st.title("Fastest Lap Gear Shift Visualization")
st.write("All data is from [Fast-F1](https://github.com/theOehrly/Fast-F1)")
if os.path.exists(path := "../doc_cache"):
    pass
else:
    os.mkdir(path)

fastf1.Cache.enable_cache(path)


class App:
    def __init__(
        self,
        year: int = 2021,
        grand_prix: str = "Austrian Grand Prix",
        session: str = "Q",
    ):
        self.fastf1 = fastf1
        self.session = self.fastf1.get_session(year, grand_prix, session)
        self.session.load()

    @st.cache
    def pick_fastest_lap(self):
        return self.session.laps.pick_fastest()

    @st.cache
    def telemetry(self):
        return self.get_fastest_lap().get_telemetry()

    @st.cache
    def get_drivers(self):
        return self.session.drivers

    @st.cache
    def get_driver_info(self, driver: str):
        return self.session.get_driver(driver)

    @st.cache
    def load_events(self, year: int = 2021):
        return self.fastf1.get_event_schedule(year, include_testing=False)


session_type = st.sidebar.selectbox(
    "Please select the session",
    (
        "Practice 1",
        "Practice 2",
        "Practice 3",
        "Sprint Qualifying",
        "Sprint",
        "Qualifying",
        "Race",
    ),
)

year = st.sidebar.selectbox("Select Year: ", list(range(2018, 2022)))

f1_client = App(year=year, session=session_type)

event = st.sidebar.selectbox(
    "Please select the Grand Prix:", f1_client.load_events().EventName
)

f1_client = App(year=year, grand_prix=event, session=session_type)


with st.spinner("Building Telemetry Plot..."):
    lap_data = f1_client.pick_fastest_lap()
    telemetry = lap_data.get_telemetry()

    x = np.array(telemetry["X"].values)
    y = np.array(telemetry["Y"].values)

    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    gear = telemetry["nGear"].to_numpy().astype(float)
    cmap = cm.get_cmap("Paired")
    lc_comp = LineCollection(segments, norm=plt.Normalize(1, cmap.N + 1), cmap=cmap)
    lc_comp.set_array(gear)
    lc_comp.set_linewidth(4)
    plt.gca().add_collection(lc_comp)
    plt.axis("equal")
    plt.tick_params(labelleft=False, left=False, labelbottom=False, bottom=False)

    title = st.write(
        f"Driver: **{lap_data['Driver']}** - EventName: **{f1_client.session.event['EventName']}** -"
        + f" EventYear: **{f1_client.session.event.year}** - LapNumber: **{lap_data['LapNumber']}**"
    )
    cbar = plt.colorbar(mappable=lc_comp, label="Gear", boundaries=np.arange(1, 10))
    cbar.set_ticks(np.arange(1.5, 9.5))
    cbar.set_ticklabels(np.arange(1, 9))

    st.pyplot(plt.show())
    st.success("Telemetry Plot Built!")
