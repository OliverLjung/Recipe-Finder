FROM pytorch/pytorch

WORKDIR /app

COPY ./requirements.txt ./requirements.txt
RUN python -m pip install -r requirements.txt

RUN apt-get update
RUN apt-get install -y redis-tools

COPY ./src .

ENTRYPOINT [ "uvicorn",  "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload" ]