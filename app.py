#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
import requests
import tweepy
import json
import os


# Function to display welcome message in a border
def display_welcome_message():
    message = "Welcome to c4t[dot]FuN"
    border_length = len(message) + 4  # Adjust border size based on message length

    # Print the message inside a border
    sys.stdout.write(f"\r+{'-' * border_length}+\n")
    sys.stdout.write(f"|  {message}  |\n")
    sys.stdout.write(f"+{'-' * border_length}+\n")
    sys.stdout.flush()


# Function to display the loading bar
def loading_bar(duration=5):
    # Total length of the loading bar
    bar_length = 20
    # Number of steps for the loading
    steps = bar_length

    for i in range(steps + 1):
        # Calculate the progress percentage
        progress = (i / steps) * 100
        # Create the loading bar
        filled_length = int(bar_length * i / steps)
        bar = '█' * filled_length + '-' * (bar_length - filled_length)
        # Print the loading bar
        sys.stdout.write(f'\r[{bar}] {progress:.0f}%')
        sys.stdout.flush()
        # Wait a bit before the next update
        time.sleep(duration / steps)

    # Ensure the loading bar reaches 100%
    sys.stdout.write(f'\r[{"█" * bar_length}] 100%\n')
    sys.stdout.flush()


# Function to display "B0t is N0w St4rt1ng" inside a border
def display_starting_message():
    message = "B0t is N0w St4rt1ng"
    border_length = len(message) + 4  # Adjust border size based on message length

    sys.stdout.write(f"\r+{'-' * border_length}+\n")
    sys.stdout.write(f"|  {message}  |\n")
    sys.stdout.write(f"+{'-' * border_length}+\n")


    print("\n◢ S34RCH1NG F0R NEW T0K3N — 🟥\n")
    print("▫ Generating ...\n")

    sys.stdout.flush()


# Display welcome message, loading bar, and starting message before running the bot
display_welcome_message()
loading_bar(duration=5)
display_starting_message()

# Twitter API credentials
api_key = "hQJON271Fe1qBZX8AzMNzVgTU"
api_secret = "qHl5QChnTwP9fqwcodtlqnUayVYkQXCP5pYJgf0W51c3ICebHI"
bearer_token = "AAAAAAAAAAAAAAAAAAAAANidvwEAAAAAlOBUWNuuA0bkN3T3zxhrOLF5pkQ%3DteSVA55Qffpj30OBsNJtzsySswbXnkj2fJz1LAkaC6Sj71Ge3K"
access_token = "1608905689531056128-zENv5oO0jINgg2iaBUkQmf46OXmDIax"
access_token_secret = "0POPIqLwerX1AOBaIROX2MJpqIXqTFp5BeDGA48BULTP6x"

# Authenticate with Twitter
client = tweepy.Client(bearer_token, api_key, api_secret, access_token, access_token_secret)
auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
api = tweepy.API(auth)

# File to store previously seen tokens
stored_tokens_file = "stored_tokens.txt"
image_file = "token_image.png"  # Temporary image file path

# Function to get previously stored tokens
def get_stored_tokens():
    if os.path.exists(stored_tokens_file):
        with open(stored_tokens_file, "r") as f:
            return f.read().strip()
    return ""

# Function to update the stored token
def update_stored_token(token):
    with open(stored_tokens_file, "w") as f:
        f.write(token)

# Function to get the latest token from the API
def get_latest_token():
    url = "https://api5.splash.trade/platform-api/v1/snekfun/pools/overview?offset=0&limit=1&snekfunSortType=New"
    response = requests.get(url)
    tokens_data = response.json()

    # Extract the asset id from "y" -> "asset" (policyId.assetNameInHex)
    latest_token = tokens_data["body"][0]["pool"]["y"]["asset"]
    return latest_token


# Function to get details of a token by policy ID
def get_token_details(policy_id):
    details_url = f"https://api6.splash.trade/asset-info/{policy_id}.json"
    response = requests.get(details_url)

    if response.status_code == 200:
        try:
            token_details = response.json()

            # Extract token name, ticker, and logoCid
            token_name = token_details.get('name')
            ticker = token_details.get('ticker', '')
            logo_cid = token_details.get('logoCid', '')
            policyid = token_details.get('policyId', '')

            # Construct the image URL
            image_url = f"https://snekdotfun.mypinata.cloud/ipfs/{logo_cid}" if logo_cid else None

            print(f"Image URL: {image_url}")  # Debugging statement
            return token_name, ticker, image_url, policyid
        except json.JSONDecodeError:
            print(f"Error: Failed to parse JSON for policy ID {policy_id}")
            return None, None, None
    elif response.status_code == 404:
        print(f"Warning: Policy ID {policy_id} not found (404 error)")
        return None, None, None
    else:
        print(f"Error: Received non-200 response code {response.status_code} for policy ID {policy_id}")
        return None, None, None


# Function to download an image from a URL
def download_image(image_url, file_path):
    if image_url:
        response = requests.get(image_url)
        if response.status_code == 200:
            with open(file_path, 'wb') as f:
                f.write(response.content)
            print(f"Image downloaded: {file_path}")  # Debugging statement
            return True
        else:
            print(f"Error: Failed to download image from {image_url} (Status Code: {response.status_code})")
            return False
    else:
        print("Error: No image URL provided")
        return False


# Main function to run the bot continuously
def run_bot():

    while True:
        # Get the previously stored token
        stored_token = get_stored_tokens()

        # Fetch the latest token from the API
        latest_token = get_latest_token()

        # Check if the latest token is different from the stored token
        if latest_token and latest_token != stored_token:
            # Extract the policy ID directly from the asset ID
            policy_id = latest_token

            # Get token details using the policyId
            token_name, ticker, image_url , policyid = get_token_details(policy_id)

            if token_name:
                # Download the image
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
                    # Tweet without image
                    tweet_content = f"🚀 New Crypto Token: {token_name} ({ticker})"
                    client.create_tweet(text=tweet_content)
                    print(f"Tweeted: {tweet_content}")

                # Update the stored token with the latest one
                update_stored_token(latest_token)

                # Add the new text in a border after tweeting
                print("\n◢ S34RCH1NG F0R NEW T0K3N — 🟥\n")
                print("▫ Generating ...\n")

        # Sleep for a while before checking again (e.g., every 1 minutes)
        time.sleep(60)

if __name__ == "__main__":
    run_bot()
