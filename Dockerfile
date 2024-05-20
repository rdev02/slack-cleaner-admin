FROM python:3.9-alpine

LABEL maintainer="rdev02 <rdev02@outlook.com>"

RUN pip --no-cache-dir install slack-cleaner2

WORKDIR /opt/work
ADD remove_slack_msgs.py remove_slack_msgs.py

ENV SLACK_TOKEN=MISSING

CMD ["python", "/opt/work/remove_slack_msgs.py"]