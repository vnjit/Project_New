FROM python:3.8

EXPOSE 5005

WORKDIR /appVI

COPY requirements.txt /appVI
RUN pip install  -r requirements.txt --upgrade pip

COPY . /appVI

CMD python app.py