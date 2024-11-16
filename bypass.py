#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
import requests
import tweepy
import json
import os
import urllib3

# Suppress SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Function to display welcome message in a border
def display_welcome_message():
    message = "Welcome to c4t[dot]FuN"
    border_length = len(message) + 4  # Adjust border size based on message length

    sys.stdout.write(f"\r+{'-' * border_length}+\n")
    sys.stdout.write(f"|  {message}  |\n")
    sys.stdout.write(f"+{'-' * border_length}+\n")
    sys.stdout.flush()

# Function to display the loading bar
def loading_bar(duration=5):
    bar_length = 20
    steps = bar_length

    for i in range(steps + 1):
        progress = (i / steps) * 100
        filled_length = int(bar_length * i / steps)
        bar = '█' * filled_length + '-' * (bar_length - filled_length)
        sys.stdout.write(f'\r[{bar}] {progress:.0f}%')
        sys.stdout.flush()
        time.sleep(duration / steps)

    sys.stdout.write(f'\r[{"█" * bar_length}] 100%\n')
    sys.stdout.flush()

# Function to display "B0t is N0w St4rt1ng" inside a border
def display_starting_message():
    message = "B0t is N0w St4rt1ng"
    border_length = len(message) + 4

    sys.stdout.write(f"\r+{'-' * border_length}+\n")
    sys.stdout.write(f"|  {message}  |\n")
    sys.stdout.write(f"+{'-' * border_length}+\n")

    print("\n◢ S34RCH1NG F0R NEW T0K3N — 🟥\n")
    print("▫ Generating ...\n")

    sys.stdout.flush()

# Display welcome message, loading bar, and starting message
display_welcome_message()
loading_bar(duration=5)
display_starting_message()

# Twitter API credentials
api_key = "csZBFuLST9nwlWUaafLmTj1me"
api_secret = "MHeVNwnSlRR0KOvyjTHULZoFUpD1pcOCtcFJ30wWVCLTZpyMYq"
bearer_token = "AAAAAAAAAAAAAAAAAAAAANidvwEAAAAABp62X75yQDG67ng1iB8RAnI07NE%3Do7JPKKRKS1fLheHJ4pVSm7D0kd343QRrExW2BneUrhkdtcbxZe"
access_token = "1608905689531056128-aQljRJiHfdSuKWuiYJ3ynE9kbIUxEu"
access_token_secret = "OvnCEhdFXZdkWdupcuIPdQUElEPuLrp4zx68C695j00hY"

client = tweepy.Client(bearer_token, api_key, api_secret, access_token, access_token_secret)
auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
api = tweepy.API(auth)

stored_tokens_file = "stored_tokens.txt"
image_file = "token_image.png"

def get_stored_tokens():
    if os.path.exists(stored_tokens_file):
        with open(stored_tokens_file, "r") as f:
            return f.read().strip()
    return ""

def update_stored_token(token):
    with open(stored_tokens_file, "w") as f:
        f.write(token)

def get_latest_token():
    url = "https://api5.splash.trade/platform-api/v1/snekfun/pools/overview?offset=0&limit=1&snekfunSortType=New"
    response = requests.get(url, verify=False)  # SSL bypass
    response.raise_for_status()  # Raise HTTP errors if any
    tokens_data = response.json()
    return tokens_data["body"][0]["pool"]["y"]["asset"]

def get_token_details(policy_id):
    details_url = f"https://api6.splash.trade/asset-info/{policy_id}.json"
    response = requests.get(details_url, verify=False)  # SSL bypass
    if response.status_code == 200:
        try:
            token_details = response.json()
            token_name = token_details.get('name')
            ticker = token_details.get('ticker', '')
            logo_cid = token_details.get('logoCid', '')
            policyid = token_details.get('policyId', '')
            image_url = f"https://snekdotfun.mypinata.cloud/ipfs/{logo_cid}" if logo_cid else None
            return token_name, ticker, image_url, policyid
        except json.JSONDecodeError:
            print(f"Error: Failed to parse JSON for policy ID {policy_id}")
    return None, None, None, None

def download_image(image_url, file_path):
    if image_url:
        response = requests.get(image_url, verify=False)  # SSL bypass
        if response.status_code == 200:
            with open(file_path, 'wb') as f:
                f.write(response.content)
            return True
    return False

def run_bot():
    while True:
        try:
            stored_token = get_stored_tokens()
            latest_token = get_latest_token()

            if latest_token and latest_token != stored_token:
                policy_id = latest_token
                token_name, ticker, image_url, policyid = get_token_details(policy_id)

                if token_name:
                    if image_url and download_image(image_url, image_file):
                        # Upload the image and tweet
                        media = api.media_upload(image_file)
                        tweet_content = (f"◢ NEW TOKEN on snekdotfun ◣"
                                         f"\n■■■■■■■■□□□\n→ Generating token metadata ...\n"
                                         f"\nName: {token_name}" 
                                         f"\nTicker: {ticker}"
                                         f"\nPolicy ID: {policyid}")
                        client.create_tweet(text=tweet_content, media_ids=[media.media_id])
                        print(f"Tweeted: {tweet_content} with image")

                        # Remove the image file after tweeting
                        os.remove(image_file)
                    else:
                        # Tweet without an image if the image cannot be downloaded
                        tweet_content = f"🚀 New Crypto Token: {token_name} ({ticker})"
                        client.create_tweet(text=tweet_content)
                        print(f"Tweeted: {tweet_content}")

                    # Update the stored token with the latest one
                    update_stored_token(latest_token)

                    # Display search message
                    print("\n◢ S34RCH1NG F0R NEW T0K3N — 🟥\n")
                    print("▫ Generating ...\n")

            # Sleep for a while before checking again (e.g., every 1 minute)
            time.sleep(60)

        except Exception as e:
            print(f"Error encountered: {e}")
            time.sleep(60)  # Wait before retrying

if __name__ == "__main__":
    run_bot()
