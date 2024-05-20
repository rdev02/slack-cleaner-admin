from slack_cleaner2 import *
from datetime import datetime
from collections import defaultdict
import os

s = SlackCleaner(os.environ["SLACK_TOKEN"])
stats = {};

for u in s.users:
    stats[u.id] = {
      'name': u.name,
      'messages': defaultdict(int),
      'files': 0
    }

for c in s.ims:
  for msg in c.msgs(before=a_while_ago(months=1)):
    stats[msg.user.id]['messages'][datetime.fromtimestamp(msg.ts).year] += 1

for c in s.mpim:
  for msg in c.msgs(before=a_while_ago(months=1)):
    stats[msg.user.id]['messages'][datetime.fromtimestamp(msg.ts).year] += 1

for channel in s.conversations:
  for msg in channel.msgs(before=a_while_ago(months=1), with_replies=True):
    if not msg.user_id:
      continue #sys messages
    stats[msg.user_id]['messages'][datetime.fromtimestamp(msg.ts).year] += 1
'''
for file in s.files(before=a_while_ago(months=1)):
  if not file.user_id:
    continue
  stats[file.user.id]['files'] += 1
'''
for uId in stats.keys():
  msgStr = ''
  totalmsgs = 0
  for yr in stats[uId]['messages']:
    totalmsgs += stats[uId]['messages'][yr]
    msgStr += '; ' + str(yr) + ': ' + str(stats[uId]['messages'][yr])

  msgStr = 'Total: ' + str(totalmsgs) + ' messages. ' + msgStr # + str(stats[uId]['files']) + ' files; '  + msgStr
  print(stats[uId]['name'] + ': ' + msgStr) 
'''
'''