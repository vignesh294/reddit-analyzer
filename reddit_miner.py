import requests
import json
from models import PostMetrics
from textblob import TextBlob


class Scraper:

    def __init__(self, reddit):
        self.reddit = reddit

    # scrape a subreddit for posts and make post metrics
    # subreddit - subreddit name
    # after & before - timestamps between when the posts must have been posted
    # limit - no of posts in this timeline to fetch
    def scrape(self, subreddit, after, before, limit):
        # since we have to get posts in a particular time period
        # have to fetch using pushshift and then praw because of https://stackoverflow.com/questions/53988619/praw-6-get-all-submission-of-a-subreddit
        url = 'https://api.pushshift.io/reddit/submission/search/'
        params = {
            'after': after,
            'before': before,
            'subreddit': subreddit,
            'limit': limit
        }
        response = json.loads(requests.get(url=url, params=params).text)
        _posts = response['data']
        posts = []
        for _post in _posts:
            posts.append(self.reddit.submission(id=_post['id']))
        return posts


class MetricCalculator:

    def __init__(self, post):
        self.post = post

    def calculate_metrics(self):
        post_body = TextBlob(self.post.selftext)
        subjectivity = post_body.subjectivity
        polarity = post_body.polarity
        followups = self.calculate_followups()
        popularity = self.calculate_popularity()
        promotion = self.calculate_promotion()
        postmetrics = PostMetrics(self.post.id)
        setattr(postmetrics, 'title', self.post.title)
        setattr(postmetrics, 'created', self.post.created)
        setattr(postmetrics, 'subjectivity', subjectivity)
        setattr(postmetrics, 'followups', followups)
        setattr(postmetrics, 'polarity', polarity)
        setattr(postmetrics, 'popularity', popularity)
        setattr(postmetrics, 'promotion', promotion)
        return postmetrics

    def calculate_followups(self):
        followups = 0
        commentsList = []
        self.post.comments.replace_more(limit=None)
        for comment in self.post.comments.list():
            commentsList.append(comment)
        for comment in commentsList:
            if (comment.author == self.post.author):
                followups = followups + 1
        return followups

    def calculate_popularity(self):
        return self.post.score + self.post.num_comments

    # a frail placeholder algorithm to determine if the post is a promotion of something
    def calculate_promotion(self):
        promotion = 0
        promotion_substrings = [
            'recommend', 'check out', 'promoted', 'Promoted'
        ]
        for promotion_substring in promotion_substrings:
            promotion = promotion + self.post.title.count(promotion_substring)
            promotion = promotion + self.post.selftext.count(
                promotion_substring)
        return promotion
