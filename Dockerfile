FROM python:3.9-alpine

LABEL maintainer="rdev02 <rdev02@outlook.com>"

RUN pip --no-cache-dir install slack-cleaner2

ENV SLACK_TOKEN=MISSING
ENV SLACK_CHANNEL=MISSING

WORKDIR /opt/work
ADD remove_slack_msgs.py remove_slack_msgs.py

# Set the timezone to PST
RUN ln -sf /usr/share/zoneinfo/US/Pacific /etc/localtime && echo "US/Pacific" > /etc/timezone

# Add the cron job MM HH DD MM DoW
RUN echo "0 0 * * * python /opt/work/remove_slack_msgs.py" > /etc/crontabs/root
# Redirect cron logs to Docker logs
RUN ln -sf /dev/stdout /var/log/cron.log

CMD ["crond", "-f", "-l", "8"]  