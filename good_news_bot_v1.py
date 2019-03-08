import praw
import json
import requests
import tweepy
import time

#Access info for twitter.

access_token = '238504147-R4fTvJuYjxYdnRwaOFdekLXuDFwzEZB59DnLRAq4'
access_token_secret = 'NDeGZoPKwAnxeoEgeuB1fXEBpTbccDU0Y2R057oYkqfnO'
consumer_key = 'eG6VulHZjZXxcsvoxXcl97Kfh'
consumer_secret = '0P2Qv6XfuLKRnshZTwwTel6P75D01L9NAZb50bqSaSGuKHpG9j'

    
# Let's set up a connection with reddit so that we can get relevant info
# from subreddit. For this we will need various info.

def setup_connection_reddit(subreddit):
    reddit = praw.Reddit(client_id = 'S9N5wZVr87UlKQ',
                client_secret = 'cCzLUAMOVFr0Byo9FKmamkBVe6Y',
                username= 'big_arj',
                password= 'spaceinvader',
                user_agent= 'PythonGoodNewsBotv1(by/u/big_arj)')
    subreddit = reddit.subreddit(subreddit) 
    return subreddit

# Twitter does not like tweet more than 140 characters. So lets make a
# function that will truncate long tweets to only 122 characters.

def strip_title(title):
    if len(title) < 122:
        return title
    else:
        return title[:119] + "..."

# Now let's make the tweet creator. The idea behind this is storing the
# submission title and url in a dictionary, and the post ids in a list.

def tweet_creator(subreddit_info):
    post_dict = {}
    post_ids = []
    print('Good news bot getting posts from Reddit')
    for submission in subreddit_info.hot(limit=6):
        if not submission.stickied:
            post_dict[strip_title(submission.title)] = submission.url
            post_ids.append(submission.id)
        
    return post_dict, post_ids

#Append the submission ids to a text file.

def add_id_to_file(id):
    with open('posted_posts.txt', 'a') as file:
        file.write(str(id) + '\n')

#Now we read this file to check if there are no duplicates!

def duplicate_check(id):
    found = 0
    with open('posted_posts.txt', 'r') as file:
        for line in file:
            if id in line:
                found = 1
    return found
    
#    return link

def tweeter(post_dict, post_ids):

#The following three lines below are just for twitter authentication.
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth)

# Now we are iterating through the post dictionary and post ids, after
# having zipped them together. We then checking them with the text file
# containing the ids for duplicates, and appending if they are new.
# Finally, if they are new, we post them on twitter. Cool!

	for post, post_id in zip(post_dict, post_ids):
		found = duplicate_check(post_id)
		if found == 0:
			print("Good news bot is posting this link on twitter")
			print(post+" "+post_dict[post]+" #goodnews")
			api.update_status(post+" "+post_dict[post]+" #goodnews")
			add_id_to_file(post_id)
			time.sleep(30)
		else:
			print("[bot] Already posted")

#This the main function!
def main():
    subreddit = setup_connection_reddit('upliftingnews')
    post_dict, post_ids = tweet_creator(subreddit)
    tweeter(post_dict, post_ids)
	

if __name__ == '__main__':
	main()

#TODO:
# Shorten urls with goo.gl
# Add other subreddits (made_me_smile)
