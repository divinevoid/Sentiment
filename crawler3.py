import tweepy
import csv
import json

with open("config.json") as config_file:
    config = json.load(config_file)

BEARER_TOKEN = config["BEARER_TOKEN"]
# Authenticate using OAuth1UserHandler
auth = tweepy.OAuth2BearerHandler(BEARER_TOKEN)

# Create the API object while passing in the authentication information
api = tweepy.API(auth, wait_on_rate_limit=True)


# Function to crawl tweets by a specific query
def crawl_tweets(query, count=100):
    tweets = []

    # Search for tweets using the standard API's search method
    try:
        for tweet in tweepy.Cursor(
            api.search_tweets, q=query, lang="en", tweet_mode="extended"
        ).items(count):
            tweet_data = {
                "tweet_id": tweet.id_str,
                "author_id": tweet.user.id_str,
                "created_at": tweet.created_at,
                "text": tweet.full_text,
                "lang": tweet.lang,
            }
            tweets.append(tweet_data)
    except tweepy.errors.TweepyException as e:
        print(f"Error: {e}")

    return tweets


# Function to save tweets to a CSV file
def save_tweets_to_csv(tweets, filename):
    fieldnames = ["tweet_id", "author_id", "created_at", "text", "lang"]

    # Writing to CSV file
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        # Write the rows (tweet data)
        for tweet in tweets:
            writer.writerow(tweet)


# Example usage: Crawl the most recent 100 tweets containing "Python"
if __name__ == "__main__":
    query = "Python"
    count = 100
    tweets = crawl_tweets(query, count)

    if tweets:
        # Save the tweets to a CSV file
        csv_filename = "tweets_oauth1.csv"
        save_tweets_to_csv(tweets, csv_filename)
        print(f"Saved {len(tweets)} tweets to {csv_filename}")
