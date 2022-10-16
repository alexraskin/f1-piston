import logging
import os

import fastf1
import numpy as np
import streamlit as st
from matplotlib import cm
from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection

logging.basicConfig(level=logging.INFO)

st.set_option("deprecation.showPyplotGlobalUse", False)
st.set_page_config(
    page_title="F1 Piston Visualization",
    page_icon="🏎️",
    layout="centered",
    menu_items={
        "About": "All data is from [Fast-F1](https://github.com/theOehrly/Fast-F1)",
        "Report a bug": "https://github.com/alexraskin/f1-piston/issues",
    },
)
st.title("Fastest Lap Gear Shift Visualization 🏎️")

st.sidebar.title("Please choose from the following options")

if os.path.exists(path := "../doc_cache"):
    pass
else:
    os.mkdir(path)

fastf1.Cache.enable_cache(path)


@st.cache
def load_session(year: int, grand_prix: str, session: str):
    session = fastf1.get_session(year, grand_prix, session)
    session.load()
    return session


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
    index = 5
)

year = st.sidebar.selectbox("Select Year: ", list(range(2018, 2022)), index=1)


event = st.sidebar.selectbox(
    "Please select the Grand Prix:", fastf1.get_event_schedule(year).EventName
)

session = load_session(year, event, session_type)

with st.spinner("Building... 🔨 Please wait..."):
    try:
        lap_data = session.laps.pick_fastest()
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
            f"Driver: **{lap_data['Driver']}** - EventName: **{session.event['EventName']}** -"
            + f" EventYear: **{session.event.year}** - LapNumber: **{lap_data['LapNumber']}**"
        )
        cbar = plt.colorbar(mappable=lc_comp, label="Gear", boundaries=np.arange(1, 10))
        cbar.set_ticks(np.arange(1.5, 9.5))
        cbar.set_ticklabels(np.arange(1, 9))

        st.pyplot(plt.show())
        st.success("Built! 🏁")
    except Exception as e:
        st.error(f"An error occurred, please select another session", icon="⚠️")
        logging.error(e)
