#!/bin/zsh

# Metadata allows the plugin to show up in the xbar app and website.
#
#  <xbar.title>Docker stats</xbar.title>
#  <xbar.version>v0.1</xbar.version>
#  <xbar.author>Tom Adamczewski</xbar.author>
#  <xbar.author.github>tadamcz</xbar.author.github>
#  <xbar.desc>Shows stats about currently running Docker containers</xbar.desc>
#  <xbar.image>https://images2.imgbox.com/e6/1a/3AEpT9sd_o.png</xbar.image>
#  <xbar.var>string(VAR_MENU_BAR_TEXT='🐳'): The text that will appear in the Menu Bar</xbar.var>

DOCKER=~/.docker/bin/docker

if ! $DOCKER --version >/dev/null 2>&1; then
    echo ⚠️$VAR_MENU_BAR_TEXT
    echo ---
    echo "Could not find docker binary at $DOCKER"
    exit
fi

echo $VAR_MENU_BAR_TEXT
echo "---"

DOCKER_STATS=$($DOCKER stats --no-stream)

# If exit code is 1, the daemon is not running
if [ $? -eq 1 ]; then
    echo "Docker daemon is not running"
    exit
fi

# Loop through each line of the docker stats output
while read -r line; do
    echo "$line" " | font='MesloLGL Nerd Font Mono' size=10"  # add `| font='MesloLGL Nerd Font Mono'`
done <<< "$DOCKER_STATS"