import os
import fastf1
import streamlit as st

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
        self.session = fastf1.get_session(year, grand_prix, session)
        with st.spinner("Loading Session Data..."):
            self.session.load()
            st.success("Session Data Loaded!")

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
        return self.session.get_event_schedule(year, include_testing=False)
