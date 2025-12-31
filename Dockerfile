FROM python:3.13.11-slim

WORKDIR /app
COPY pyproject.toml ./

RUN pip install --upgrade pip
RUN pip install .

COPY . .

EXPOSE 8000

ENV PYTHONPATH=./payments

COPY seed_db.sh /seed_db.sh
RUN chmod +x /seed_db.sh

ENTRYPOINT ["/seed_db.sh"]
