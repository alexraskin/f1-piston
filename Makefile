.PHONY start:
.PHONY install:

start:
	poetry run streamlit run f1_piston/Gear_Shift_Visualization.py

install:
	poetry install
