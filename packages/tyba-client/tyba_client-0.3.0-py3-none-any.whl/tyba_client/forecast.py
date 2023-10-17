from datetime import datetime, time


class Forecast(object):
    def __init__(self, client):
        self.client = client

    def get(self, route, params=None):
        return self.client.get(f"forecasts/{route}", params=params)

    def most_recent(self, object_name: str, product: str, start_time: datetime, end_time: datetime):
        return self.get("most_recent_forecast", params={"object_name": object_name,
                                                        "product": product,
                                                        "start_time": start_time,
                                                        "end_time": end_time})

    def vintaged(self, object_name: str, product: str, start_time: datetime, end_time: datetime, days_ago: int,
                 before_time: time):
        return self.get("vintaged_forecast", params={"object_name": object_name,
                                                     "product": product,
                                                     "start_time": start_time,
                                                     "end_time": end_time,
                                                     "days_ago": days_ago,
                                                     "before_time": before_time,
                                                     })
