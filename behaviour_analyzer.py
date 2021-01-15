from csv import reader
from csv_maker import make_csv
from csv_plotter import plot
from models import PostMetrics
from os import mkdir, path
from util import get_metric_name_by_input

DATASETS_FOLDER = path.join('.', 'datasets')
ANALYSIS_KEYWORDS_FOLDER_NAME = 'analysis_keywords'


class KeywordAnalyzer():

    def __init__(self, reddit, keywords: str, subreddit1: str, subreddit2: str,
                 from_date: str, to_date: str, datasets_folder: str):
        self.reddit = reddit
        self.keywords = keywords
        self.subreddit1 = subreddit1
        self.subreddit2 = subreddit2
        self.from_date = from_date
        self.to_date = to_date
        self.datasets_folder = datasets_folder

    def prepare_data(self):
        analysis_folder = path.join(self.datasets_folder,
                                    ANALYSIS_KEYWORDS_FOLDER_NAME)
        keywords_folder = path.join(analysis_folder, self.keywords)

        if not path.exists(analysis_folder):
            mkdir(analysis_folder)
        if not path.exists(keywords_folder):
            mkdir(keywords_folder)

        subreddit1_post_metrics = self.get_all_post_metrics(self.subreddit1)
        subreddit2_post_metrics = self.get_all_post_metrics(self.subreddit2)

        subreddit1_posts_with_keywords = []
        subreddit1_posts_without_keywords = []
        for post_metric in subreddit1_post_metrics:
            if self.check_post_has_keywords(getattr(post_metric, 'post_id')):
                subreddit1_posts_with_keywords.append(post_metric)
            else:
                subreddit1_posts_without_keywords.append(post_metric)
        subreddit1_with_keywords_csv = path.join(
            keywords_folder, self.subreddit1 + '_withkeywords.csv')
        subreddit1_without_keywords_csv = path.join(
            keywords_folder, self.subreddit1 + '_withoutkeywords.csv')
        make_csv(subreddit1_with_keywords_csv, subreddit1_posts_with_keywords)
        make_csv(subreddit1_without_keywords_csv,
                 subreddit1_posts_without_keywords)

        subreddit2_posts_with_keywords = []
        subreddit2_posts_without_keywords = []
        for post_metric in subreddit2_post_metrics:
            if self.check_post_has_keywords(getattr(post_metric, 'post_id')):
                subreddit2_posts_with_keywords.append(post_metric)
            else:
                subreddit2_posts_without_keywords.append(post_metric)
        subreddit2_with_keywords_csv = path.join(
            keywords_folder, self.subreddit2 + '_withkeywords.csv')
        subreddit2_without_keywords_csv = path.join(
            keywords_folder, self.subreddit2 + '_withoutkeywords.csv')
        make_csv(subreddit2_with_keywords_csv, subreddit2_posts_with_keywords)
        make_csv(subreddit2_without_keywords_csv,
                 subreddit2_posts_without_keywords)

    def get_all_post_metrics(self, subreddit: str):
        with open(path.join(self.datasets_folder, subreddit + '.csv'),
                  'r') as f:
            csv_reader = reader(f, quotechar="'", skipinitialspace=True)
            rows = list(csv_reader)
            post_metrics_list = []
            for row in rows:
                post_metrics = PostMetrics(row[0])
                setattr(post_metrics, 'subjectivity', row[1])
                setattr(post_metrics, 'followups', row[2])
                setattr(post_metrics, 'polarity', row[3])
                setattr(post_metrics, 'popularity', row[4])
                setattr(post_metrics, 'promotion', row[5])
                post_metrics_list.append(post_metrics)
        return post_metrics_list

    def check_post_has_keywords(self, post_id):
        post = self.reddit.submission(id=post_id)
        keywords = self.keywords.split(',')
        for keyword in keywords:
            if keyword in post.title or keyword in post.selftext:
                return True
        return False

    def plot_data(self, metric, keywords_folder):
        plot(
            path.join(keywords_folder, self.subreddit1 + '_withkeywords.csv'),
            metric, self.subreddit1 + ': ' + 'Posts with one or more of ' +
            self.keywords + ' and ' + get_metric_name_by_input(metric),
            'Metric: ' + get_metric_name_by_input(metric))
        plot(
            path.join(keywords_folder,
                      self.subreddit1 + '_withoutkeywords.csv'), metric,
            self.subreddit1 + ': ' + 'Posts without any of ' + self.keywords +
            ' and ' + get_metric_name_by_input(metric),
            'Metric: ' + get_metric_name_by_input(metric))
        plot(
            path.join(keywords_folder, self.subreddit2 + '_withkeywords.csv'),
            metric, self.subreddit2 + ': ' + 'Posts with one or more of ' +
            self.keywords + ' and ' + get_metric_name_by_input(metric),
            'Metric: ' + get_metric_name_by_input(metric))
        plot(
            path.join(keywords_folder,
                      self.subreddit2 + '_withoutkeywords.csv'), metric,
            self.subreddit2 + ': ' + 'Posts without any of ' + self.keywords +
            ' and ' + get_metric_name_by_input(metric),
            'Metric: ' + get_metric_name_by_input(metric))
