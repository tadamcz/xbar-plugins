#!/bin/zsh

# xbar plugin script for HetrixTools uptime report

# <xbar.var>string(VAR_HETRIX_API_KEY=''): Hetrix API key </xbar.var>
# <xbar.var>string(VAR_REPORT_ID=''): Hetrix report ID</xbar.var>


# Environment variables in xBar format
API_KEY=$VAR_HETRIX_API_KEY
REPORT_ID=$VAR_REPORT_ID

# URL
URL="https://api.hetrixtools.com/v1/$API_KEY/uptime/report/$REPORT_ID/"

# Fetching data from HetrixTools API
RESPONSE=$(curl -s --fail "$URL")

# Check if the request was successful
if [ $? -ne 0 ]; then
    echo "⚠️"
    echo "---"
    echo $RESPONSE
    exit 1
fi

# Extracting the Uptime Status
JQ_PATH=/opt/homebrew/bin/jq
UPTIME_STATUS=$(echo $RESPONSE | $JQ_PATH -r '.Uptime_Status')

# Displaying appropriate icon based on Uptime Status
if [[ "$UPTIME_STATUS" == "Online" ]]; then
    echo "✨"
else
    echo "❗️"
    echo "---"
    echo $UPTIME_STATUS
fi
