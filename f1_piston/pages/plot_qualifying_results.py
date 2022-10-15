import os

import fastf1
import fastf1.plotting
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from fastf1.core import Laps
from timple.timedelta import strftimedelta

if os.path.exists(path := "../doc_cache"):
    pass
else:
    os.mkdir(path)

fastf1.Cache.enable_cache(path)

@st.experimental_memo
def load_fastf1(year: int, grand_prix: str, session: str):
    session = fastf1.get_session(year, grand_prix, session)
    session.load()
    return session

st.set_option("deprecation.showPyplotGlobalUse", False)
st.set_page_config(page_title="F1 Piston", page_icon="🏎️", layout="centered")
st.title("Qualifying results overview")
with st.spinner("Loading data..."):
    fastf1.plotting.setup_mpl(
        mpl_timedelta_support=True, color_scheme=None, misc_mpl_mods=False
    )

    session = load_fastf1(2021, "Austrian Grand Prix", "Q")
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
    st.success("Done!")
