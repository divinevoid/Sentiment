import tweepy
import csv

# Twitter API credentials
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAALN6vwEAAAAAC%2FW00lfLqAhbWmedg0aQU%2FEXX4w%3DaYBvxPc6Isk1A18ztITlFfQ1WzD08upuqDY82y54im6GOg6qEu"

# Initialize the Twitter API client
client = tweepy.Client(bearer_token=BEARER_TOKEN)

# Define search query parameters
query = "Paralympics"  # Change to your search query
max_results_per_request = 100  # Maximum results per request
total_tweets_to_fetch = 200  # Total number of tweets you want to fetch
csv_filename = "tweets.csv"  # File to save the extracted tweets


def fetch_tweets(query, total_tweets_to_fetch):
    """Fetch tweets using the Twitter API v2."""
    fetched_tweets = 0
    next_token = None
    tweets_list = []  # List to store fetched tweets

    while fetched_tweets < total_tweets_to_fetch:
        try:
            # Fetch tweets using the search_recent_tweets method
            tweets = client.search_recent_tweets(
                query=query,
                tweet_fields=["id", "text", "created_at", "author_id", "lang"],
                max_results=min(
                    max_results_per_request, total_tweets_to_fetch - fetched_tweets
                ),
                next_token=next_token,  # For pagination
            )

            # Check if there are tweets in the response
            if tweets.data:
                for tweet in tweets.data:
                    tweet_data = {
                        "Tweet ID": tweet.id,
                        "Author ID": tweet.author_id,
                        "Created At": tweet.created_at,
                        "Text": tweet.text,
                        "Language": tweet.lang,
                    }
                    tweets_list.append(tweet_data)
                    fetched_tweets += 1

            # Update next_token for pagination
            next_token = tweets.meta.get("next_token")

            # Stop if there are no more tweets
            if not next_token:
                break

        except tweepy.TweepyException as e:
            print(f"Error: {e}")
            break

    # Save the fetched tweets to a CSV file
    save_to_csv(tweets_list, csv_filename)


def save_to_csv(tweets, filename):
    """Save the tweets data to a CSV file."""
    try:
        with open(filename, mode="a", newline="", encoding="utf-8") as csvfile:
            fieldnames = ["Tweet ID", "Author ID", "Created At", "Text", "Language"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Write headers only if the file is empty
            csvfile.seek(0)
            if csvfile.tell() == 0:
                writer.writeheader()

            # Write the tweet data
            for tweet in tweets:
                writer.writerow(tweet)

        print(f"Saved {len(tweets)} tweets to {filename}")
    except Exception as e:
        print(f"Failed to save tweets to {filename}. Error: {e}")


# Run the fetching function
fetch_tweets(query, total_tweets_to_fetch)
