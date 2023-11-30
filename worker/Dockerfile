FROM pytorch/pytorch

WORKDIR /app

COPY ./requirements.txt ./requirements.txt
RUN python -m pip install -r requirements.txt

COPY ./src .

ENTRYPOINT [ "uvicorn",  "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload" ]