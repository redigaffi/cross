FROM python:3.13-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir poetry && poetry config virtualenvs.create false && poetry install
ENTRYPOINT ["python", "-m", "cross"]