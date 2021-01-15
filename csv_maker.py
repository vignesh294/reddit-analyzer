def make_csv(csv_file_path, post_metrics_list):
    with open(csv_file_path, 'w') as csv_file:
        for post_metrics in post_metrics_list:
            csv_file.write(post_metrics.post_id + ",")
            csv_file.write(str(post_metrics.subjectivity) + ",")
            csv_file.write(str(post_metrics.followups) + ",")
            csv_file.write(str(post_metrics.polarity) + ",")
            csv_file.write(str(post_metrics.popularity) + ",")
            csv_file.write(str(post_metrics.promotion))
            csv_file.write('\n')
    print(str(csv_file) + ' created.')
