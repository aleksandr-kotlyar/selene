FROM python:3.7-slim-buster

RUN apt-get update && \
    apt-get -y install sudo wget xvfb gnupg2

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' \
    && apt-get update \
    && apt-get install -y google-chrome-stable && rm -rf /var/lib/apt/lists/*
RUN sudo Xvfb -ac :99 -screen 0 1280x1024x24 > /dev/null 2>&1 &
ENV DISPLAY=:99

COPY ./ /selene
RUN python -m venv /.venv \
    && bash /.venv/bin/activate \
    && pip install poetry \
    && poetry config virtualenvs.create false \
    && cd selene \
    && poetry install
RUN rm -rf selene
ENV PATH=/.venv/bin:$PATH
