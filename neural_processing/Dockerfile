FROM python:3.10

COPY requirements_nn.txt .

RUN pip install -r requirements_nn.txt

RUN apt-get update && apt-get install -y ffmpeg

RUN mkdir -p /deep_fake/np_app

WORKDIR /deep_fake/np_app

COPY . .

CMD python3 main.py