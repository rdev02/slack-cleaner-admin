Removes all slack messages and files older then 1mo.

Based on [slack_cleaner2](https://github.com/sgratzl/slack_cleaner2/tree/main).

Usage
```
pip install slack_cleaner2
export SLACK_TOKEN="YOUR_SLACK_TOKEN"
export SLACK_CHANNEL=general
python remove_slack_messages.py
```
or via docker(cleans once a day)
```
docker build -t rdev02/slackcleaner:0.1 .
docker run -d -e SLACK_TOKEN="YOUR_SLACK_TOKEN" -e SLACK_CHANNEL=general rdev02/slackcleaner:0.1
```