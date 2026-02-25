# edc2026-workshop-containerised-integration-testing

Tired of bugs only appearing in production? Or seeing your in-memory
database behave nothing like your cloud database? Learn how Testcontainers enables
integration tests that mirror real environments. Explore how to run any service, third-party
or your own, as containers for reliable, production-like testing.

## Preparation

This section describes required software and preparation prior to the workshop.

### Software requirements

- Docker Desktop (Mac/Windows) or Docker on Linux.
    - Apply for access to "Docker Desktop" in AccessIT.
    - Please verify that your Docker installation is functional. Reach out if you have issues.
- Docker Compose (provided with Docker Desktop, Linux users might need to install separately).
- Python 3.13+ installed.
    - For an easy way to manage python versions please have a look at [pyenv](https://github.com/pyenv/pyenv).

### Steps to perform before the workshop

- Ensure the software requirements are satisfied.
- Fork this repository and clone your fork to you local environment.
- Have a look at the setup in [Chapter 1](./chapter_1/README.md) and see if you can create the virtual environment.

### A note on operating systems

The choice of operating system is left to you and Windows, macOS or your favorite Linux distro should work. However, as
this workshop delves heavily into Docker please do not be surprised if we encounter some OS related issues on the way.
We will do our best to solve them when they arise.

### Contact

If you encounter issues with the preparation or have questions to the workshop please feel free to contact us (
teams/slack) and we will do our best to help out.

- Arnt Erik Stene: arnts@equinor.com
- Mariana Ricardo Santos: mrica@equinor.com
- Øystein Barth Utbjøe: outb@equinor.com

## Containerised integration testing

This workshop aims to motivate you and introduce tools that will enable you to perform integration testing of both
simple and complex software systems. The tool in focus is the [Testcontainers framework](https://testcontainers.com)
which enables us to run custom containers as part of our regular test execution. In essence, our goal is to have a
simple `pytest .` command which ultimately can spin up all your APIs, databases, message broker and anything else that
is dockerizable and enable your test to interact with the entire system.

We use python to exemplify, but the framework is available for a range of other programming languages.  

