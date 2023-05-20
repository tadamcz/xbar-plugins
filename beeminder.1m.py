#!/usr/bin/env -S PATH="${PATH}:/opt/homebrew/bin:/usr/local/bin" python3
# -*- coding: utf-8 -*-

# Metadata allows the plugin to show up in the xbar app and website.
#
#  <xbar.title>Beeminder</xbar.title>
#  <xbar.version>v0.1</xbar.version>
#  <xbar.author>Tom Adamczewski</xbar.author>
#  <xbar.author.github>tadamcz</xbar.author.github>
#  <xbar.desc>Concisely show the status of a Beeminder goal</xbar.desc>
#  <xbar.image>https://images2.imgbox.com/8d/2d/wLOcD9sz_o.png</xbar.image>
#  <xbar.dependencies>python</xbar.dependencies>

# <xbar.var>string(VAR_AUTH_TOKEN=None): Your Beeminder auth token</xbar.var>
# <xbar.var>string(VAR_GOAL_SLUG='exercise'): Your Beeminder goal slug e.g. 'exercise' for beeminder.com/myusername/exercise</xbar.var>
# <xbar.var>string(VAR_GOAL_EMOJI='🏋️'): Emoji to represent your goal (will appear in the menu bar)</xbar.var>

import json
import os
import time
from datetime import datetime
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import urlopen

# Script-level variables
AUTH_TOKEN = os.environ["VAR_AUTH_TOKEN"]

# Check variables
if not AUTH_TOKEN:
    raise Exception("Please set your Beeminder auth token in the script variables")

# Get data

# Docs: "Since appending an access_token to the request uniquely identifies a user, you can alternatively make the request to /users/me.json (without the username)."
API_URL = f'https://www.beeminder.com/api/v1/users/me.json'
params = dict(auth_token=AUTH_TOKEN, datapoints_count=1, associations=True)
url_with_params = f'{API_URL}?{urlencode(params)}'

retries = 13
backoff_factor = 0.1
data = None

for i in range(retries):
    try:
        response = urlopen(url_with_params)
        if response.status != 200:
            raise URLError(f'Error fetching data: status {response.status}')
        data = json.loads(response.read())
        goals = data['goals']
        resolved_username = data['username']
        response_datetime = datetime.now()
        break
    except URLError as e:
        if i < retries - 1:
            time.sleep(backoff_factor * (2 ** i))
            continue
        else:
            raise Exception(f'Error fetching data: {e}')

# Select goals
chinup = next(filter(lambda goal: goal['slug'] == 'chinup', goals))
pushup = next(filter(lambda goal: goal['slug'] == 'pushup', goals))

color_emojis = {
    "green": "🟢",
    "blue": "🔵",
    "orange": "🟠",
    "red": "🔴",
}
goal_emojis = {
    "chinup": "️:muscle:",
    "pushup": ":raised_hands:",
}
goals = [chinup, pushup]


def menu_bar(goals):
    output = ""
    for goal in goals:
        goal_slug = goal["slug"]
        goal_emoji = goal_emojis[goal_slug]
        color_emoji = color_emojis[goal["roadstatuscolor"]]
        output += f'{goal_emoji}{color_emoji}'
    return output


def dropdown(goals):
    output = []
    for goal in goals:
        goal_slug = goal["slug"]
        goal_emoji = goal_emojis[goal_slug]
        color_emoji = color_emojis[goal["roadstatuscolor"]]
        message = goal['limsumdays']

        goal_url = f'https://www.beeminder.com/{resolved_username}/{goal["slug"]}'

        goal_lines = [
            "---",
            f"{goal_slug}",
            f'{goal_emoji} {color_emoji} {message}',
            f"{goal_url} | href={goal_url}",
        ]

        output.extend(goal_lines)

    return output


print(menu_bar(goals))
print("---")
print("\n".join(dropdown(goals)))
print("---")
print(f"Last updated: {response_datetime.strftime('%a %b %d %Y @ %H:%M:%S')}")  # xbar hangs sometimes
