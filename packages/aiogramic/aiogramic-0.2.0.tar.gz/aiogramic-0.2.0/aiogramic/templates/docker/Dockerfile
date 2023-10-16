FROM python:3.11.5

RUN mkdir /home/examplebot

WORKDIR /home/examplebot

COPY requirements.txt .

RUN python -m pip install -r requirements.txt

COPY . .

CMD python -m src
