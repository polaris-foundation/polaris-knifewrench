# Polaris Knife Wrench

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black) [![code style: prettier](https://img.shields.io/badge/code_style-prettier-ff69b4.svg?style=flat-square)](https://github.com/prettier/prettier)

Knife Wrench does two things:

#### Retrieves and saves messages from RabbitMQ's error queue.

This frees up RabbitMQ's memory, so the cluster isn't constantly syncing an ever-growing error queue, which provides stability.

It also allows us to diagnose the reason behind a message, which can be extremely helpful with bugfixing.

#### Allows a human to act on the errored messages

Humans can use a UI to mark a message as dealt with, and potentially resubmit it for processing as part of that.

## Knife Wrench API
This service stores details of errored AMQP messages, and can be found in the [api](api) directory.

For more details, see [api/README.md](api/README.md)

## Knife Wrench API
This service processes errored AMQP messages and POSTs them to the Knife Wrench API. It can be found in the [adapter-worker](adapter-worker) directory.

![Knife Wrench](https://media2.giphy.com/media/146myoFdrXUoGA/giphy.gif?cid=6104955e5cfa58ee30534a4c6fd5fa72&rid=giphy.gif)
