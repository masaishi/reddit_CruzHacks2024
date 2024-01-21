import os
import praw
import datetime
import pandas as pd
import uuid
import time
from tqdm import tqdm
from praw.models import MoreComments
import os
import praw
import datetime
import time
from tqdm import tqdm
from praw.models import MoreComments

class RedditDataCollector:
	def __init__(self, **kwargs):
		client_id = kwargs.pop('client_id', os.environ.get('REDDIT_CLIENT_ID'))
		client_secret = kwargs.pop('client_secret', os.environ.get('REDDIT_CLIENT_SECRET'))
		user_agent = kwargs.pop('user_agent', "testscript by u/ucsc")
		subreddit_name = kwargs.pop('subreddit_name', "ucsc")

		self.reddit = praw.Reddit(
			client_id=client_id,
			client_secret=client_secret,
			user_agent=user_agent
		)
		self.subreddit = self.reddit.subreddit(subreddit_name)
		
		self.post_data = []
		self.comment_data = []

	def collect_text_data(self, limit=10, **params):
		return self._collect_data(self.subreddit.new, limit, **params)

	def collect_hot_text_data(self, limit=10, **params):
		return self._collect_data(self.subreddit.hot, limit, **params)
	
	def _expand_comments(self, containers, post_id, comment):
		if isinstance(comment, MoreComments):
			for more_comment in comment.comments():
				self._expand_comments(containers, post_id, more_comment)
		else:
			containers.append(comment.body)
			if hasattr(comment, 'replies'):
				for reply in comment.replies:
					self._expand_comments(containers, post_id, reply)

	def find_replies(self, parent_id, comment):
		if isinstance(comment, MoreComments):
			for more_comment in comment.comments():
				self.find_replies(parent_id, more_comment)
		else:

			if comment.id:
				comment_id = comment.id
			else:
				comment_id = uuid.uuid4()
			self.comment_data.append({
				'id': comment_id,
				'post_id': parent_id,
				'created': datetime.datetime.fromtimestamp(comment.created),
				'text': comment.body
			})
			if hasattr(comment, 'replies'):
				for reply in comment.replies:
					self.find_replies(parent_id, reply)

	def _collect_data(self, submission_source, limit, **params):
		for submission in tqdm(submission_source(limit=limit, params=params), total=limit):
			self.post_data.append({
				'id': submission.id,
				'url': submission.url,
				'created': datetime.datetime.fromtimestamp(submission.created),
				'title': submission.title,
				'text': submission.selftext
			})
			submission.comments.replace_more(limit=None)
			for comment in submission.comments.list():
				self.find_replies(submission.id, comment)
			
			time.sleep(1)


if __name__ == '__main__':
	collector = RedditDataCollector()
	data = collector.collect_hot_text_data(limit=10, after='1577836800', before='1735689600')
	#result_df = pd.DataFrame(data)
	#result_df.to_csv('/data/sample_row.csv', index=False)

	post_df = pd.DataFrame(collector.post_data)
	post_df.to_csv('/data/hot_posts.csv', index=False)
	comment_df = pd.DataFrame(collector.comment_data)
	comment_df.to_csv('/data/hot_comments.csv', index=False)
