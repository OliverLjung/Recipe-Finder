FROM python

WORKDIR /app

COPY ./requirments.txt ./requirments.txt
RUN python -m pip install -r requirments.txt

COPY ./src .

EXPOSE 80

ENTRYPOINT [ "gunicorn",  "main:app", "--port", "80"]