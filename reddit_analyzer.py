from os import mkdir, path
from csv_maker import make_csv
from csv_plotter import plot
from behaviour_analyzer import KeywordAnalyzer
from reddit_miner import Scraper, MetricCalculator
from util import get_metric_name_by_input, get_timestamp
import csv
import json
import praw
import sys

DATASETS_FOLDER = path.join('.', 'datasets')
USER_INPUT = path.join('.', 'user_input.json')
ANALYSIS_KEYWORDS_FOLDER_NAME = 'analysis_keywords'


def check_program_params():
    if len(sys.argv) < 2:
        raise ProgramParamsException("No parameter passed.")
    mode = sys.argv[1].lower()
    if (mode == '-mine'):
        if len(sys.argv) < 6:
            raise ProgramParamsException("Missing mining critera.")
    elif mode == '-plot':
        if len(sys.argv) < 7:
            raise ProgramParamsException("Missing plotting critera.")
    elif mode == '-analyze':
        if len(sys.argv) < 9:
            raise ProgramParamsException("Missing analysis critera.")


def get_reddit():
    user_input = None
    with open(USER_INPUT, 'r') as user_input_file:
        user_input = json.loads(user_input_file.read())
    reddit = praw.Reddit(client_id=user_input['client_id'],
                         client_secret=user_input['client_secret'],
                         user_agent=user_input['user_agent'])
    return reddit


def do_mine():
    reddit = get_reddit()
    scraper = Scraper(reddit)
    subreddit = sys.argv[2]
    start_timestamp = get_timestamp(sys.argv[3])
    end_timestamp = get_timestamp(sys.argv[4])
    posts = scraper.scrape(subreddit, start_timestamp, end_timestamp,
                           sys.argv[5])
    post_metrics_list = []
    for post in posts:
        post_metrics_list.append(MetricCalculator(post).calculate_metrics())
    folder = path.join(DATASETS_FOLDER,
                       str(start_timestamp) + '_' + str(end_timestamp))
    if not path.exists(folder):
        mkdir(folder)
    csv_file = path.join(folder, subreddit + '.csv')
    make_csv(csv_file, post_metrics_list)


def do_plot():
    subreddit1 = sys.argv[2]
    subreddit2 = sys.argv[3]
    start = sys.argv[4]
    start_timestamp = get_timestamp(start)
    end = sys.argv[5]
    end_timestamp = get_timestamp(end)
    metric = int(sys.argv[6])
    if metric < 1 or metric > 5:
        raise ProgramParamsException('Invalid Metric')
    folder = path.join(DATASETS_FOLDER,
                       str(start_timestamp) + '_' + str(end_timestamp))
    subreddit_csv_1 = path.join(folder, subreddit1 + '.csv')
    subreddit_csv_2 = path.join(folder, subreddit2 + '.csv')
    if path.exists(folder) and path.isfile(subreddit_csv_1) and path.isfile(
            subreddit_csv_2):
        plot(
            subreddit_csv_1, metric,
            subreddit1 + ': ' + 'Posts and ' + get_metric_name_by_input(metric),
            'Metric: ' + get_metric_name_by_input(metric))
        plot(
            subreddit_csv_2, metric,
            subreddit2 + ': ' + 'Posts and ' + get_metric_name_by_input(metric),
            'Metric: ' + get_metric_name_by_input(metric))
    else:
        raise NotFoundError(
            str(folder) + ' or subreddit data in the folder not found.')


# check ./datasets/fromdate_todate and subreddit csvs in them already generated using `-mine` mode (Mode 1 in readme)
def check_datasets_exist(subreddit1: str, subreddit2: str, from_date: str,
                         to_date: str):
    folder_for_time_range = path.join(
        DATASETS_FOLDER,
        str(get_timestamp(from_date)) + '_' + str(get_timestamp(to_date)))
    if path.exists(DATASETS_FOLDER) and path.exists(
            folder_for_time_range) and path.isfile(
                path.join(folder_for_time_range,
                          subreddit1 + '.csv')) and path.isfile(
                              path.join(folder_for_time_range,
                                        subreddit2 + '.csv')):
        return folder_for_time_range
    else:
        raise NotFoundError('No dataset in the time range generated')


# check ./datasets/fromdate_todate/analysis_keywords/comma_separated_keywords_list and subreddit csvs in them already generated using `-analyze -bykeyword -mine` mode (Mode 3a in readme)
def check_keyword_datasets_exist(datasets_folder, keywords, subreddit1,
                                 subreddit2):
    keywords_folder = path.join(datasets_folder, ANALYSIS_KEYWORDS_FOLDER_NAME,
                                keywords)
    if path.exists(keywords_folder) and path.isfile(
            path.join(
                keywords_folder,
                subreddit1 + '_withkeywords.csv')) and path.isfile(
                    path.join(
                        keywords_folder,
                        subreddit2 + '_withkeywords.csv')) and path.isfile(
                            path.join(keywords_folder, subreddit1 +
                                      '_withoutkeywords.csv')) and path.isfile(
                                          path.join(
                                              keywords_folder, subreddit2 +
                                              '_withoutkeywords.csv')):
        return keywords_folder
    else:
        raise NotFoundError('No datasets for the keywords')


def do_case_analysis():
    if sys.argv[2].lower() == '-bykeywords':
        analysis_mode = sys.argv[3].lower()
        keywords = sys.argv[4]
        subreddit1 = sys.argv[5]
        subreddit2 = sys.argv[6]
        from_date = sys.argv[7]
        to_date = sys.argv[8]
        datasets_folder = check_datasets_exist(subreddit1, subreddit2,
                                               from_date, to_date)
        reddit = get_reddit()
        analyzer = KeywordAnalyzer(reddit, keywords, subreddit1, subreddit2,
                                   from_date, to_date, datasets_folder)
        if analysis_mode == '-mine':
            analyzer.prepare_data()
        elif analysis_mode == '-plot':
            metric = int(sys.argv[9])
            keywords_folder = check_keyword_datasets_exist(
                datasets_folder, keywords, subreddit1, subreddit2)
            analyzer.plot_data(metric, keywords_folder)
        else:
            raise NotFoundError('Invalid analysis mode')
    else:
        raise NotFoundError('Invalid analysis type')


def main():
    try:
        check_program_params()
    except ProgramParamsException as ppe:
        raise RuntimeError('Error: ' + str(ppe) + 'Please refer to readme.')
    mode = sys.argv[1].lower()
    if mode == '-mine':
        do_mine()
    if mode == '-plot':
        try:
            do_plot()
        except NotFoundError as nfe:
            raise RuntimeError('Data generated for this timeline? ' + str(nfe))
    if mode == '-analyze':
        try:
            do_case_analysis()
        except NotFoundError as nfe:
            raise RuntimeError('Data generated for this timeline? ' + str(nfe))


class ProgramParamsException(Exception):
    pass


class NotFoundError(Exception):
    pass


if __name__ == '__main__':
    main()
