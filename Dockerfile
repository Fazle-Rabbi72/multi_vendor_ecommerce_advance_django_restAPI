# FROM python:3.12-slim

# # Environment
# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1

# # Working directory
# WORKDIR /app

# # System dependencies
# RUN apt-get update \
#     && apt-get install -y gcc libpq-dev \
#     && apt-get clean

# # Install python dependencies
# COPY requirements.txt .
# RUN pip install --upgrade pip \
#     && apt-get install -y netcat-openbsd \
#     && pip install -r requirements.txt\
#     && pip install gunicorn

# # Copy project
# COPY . .

# # Collect static
# RUN python manage.py collectstatic --noinput

# COPY entrypoint.sh /entrypoint.sh
# RUN chmod +x /entrypoint.sh

# ENTRYPOINT ["/entrypoint.sh"]


# # Run server
# CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8000"]
# #