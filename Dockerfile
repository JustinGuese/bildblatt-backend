FROM python:slim
COPY ./src/requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
COPY ./src/app.py ./app.py
CMD ["uvicorn", "app:app", "--host", "0.0.0.0"]
