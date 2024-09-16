import tweepy
import csv

# Twitter API credentials (replace with your credentials)
API_KEY = "dDrmTPfTBWXy7Uo23fJnl1v3l"
API_SECRET_KEY = "icgAhZlxZrDPiin2wvHoZgg8XMEXrRGIa89Imm55AnH7fGVh25"
ACCESS_TOKEN = "1829411137231732736-xDBOyerIGzlW7SfO43Km0EieOUbzab"
ACCESS_TOKEN_SECRET = "8NjvBR0fJGHUzF7v18SLJXvFW2tgA4kCmtAAnZRF0ctfI"

# Authenticate using OAuth1UserHandler
auth = tweepy.OAuth1UserHandler(
    API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
)

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
