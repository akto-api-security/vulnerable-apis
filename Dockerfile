FROM python:3.9
ENV PYTHONUNBUFFERED 1
RUN mkdir /vulnerable-apis
WORKDIR /vulnerable-apis
ADD . /vulnerable-apis/
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
