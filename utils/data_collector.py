from datetime import datetime, timedelta

import requests

from apps.articles.models import Article


class DataCollector:
    model = Article

    # Requests methods
    get = requests.get
    post = requests.post

    def get_time(self, from_date=None):
        today = "{0:%Y-%m-%d}".format(datetime.today())
        if from_date is not None:
            assert type(from_date) is int
            todays = "{0:%Y-%m-%d}".format(datetime.today() - timedelta(days=from_date))
            return today, todays
        return today

    def collector(self, query, *args, **kwargs):
        return

    def bulk_create(self, objs_bulk: list):
        assert [isinstance(i, self.model) for i in objs_bulk]

        objs = self.model.objects.bulk_create(objs=objs_bulk)
        return objs
