FROM python

WORKDIR /app

COPY ./requirements.txt ./requirements.txt
RUN python -m pip install -r requirements.txt

COPY ./src .

EXPOSE 80

ENTRYPOINT [ "gunicorn", "-w", "2", "-b", "0.0.0.0:80", "main:app" ]