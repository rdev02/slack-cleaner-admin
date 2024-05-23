from slack_cleaner2 import *
import os
import requests
import json

from datetime import datetime

today = datetime.now()
print("Today:", today.strftime("%d/%m/%Y %H:%M:%S"))

def post_message_to_slack(token, channel, text):
    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    payload = {
        "channel": channel,
        "text": text
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200 and response.json()['ok']:
        print("Message posted successfully!")
        return response.json()
    else:
        print(f"Failed to post message. Status code: {response.status_code}")
        print(f"Response: {response.text}")
        return None

def clean_slack(timeBefore):
  s = SlackCleaner(os.environ["SLACK_TOKEN"])
  stats = {};

  for u in s.users:
      stats[u.id] = {
        'name': u.name,
        'removedMsg': 0,
        'failedMsg': 0,
        'removedFiles': 0,
        'failedFiles': 0
      }

  try:
    for c in s.ims:
      for msg in c.msgs(before=timeBefore, with_replies=True):
        if msg.delete() == None:
          stats[msg.user.id]['removedMsg'] += 1
        else:
          stats[msg.user.id]['failedMsg'] += 1
  except Exception as e:
    stats['errorIm'] = f'exception while deletig ims: {e}'    

  try:
    for c in s.mpim:
      for msg in c.msgs(before=timeBefore, with_replies=True):
        if msg.delete() == None:
          stats[msg.user.id]['removedMsg'] += 1
        else:
          stats[msg.user.id]['failedMsg'] += 1
  except Exception as e:
    stats['errorMpim'] = f'exception while deletig mpims: {e}'  

  try:
    for channel in s.conversations:
      for msg in channel.msgs(before=timeBefore, with_replies=True):
        if not msg.user_id:
          continue #sys messages
        if msg.delete() == None:
          stats[msg.user.id]['removedMsg'] += 1
        else:
          stats[msg.user.id]['failedMsg'] += 1
  except Exception as e:
    stats['errorConversations'] = f'exception while deletig conversations: {e}'  
  
  try:
    for file in s.files(before=a_while_ago(months=1)):
      if not file.user.id:
        continue
      if file.delete() == None:
        stats[file.user.id]['removedFiles'] += 1
      else: 
        stats[file.user.id]['failedFiles'] += 1
  except Exception as e:
    stats['errorFiles'] = f'exception while deletig files: {e}'   
  
  return stats

# Your OAuth token
oauth_token = os.environ["SLACK_TOKEN"]
report_channel_name = "#" + os.environ["SLACK_CHANNEL"]

stats = clean_slack(a_while_ago(months=1))

userStatsStr = 'removed ```';
errorString = '\nErrors:\n'
for uId in stats.keys():
  if uId.text.startswith('error'):
    errorString += stats[uId]
    continue
  uname = stats[uId]['name']
  totalmsgs = stats[uId]['removedMsg']
  totalFailedmsgs = stats[uId]['failedMsg']
  if totalmsgs == 0 and totalFailedmsgs == 0:
     print(f'skipping {uname}')
     continue

  totalFiles = stats[uId]['removedFiles']
  totalFailedFiles = stats[uId]['failedFiles']
  
  userStatsStr += f"{uname}: {totalmsgs} msgs / {totalFailedmsgs} failed; {totalFiles} files / {totalFailedFiles} failed\n" 
userStatsStr += "```" + errorString

print(userStatsStr)
post_message_to_slack(oauth_token, report_channel_name, userStatsStr)