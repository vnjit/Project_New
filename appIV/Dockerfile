FROM python:3.8

EXPOSE 5003

WORKDIR /appIV

COPY requirements.txt /appIV
RUN pip install  -r requirements.txt --upgrade pip

COPY . /appIV

CMD python app.py