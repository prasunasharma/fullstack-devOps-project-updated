FROM python:3.10-slim

# Create a non-root user
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

WORKDIR /app

COPY ./app /app

# Install dependencies
RUN pip install --no-cache-dir fastapi[all] sqlalchemy psycopg2-binary

# Use non-root user
USER appuser

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000"]

