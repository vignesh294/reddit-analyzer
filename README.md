# reddit-analyzer
Analyze the behaviour of reddit contributors.

Metrics posts are measured by, to understand the behaviour of the contributors in the subreddit:
Subjectivity: How much of a personal opinion, emotion or judgement is this post vs factual information, as measured by the textblob library - [0, 1].
FollowUps: How much has the op followed up on this post - number of comments by the author.
Polarity: The textblob measure of the polarity of the post - [-1, +1].
Popularity: How much attention the post has gathered - score + total number of comments on the post.
Promotion: How much this post looks like a promotion of something - occurrances of certain keywords.

Setting up:
Python - Python 3
pip install requests, praw, matplotlib, textblob
Create an app here https://www.reddit.com/prefs/apps and provide client id, client secret to user_input.json

Running:
Please follow this pattern `python reddit_analyzer.py [mode] [mode specific args]` to run.
It can be run in 3 modes:
1. Mine:
`python reddit_analyzer.py -mine subreddit after_date before_date limit`: Fetch `limit` number of posts in the `subreddit` from `before_date` to `after_date` and calculate their metrics, store as csv files in the `datasets` folder.
Examples: 
    `python reddit_analyzer.py -mine queensuniversity 30.09.2020 10.01.2021 500`
    `python reddit_analyzer.py -mine Concordia 30.09.2020 10.01.2021 500`
2. Plot
`python reddit_analyzer.py -plot subreddit1 subreddit2 after_date before_date metric`: Plot the graphs using the csv files in `datasets` which were generated for posts `before_date` to `after_date` for `subreddit1` and `subreddit2` for a `metric`.
For the `metric` field, use `1` for Subjectivity, `2` for FollowUps, `3` for Polarity, `4` for Popularity, and `5` for Promotion.
Ensure datasets are generated using the `mine` mode for the timeline and for the sureddits mentioned in this, before running this mode.
Example: `python reddit_analyzer.py -plot queensuniversity Concordia 30.09.2020 10.01.2021 2`
3. Analyze
The case analysis supported right now is the impact of certain keywords on the metrics.
a. `python reddit_analyzer.py -analyze -bykeywords -mine keywords subreddit1 subreddit2 after_date before_date`: Classify which of the posts generated in mode 1 have atleast one of the comma separated `keywords` in title or body of the posts.
Example: `python reddit_analyzer.py -analyze -bykeywords -mine online,remote queensuniversity Concordia 30.09.2020 10.01.2021`
b. `python reddit_analyzer.py -analyze -bykeywords -plot keywords subreddit1 subreddit2 after_date before_date metric`: Plot the `metric` for the data generated in 3a.
For the `metric` field, use `1` for Subjectivity, `2` for FollowUps, `3` for Polarity, `4` for Popularity, and `5` for Promotion.
Example: `python reddit_analyzer.py -analyze -bykeywords -plot online,remote queensuniversity Concordia 30.09.2020 10.01.2021 3`
