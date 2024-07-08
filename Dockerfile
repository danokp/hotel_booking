FROM python:3.12

WORKDIR /hotel_booking

COPY pyproject.toml .
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

COPY . .

CMD ["gunicorn", "app.main:app", "--workers", "1", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]
