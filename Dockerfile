FROM python:3.10-slim

EXPOSE 8501

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/alexraskin/f1-piston.git .

RUN pip3 install -r requirements.txt

ENTRYPOINT ["streamlit", "run", "f1_piston/Gear_Shift_Visualization.py", "--server.port=8501", "--server.address=0.0.0.0"]