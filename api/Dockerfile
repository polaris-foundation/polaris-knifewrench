#####
# Build the JS client
#####
FROM node:12.18.4-alpine as clientbuilder

WORKDIR /app

# Add dependencies
ADD dhos_knifewrench_ui/package.json .
ADD dhos_knifewrench_ui/yarn.lock .
ADD dhos_knifewrench_ui/tsconfig.* ./
RUN yarn install --frozen-lockfile

# Build
ADD dhos_knifewrench_ui/public ./public
ADD dhos_knifewrench_ui/src ./src
RUN yarn build

#####
# Build the microservice
#####
FROM python:3.9-slim

LABEL org.opencontainers.image.source=https://github.com/polaris-foundation/polaris-knifewrench

ENV FLASK_APP dhos_knifewrench_api/autoapp.py

WORKDIR /app

COPY poetry.lock pyproject.toml ./

RUN apt-get update \
    && apt-get install -y wait-for-it curl nano \
    && useradd -m app \
    && chown -R app:app /app \
    && pip install --upgrade pip poetry \
    && poetry config virtualenvs.create false \
    && poetry install -v --no-dev \
    && mkdir -p /app/dhos_knifewrench_api/static

# Pull in built JS client from previous Docker image
COPY --from=clientbuilder --chown=app /app/build/*.html /app/dhos_knifewrench_api/static
COPY --from=clientbuilder --chown=app /app/build/static /app/dhos_knifewrench_api/static

COPY --chown=app . ./

USER app

EXPOSE 5000

CMD ["python", "-m", "dhos_activation_auth_api"]
