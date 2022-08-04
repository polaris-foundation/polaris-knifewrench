FROM python:3.9-slim

RUN apt-get update -y && apt-get upgrade -y

# Working directory is app
WORKDIR /app

RUN apt-get update -y && apt-get upgrade -y

# Install dependencies
ADD requirements.txt .
RUN apt-get update \
    && apt-get install wait-for-it \
    && pip install -r requirements.txt


# Add the app
ADD . .

# Go go go (overridden in docker-compose.yaml)
CMD ["behave", "--no-capture"]
