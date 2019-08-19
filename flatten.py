import json

def flatten(json_file):
    """
    Formats and flattens the data and creates a tweets_list
    before converting to a DataFrame.
    """
    tweets_list = []
    
    with open(json_file, 'r') as tweets: # encoding = 'utf-8'
        tweets_json = tweets.read().split("\n")
    
    # Remove empty lines
    tweets_json = list(filter(len, tweets_json))

    # Iterate through each tweet
    for tweet in tweets_json:

        # Create Python object for the tweet
        tweet_obj = json.loads(tweet)

        # Save the user screen name in 'user-screen_name'
        tweet_obj['user-screen_name'] = tweet_obj['user']['screen_name']
        
        # Check if 140+ character tweet
        if 'extended_tweet' in tweet_obj:
            # Save the extended tweet in 'extended_tweet-full_text'
            tweet_obj['extended_tweet-full_text'] = tweet_obj['extended_tweet']['full_text']
            
        # Check if a retweet
        if 'retweeted_status' in tweet_obj:
            # Save the retweet user screen name in 'retweeted_status-user-screen_name'
            tweet_obj['retweeted_status-user-screen_name'] = tweet_obj['retweeted_status']['user']['screen_name']

                # Save the retweet text in 'retweeted_status-text'
            tweet_obj['retweeted_status-text'] = tweet_obj['retweeted_status']['text']
                
            # Check if 140+ character retweet
            if 'extended_tweet' in tweet_obj['retweeted_status']:
                    
                # Save the extended retweet text
                tweet_obj['retweeted_status-extended_tweet-full_text'] = tweet_obj['retweeted_status']['extended_tweet']['full_text']
            
        # Check if a quoted tweet text
        if 'quoted_status' in tweet_obj:

            # Save the quoted tweet text
            tweet_obj['quoted_status-text'] = tweet_obj['quoted_status']['text']
                
            # Check if 140+ character quoted tweet
            if 'extended_tweet' in tweet_obj['quoted_status']:
  
                # Save the extended quoted tweet text
                tweet_obj['quoted_status-extended_tweet-full_text'] = tweet_obj['quoted_status']['extended_tweet']['full_text']
        
        if 'location' in tweet_obj['user']:
            # Save the user location
            tweet_obj['user-location'] = tweet_obj['user']['location']

        tweets_list.append(tweet_obj)
        
    return tweets_list