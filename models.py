class PostMetrics:

    post_id = None
    created = None
    title = None
    subjectivity = None
    followups = None
    polarity = None
    popularity = None
    promotion = None

    def __init__(self, post_id):
        self.post_id = post_id

    def __str__(self):
        return 'PostMetrics (%s, %s, %s, %s, %s, %s, %s, %s)' % (
            self.post_id, self.title, self.created, self.subjectivity,
            self.followups, self.polarity, self.popularity, self.promotion)
