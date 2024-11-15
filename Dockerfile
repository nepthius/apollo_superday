FROM python:3.12-slim

#add user to prevent sudo commands running
RUN useradd -r -s /bin/bash anish

#set up the current env
ENV HOME /app
WORKDIR /app
ENV PATH="/app/.local/bin:${PATH}"
RUN chown -R anish:anish /app
USER anish

#set to prod
ENV FLASK_ENV=production

#arguments variables in the docker-run
ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG AWS_DEFAULT_REGION

ENV AWS_ACCESS_KEY_ID $AWS_ACCESS_KEY_ID
ENV AWS_SECRET_ACCESS_KEY $AWS_SECRET_ACCESS_KEY
ENV AWS_DEFAULT_REGION $AWS_DEFAULT_REGION

ADD ./requirements.txt ./requirements.txt

RUN pip3 install --no-cache-dir -r ./requirements.txt --user

#add other files
COPY . /app
WORKDIR /app

#startup the web server
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app", "--workers=5"]