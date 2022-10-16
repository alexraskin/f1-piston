import logging
import os

import fastf1
import fastf1.plotting
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from fastf1.core import Laps
from timple.timedelta import strftimedelta

logging.basicConfig(level=logging.INFO)

if os.path.exists(path := "../doc_cache"):
    pass
else:
    os.mkdir(path)

fastf1.Cache.enable_cache(path)


@st.experimental_memo
def load_fastf1(
    year: int = 2021, grand_prix: str = "Austrian Grand Prix", session: str = "Q"
):
    try:
        session = fastf1.get_session(year, grand_prix, session)
        session.load()
    except Exception as e:
        st.error(f"An error occurred loading the session")
        logging.error(e)
    return session


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
st.title("Qualifying results Visualization 🏎️")
st.write("All data is from [Fast-F1](https://github.com/theOehrly/Fast-F1)")

st.sidebar.title("Please choose from the following options")


year = st.sidebar.selectbox("Select Year: ", list(range(2018, 2022)))

event = st.sidebar.selectbox(
    "Please select the Grand Prix:", fastf1.get_event_schedule(year).EventName
)

with st.spinner("Building... 🔨 Please wait..."):
    try:
        fastf1.plotting.setup_mpl(
            mpl_timedelta_support=True, color_scheme=None, misc_mpl_mods=False
        )

        session = load_fastf1(year, event)
        drivers = pd.unique(session.laps["Driver"])

        list_fastest_laps = list()
        for drv in drivers:
            drvs_fastest_lap = session.laps.pick_driver(drv).pick_fastest()
            list_fastest_laps.append(drvs_fastest_lap)
        fastest_laps = (
            Laps(list_fastest_laps).sort_values(by="LapTime").reset_index(drop=True)
        )

        pole_lap = fastest_laps.pick_fastest()
        fastest_laps["LapTimeDelta"] = fastest_laps["LapTime"] - pole_lap["LapTime"]

        team_colors = list()
        for index, lap in fastest_laps.iterlaps():
            color = fastf1.plotting.team_color(lap["Team"])
            team_colors.append(color)

        fig, ax = plt.subplots()
        ax.barh(
            fastest_laps.index,
            fastest_laps["LapTimeDelta"],
            color=team_colors,
            edgecolor="grey",
        )
        ax.set_yticks(fastest_laps.index)
        ax.set_yticklabels(fastest_laps["Driver"])

        ax.invert_yaxis()

        ax.set_axisbelow(True)
        ax.xaxis.grid(True, which="major", linestyle="--", color="black", zorder=-1000)

        lap_time_string = strftimedelta(pole_lap["LapTime"], "%m:%s.%ms")

        plt.suptitle(
            f"{session.event['EventName']} {session.event.year} Qualifying\n"
            f"Fastest Lap: {lap_time_string} ({pole_lap['Driver']})"
        )

        st.pyplot(plt.show())
        st.success("Built! 🏁")
    except Exception as e:
        st.error(f"An error occurred, please select another session", icon="⚠️")
        logging.error(e)
