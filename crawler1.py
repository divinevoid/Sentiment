import tweepy
import csv
import json

with open("config.json") as config_file:
    config = json.load(config_file)

api_key = config["API_KEY"]
api_secret = config["API_SECRET_KEY"]
access_token = config["ACCESS_TOKEN"]
access_token_secret = config["ACCESS_TOKEN_SECRET"]
bearer_token = config["BEARER_TOKEN"]


if not bearer_token:
    print("Bearer token is missing. Please ensure it is set correctly.")
# Setting up the Tweepy client with the bearer token (used for API v2)
client = tweepy.Client(bearer_token=bearer_token)


# Function to crawl tweets by a specific query
def crawl_tweets(query, max_results=100):
    tweets = []

    # Make a search request using the Twitter API v2 search_recent_tweets endpoint
    response = client.search_recent_tweets(
        query=query,
        max_results=max_results,
        tweet_fields=["created_at", "author_id", "text", "lang"],
    )

    # Parse the response
    for tweet in response.data:
        tweet_data = {
            "tweet_id": tweet.id,
            "author_id": tweet.author_id,
            "created_at": tweet.created_at,
            "text": tweet.text,
            "lang": tweet.lang,
        }
        tweets.append(tweet_data)

    return tweets


# Function to save tweets to a CSV file
def save_tweets_to_csv(tweets, filename):
    # Specify the CSV file column names
    fieldnames = ["tweet_id", "author_id", "created_at", "text", "lang"]

    # Writing to CSV file
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Write the header (column names)
        writer.writeheader()

        # Write the rows (tweet data)
        for tweet in tweets:
            writer.writerow(tweet)


# Example usage: Crawl the most recent 100 tweets containing "Python"
if __name__ == "__main__":
    query = "Python"
    max_results = 100
    tweets = crawl_tweets(query, max_results)

    # Save the tweets to a CSV file
    csv_filename = "tweets.csv"
    save_tweets_to_csv(tweets, csv_filename)

    print(f"Saved {len(tweets)} tweets to {csv_filename}")
