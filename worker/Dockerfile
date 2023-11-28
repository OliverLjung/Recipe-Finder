FROM pytorch/pytorch

WORKDIR /app

COPY ./requirements.txt ./requirements.txt
RUN python -m pip install -r requirements.txt

COPY ./src .

EXPOSE 8000

ENTRYPOINT [ "uvicorn",  "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload" ]