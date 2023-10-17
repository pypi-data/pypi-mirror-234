# pylint: disable=too-few-public-methods,arguments-differ,import-error,too-many-arguments,too-many-locals,line-too-long, disable=useless-elif-before-else, disable=R1705, disable=R1720, disable=W1309, disable=C0103
""" Falcon Reader SDK"""
from abc import abstractmethod
from typing import List, Dict
import os
from datetime import datetime
from random import randint, random
import requests
from sdc_dp_helpers.api_utilities.retry_managers import request_handler, retry_handler


class FalconResponseInProgress(Exception):
    """Class for Falcon API call in progress """


class FalconTimeoutException(Exception):
    """Class for Ficlon timedout Exception """


class FalconQuotaException(Exception):
    """"Class for Ficlon Quota Exception """


class RequestHandler:
    """Interface for  API Call method"""
    api_calls = 0

    def __init__(self, session, creds):
        self.session: requests.Session = session
        self.base_url: str = "https://api.falcon.io/"
        self._creds = creds

    @abstractmethod
    def make_api_call(self, **kwargs):
        """Make API Call"""
        raise NotImplementedError


class FalconAPICall:
    """Class for Making API Call"""

    def __init__(self, session, creds, config):
        self.session = session
        self._creds = creds
        self.config = config
        self.channel_ids = self.get_channel_ids()
        self.start = 0
        self.curr_channels = []

    def get_channel_ids(self):
        """This gets channel ids"""
        channel_id_methods = {"v1": ChannelIdsV1, "v2": ChannelIdsV2}
        version = self.config["version"]
        if version not in channel_id_methods:
            raise KeyError(
                f"unkown value for 'version' in configs, expecting 'v1' or 'v2'. Got {version}"
            )
        channel_ids_caller = channel_id_methods[version](
            session=self.session, creds=self._creds
        )
        channel_ids = channel_ids_caller.make_api_call()

        return channel_ids

    def get_data(
        self, start_date: str, end_date: str, network: str, channel_ids: dict
    ) -> dict:
        """Gets the API Call Handler to Use"""
        endpoint_handlers = {
            "channel_insights": ChannelInsights,
            "content_insights": ContentInsights,
            "published_posts": PublishedPosts,
        }
        endpoint_name = self.config["endpoint_name"]
        if endpoint_name not in endpoint_handlers:
            raise KeyError(
                f"""
                unkown endpoint name in configs, expecting 'channel_insights',
                'content_insights' or 'published_posts'. Got {endpoint_name}
                """
            )
        endpoint_caller = endpoint_handlers[endpoint_name](
            session=self.session, creds=self._creds, config=self.config
        )
        data = endpoint_caller.get_dataset(
            start_date, end_date, network, channel_ids)

        return data


class ChannelIdsV1(RequestHandler):
    """Class for v1 channel ids"""
    @retry_handler(exceptions=FalconQuotaException, total_tries=1, should_raise=True)
    @retry_handler(exceptions=FalconTimeoutException, total_tries=5)
    @retry_handler(exceptions=ConnectionError, total_tries=5)
    def make_api_call(self, **kwargs):
        """
        Gather all available channel ids v1.
        """
        RequestHandler.api_calls += 1
        print("GET v1: channel ids. ")
        endpoint_url = f"channels?apikey={self._creds['api_key']}"
        url = f"{self.base_url}{endpoint_url}"
        response = self.session.get(url=url, params={"limit": "9999"})

        if int(response.status_code) == 200:
            response_data = response.json()
            channel_ids = set()
            for item in response_data.get("items", []):
                channel_ids.add(item["id"])

            return list(channel_ids)

        if int(response.status_code) == 429:
            if 'Retry-After' in response.headers:
                wait_time = response.headers.get(
                    'Retry-After', randint(4, 29)) * (1 + randint(2, 8) * random())
                os.environ['API_WAIT_TIME'] = str(wait_time)
                raise FalconTimeoutException(
                    f"Rolling Window Quota [429] reached. Waiting {wait_time} seconds. ")
            else:
                raise FalconQuotaException(
                    f"Falcon Quota Reached when getting channel id v1. "
                    f"Status code: {response.status_code}, Reason: {response.reason}. "
                )
        raise ConnectionError(
            f"Falcon API failed to return content id by channel ids. "
            f"Status code: {response.status_code}, Reason: {response.reason}. "
        )


class ChannelIdsV2(RequestHandler):
    """Class for v2 channel ids"""

    @retry_handler(exceptions=FalconQuotaException, total_tries=1, should_raise=True)
    @retry_handler(exceptions=FalconTimeoutException, total_tries=5)
    @retry_handler(exceptions=ConnectionError, total_tries=5)
    def make_api_call(self, **kwargs):
        """
        Gather all available channel ids v2.
        """
        RequestHandler.api_calls += 1
        print("GET v2: channel ids. ")
        endpoint_url = f"channels?apikey={self._creds['api_key']}"
        url = f"{self.base_url}{endpoint_url}"
        response = self.session.get(url=url, params={"limit": "9999"})

        if int(response.status_code) == 200:
            response_data = response.json()
            channel_ids = {}
            for item in response_data.get("items", []):
                channel_ids[item["uuid"]] = item["name"]
            return channel_ids

        if int(response.status_code) == 429:
            if 'Retry-After' in response.headers:
                wait_time = response.headers.get(
                    'Retry-After', randint(4, 29)) * (1 + randint(2, 8) * random())
                os.environ['API_WAIT_TIME'] = str(wait_time)
                raise FalconTimeoutException(
                    f"Rolling Window Quota [429] reached. Waiting {wait_time} seconds. ")
            else:
                raise FalconQuotaException(
                    f"Falcon Quota Reached when getting channel id v2. "
                    f"Status code: {response.status_code}, Reason: {response.reason}. "
                )
        raise ConnectionError(
            f"Falcon API failed to return content id by channel ids. "
            f"Status code: {response.status_code}, Reason: {response.reason}. "
        )


class ContentIdByChannelId(RequestHandler):
    """Class to get Content Ids by Channel id"""

    @retry_handler(exceptions=FalconQuotaException, total_tries=1, should_raise=True)
    @retry_handler(exceptions=FalconTimeoutException, total_tries=5)
    @retry_handler(exceptions=ConnectionError, total_tries=5, initial_wait=5)
    def make_api_call(
        self, start_date: str, end_date: str, network: str, channel_ids: Dict[str, str]
    ) -> dict:
        print("GET: content ids by channel id. ")
        date_filters = f"since={start_date}&until={end_date}"
        endpoint_url = (
            f"publish/items?apikey={self._creds['api_key']}"
            f"&statuses=published"
            f"&networks={network}"
            f"&{date_filters}"
        )
        content_ids_by_channel_id = {}
        while endpoint_url is not None:
            RequestHandler.api_calls += 1
            url = f"{self.base_url}{endpoint_url}"
            response = self.session.get(url=url)
            if int(response.status_code) == 200:
                response_data = response.json()
                for item in response_data.get("items"):
                    content_id = item.get("id")
                    channel_id = item.get("channels")
                    if channel_id is not None:
                        channel_id = channel_id[0]
                        if network == "linkedIn":
                            channel_id = channel_id.replace("-", "")
                        if channel_id in channel_ids:
                            content_ids_by_channel_id.setdefault(channel_id, []).append(
                                content_id
                            )
                endpoint_url = response_data.get(
                    "next", {"href": None}).get("href")
            elif int(response.status_code) == 429:
                if 'Retry-After' in response.headers:
                    wait_time = response.headers.get(
                        'Retry-After', randint(4, 29)) * (1 + randint(2, 8) * random())
                    os.environ['API_WAIT_TIME'] = str(wait_time)
                    raise FalconTimeoutException(
                        f"Rolling Window Quota [429] reached. Waiting {wait_time} seconds. ")
                else:
                    raise FalconQuotaException(
                        f"Falcon Quota Reached when getting content id by channel id. "
                        f"Status code: {response.status_code}, Reason: {response.reason}. "
                    )
            else:
                raise ConnectionError(
                    f"Falcon API failed to get content id by channel id. "
                    f"Status code: {response.status_code}, Reason: {response.reason}. "
                )
        return content_ids_by_channel_id


class PublishedPostsByChannelId(RequestHandler):
    """Gets the published posts by channel id"""

    @request_handler(
        wait=int(os.environ.get("REQUEST_WAIT_TIME", 2)),
        backoff_factor=float(os.environ.get("REQUEST_BACKOFF_FACTOR", 0.01)),
        backoff_method=os.environ.get("REQUEST_BACKOFF_METHOD", 0.01),
    )
    @retry_handler(exceptions=FalconQuotaException, total_tries=1, should_raise=True)
    @retry_handler(exceptions=FalconTimeoutException, total_tries=5)
    @retry_handler(exceptions=ConnectionError, total_tries=5, initial_wait=900)
    def make_api_call(
        self,
        start_date: str,
        end_date: str,
        network: str,
        channel_ids: list,
        statuses: str,
        limit: int,
        index: int,
    ) -> list:
        """Gets the published posts by channel id
        SEE: https://falconio.docs.apiary.io/
        #reference/content-api/get-content-metrics-by-channel-ids
        :param: channel_id - integer
        :param: date - string '2022-07-20' but converted to isoformat '2022-07-20T00:00:00'
        :returns: list of dictionaries
        """

        dataset: list = []
        endpoint_url: str = f"publish/items?apikey={self._creds['api_key']}"
        while endpoint_url:
            RequestHandler.api_calls += 1
            print(
                f"INFO: channel id index: {index}, "
                f"channel id: {channel_ids},  date: {start_date}, offset: {len(dataset)}. "
            )
            response = self.session.get(
                url=f"{self.base_url}{endpoint_url}",
                headers={"Content-Type": "application/json"},
                params={
                    "channels": channel_ids,
                    "since": start_date,
                    "until": end_date,
                    "networks": network,
                    "statuses": statuses,
                    "limit": limit,
                },
            )
            status_code: int = response.status_code
            reason: str = response.reason
            if int(response.status_code) == 200:
                results: dict = response.json()
                items_data: list = results.get("items", [])
                dataset.extend(items_data)

                endpoint_url = results.get("next", {"href": None}).get("href")

                if len(items_data) == 0 or endpoint_url is None:
                    break

            elif reason == "Not Found" and status_code == 404:
                print(f"No data for channel id: {channel_ids}, skipping.\n")
                break
            elif int(response.status_code) == 429:
                if 'Retry-After' in response.headers:
                    wait_time = response.headers.get(
                        'Retry-After', randint(4, 29)) * (1 + randint(2, 8) * random())
                    os.environ['API_WAIT_TIME'] = str(wait_time)
                    raise FalconTimeoutException(
                        f"Rolling Window Quota [429] reached. Waiting {wait_time} seconds. ")
                else:
                    raise FalconQuotaException(
                        f"Falcon Quota Reached when getting published posts by channel id. "
                        f"Status code: {response.status_code}, Reason: {response.reason}. "
                    )
            else:
                raise ConnectionError(
                    f"Falcon API failed to get publish post by channel id. "
                    f"Status code: {response.status_code}, Reason: {response.reason}. "
                )
        return dataset


class ContentInsightsRequestId(RequestHandler):
    """This class gets Content Insights Request Id"""

    @retry_handler(exceptions=FalconQuotaException, total_tries=1, should_raise=True)
    @retry_handler(exceptions=FalconTimeoutException, total_tries=5)
    @retry_handler(exceptions=ConnectionError, total_tries=5, initial_wait=5)
    def make_api_call(
        self,
        start_date: str,
        end_date: str,
        metric_ids: List[str],
        content_ids_by_channel_id: Dict[str, List],
    ) -> Dict[str, str]:
        RequestHandler.api_calls += 1
        print("GET: insights request id. ")
        endpoint_url = f"measure/v2/insights/content?apikey={self._creds['api_key']}"
        url = f"{self.base_url}{endpoint_url}"
        body = {
            "since": start_date,
            "until": end_date,
            "metricIds": metric_ids,
            "channels": [],
        }
        for key, value in content_ids_by_channel_id.items():
            body["channels"].append({"id": key, "contentIds": value})
        response = self.session.post(
            url=url, headers={"Content-Type": "application/json"}, json=body
        )
        # Check if we hit the rate limit

        if int(response.status_code) == 200:
            response_data = response.json()
            insights_request_id = response_data["insightsRequestId"]
            return insights_request_id
            # Check if we hit the rate limit
        elif int(response.status_code) == 429:
            if 'Retry-After' in response.headers:
                wait_time = response.headers.get(
                    'Retry-After', randint(4, 29)) * (1 + randint(2, 8) * random())
                os.environ['API_WAIT_TIME'] = str(wait_time)
                raise FalconTimeoutException(
                    f"Rolling Window Quota [429] reached. Waiting {wait_time} seconds. ")
            else:
                raise FalconQuotaException(
                    f"Falcon Quota Reached when getting content insight request ids. "
                    f"Status code: {response.status_code}, Reason: {response.reason}. "
                )
        else:
            raise ConnectionError(
                f"Falcon API failed to return content insight request ids. "
                f"Status code: {response.status_code}, Reason: {response.reason}. "
            )


class ChannelInsightsRequestId(RequestHandler):
    """This class gets Channel Insights Request Id"""

    @retry_handler(exceptions=FalconQuotaException, total_tries=1, should_raise=True)
    @retry_handler(exceptions=FalconTimeoutException, total_tries=5)
    @retry_handler(exceptions=ConnectionError, total_tries=5, initial_wait=5)
    def make_api_call(
        self,
        start_date: str,
        end_date: str,
        metric_ids: List[str],
        channel_ids: List[str],
    ) -> Dict[str, str]:
        RequestHandler.api_calls += 1
        print("GET: insights request id. ")
        start_date = datetime.strftime(
            datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%SZ"), "%Y-%m-%d"
        )
        end_date = start_date
        endpoint_url = f"measure/v2/insights/channel?apikey={self._creds['api_key']}"
        url = f"{self.base_url}{endpoint_url}"
        body = {
            "since": start_date,
            "until": end_date,
            "metricIds": metric_ids,
            "channelIds": channel_ids,
        }
        response = self.session.post(
            url=url, headers={"Content-Type": "application/json"}, json=body
        )

        # Check if we hit the rate limit

        if int(response.status_code) == 200:
            response_data = response.json()
            insights_request_id = response_data["insightsRequestId"]
            return insights_request_id
        if int(response.status_code) == 429:
            if 'Retry-After' in response.headers:
                wait_time = response.headers.get(
                    'Retry-After', randint(4, 29)) * (1 + randint(2, 8) * random())
                os.environ['API_WAIT_TIME'] = str(wait_time)
                raise FalconTimeoutException(
                    f"Rolling Window Quota [429] reached. Waiting {wait_time} seconds. ")
            else:
                raise FalconQuotaException(
                    f"Falcon Quota Reached. "
                )
        raise ConnectionError(
            f"Falcon API failed to return channel insight request ids. "
            f"Status code: {response.status_code}, Reason: {response.reason}. "
        )


class Insights(RequestHandler):
    """This class gets insights data"""

    @retry_handler(exceptions=FalconResponseInProgress, total_tries=5, initial_wait=5)
    @retry_handler(exceptions=FalconQuotaException, total_tries=1, should_raise=True)
    @retry_handler(exceptions=FalconTimeoutException, total_tries=5)
    @retry_handler(exceptions=ConnectionError, total_tries=5, initial_wait=5)
    def make_api_call(self, insights_request_id: Dict[str, str] = None):
        RequestHandler.api_calls += 1
        print("GET: insights. ")
        endpoint_url = (
            f"measure/v2/insights/{insights_request_id}?apikey={self._creds['api_key']}"
        )
        url = f"{self.base_url}{endpoint_url}"
        response = self.session.get(url=url)
        response_data = response.json()
        if int(response.status_code) == 200:
            response_data = response.json()
            if response_data["status"] == "READY":
                return response_data
            elif response_data["status"] == "IN_PROGRESS":
                raise FalconResponseInProgress(
                    f"Response for Insights is {response_data['status']}. "
                )
            else:
                # Data is not ready.
                raise ConnectionError(
                    f"Falcon API failed to return content ids. "
                    f"Status code: {response.status_code}, Reason: Response status is {response_data['status']}. "
                )
        # Check if we hit the rate limit
        elif int(response.status_code) == 429:
            if 'Retry-After' in response.headers:
                wait_time = response.headers.get(
                    'Retry-After', randint(4, 29)) * (1 + randint(2, 8) * random())
                os.environ['API_WAIT_TIME'] = str(wait_time)
                raise FalconTimeoutException(
                    f"Rolling Window Quota [429] reached. Waiting {wait_time} seconds. ")
            else:
                raise FalconQuotaException(
                    f"Falcon Quota Reached when calling Insights. "
                    f"Status code: {response.status_code}, Reason: {response.reason}. "
                )
        else:
            raise ConnectionError(
                f"Falcon API failed to return insights. "
                f"Status code: {response.status_code}, Reason: {response.reason}. "
            )


class ContentInsights(FalconAPICall):
    """This class  gets content insights and normalises the data"""

    @staticmethod
    def _normalize_data(dataset: dict, network: str, channel_ids: dict) -> List[Dict]:
        temp = {}

        for metric, data_items in dataset.items():
            if not data_items:
                # if we have nothing in value
                continue
            for data in data_items:
                data[metric] = data.pop("value")
                data["network"] = network
                data["brand"] = channel_ids.get(data["channelId"], None)
                check_point = tuple(
                    map(data.get, ["channelId", "date", "contentId"]))
                if not temp.get(check_point):
                    temp[check_point] = data
                else:
                    missing_keys = set(data).difference(set(temp[check_point]))
                    # flatten
                    for key in missing_keys:
                        temp[check_point].update({key: data[key]})
        normalized_data = list(temp.values())
        return normalized_data

    def insights_handler(
        self,
        **kwargs,
    ):
        insights_requests_handler = ContentInsightsRequestId(
            creds=self._creds, session=self.session
        )
        insights_request_id = insights_requests_handler.make_api_call(**kwargs)
        results = Insights(
            creds=self._creds, session=self.session
        ).make_api_call(insights_request_id)
        if results is None or results.get("data") is None:
            insights_request_id = insights_requests_handler.make_api_call(
                **kwargs)
            results = Insights(
                creds=self._creds, session=self.session
            ).make_api_call(insights_request_id)

        return results

    def get_dataset(
        self, start_date: str, end_date: str, network: str, channel_ids: dict
    ) -> dict:
        """Fucntion handles content insights query"""
        channel_steps = self.config.get("channel_steps", 10)
        content_steps = self.config.get("content_steps", 250)
        metric_ids = self.config["metrics"]
        content_ids_by_channel_id = ContentIdByChannelId(
            creds=self._creds, session=self.session
        ).make_api_call(
            start_date=start_date,
            end_date=end_date,
            network=network,
            channel_ids=channel_ids,
        )
        if content_ids_by_channel_id is None:
            raise ConnectionError("Failed to get content id by channel id")
        channels = list(content_ids_by_channel_id.keys())
        channel_id_length = len(channels)
        dataset = []
        data = []
        for _ in range(0, channel_id_length, channel_steps):
            self.curr_channels = channels[self.start: self.start + channel_steps]
            request_content_ids_by_channel_id = {
                key: value
                for key, value in content_ids_by_channel_id.items()
                if key in self.curr_channels
            }

            for key, value in request_content_ids_by_channel_id.items():
                content_ids_length = len(value)
                start = 0
                curr_content_ids = []
                curr_request_content_ids_by_channel_id = {}
                for _ in range(0, content_ids_length, content_steps):
                    curr_content_ids = value[start: start + content_steps]
                    curr_request_content_ids_by_channel_id[key] = curr_content_ids
                    if len(curr_request_content_ids_by_channel_id) < 1:
                        continue
                    results = self.insights_handler(
                        start_date=start_date,
                        end_date=end_date,
                        metric_ids=metric_ids,
                        content_ids_by_channel_id=curr_request_content_ids_by_channel_id,
                    )
                    if results is not None:
                        data = results["data"].get("insights")
                        if data is not None:
                            dataset.extend(self._normalize_data(
                                data, network, channel_ids))
                start = start + content_steps
            self.start = self.start + channel_steps
        return dataset


class ChannelInsights(FalconAPICall):
    """This class  gets channel insights and normalises the data"""

    @staticmethod
    def _normalize_data(dataset: dict, network: str, channel_ids: dict) -> List[Dict]:
        templist = []

        for metric, data_items in dataset.items():
            if not data_items:
                # if we have nothing in value
                continue
            for data in data_items:
                data[metric] = data.pop("value")
                data["network"] = network
                data["brand"] = channel_ids.get(data["channelId"], None)
                templist.append(data)
        normalized_data = templist

        return normalized_data

    def get_dataset(
        self, start_date: str, end_date: str, network: str, channel_ids: dict
    ) -> dict:
        """Fucntion handles channel insights query"""
        channels = list(channel_ids.keys())
        channel_id_length = len(channels)
        channel_steps = self.config.get("channel_steps", 10)
        metric_ids = self.config["metrics"]
        dataset = []
        data = []
        for _ in range(0, channel_id_length, channel_steps):
            self.curr_channels = channels[self.start: self.start + channel_steps]
            insights_request_id = ChannelInsightsRequestId(
                creds=self._creds, session=self.session
            ).make_api_call(
                start_date=start_date,
                end_date=end_date,
                metric_ids=metric_ids,
                channel_ids=self.curr_channels,
            )
            results = Insights(creds=self._creds, session=self.session).make_api_call(
                insights_request_id
            )
            if results is None:
                insights_request_id = ChannelInsightsRequestId(
                    creds=self._creds, session=self.session
                ).make_api_call(
                    start_date=start_date,
                    end_date=end_date,
                    metric_ids=metric_ids,
                    channel_ids=self.curr_channels,
                )
                results = Insights(
                    creds=self._creds, session=self.session
                ).make_api_call(insights_request_id)
            if results is None:
                raise ConnectionError(
                    f"Falcon API failed to return channel insights. "
                )
            data = results["data"]["insights"]
            dataset.extend(self._normalize_data(data, network, channel_ids))
            self.start = self.start + channel_steps
        return dataset


class PublishedPosts(FalconAPICall):
    """This class gets published posts data"""

    def get_dataset(
        self, start_date: str, end_date: str, network: str, channel_ids: list
    ) -> dict:
        """Fucntion handles published posts query"""
        dataset = []
        if channel_ids is not None:
            print(
                f"Attempting to gather metrics from {len(channel_ids)} channel ids. ")
            statuses = self.config.get("statuses", "published")
            limit = self.config.get("limit", 2000)
            try:
                for channel_id in channel_ids:
                    self.curr_channels = [channel_id]
                    results = PublishedPostsByChannelId(
                        creds=self._creds, session=self.session
                    ).make_api_call(
                        start_date=start_date,
                        end_date=end_date,
                        network=network,
                        channel_ids=[channel_id],
                        statuses=statuses,
                        limit=limit,
                        index=self.start,
                    )
                    if results:
                        print(len(results))
                        dataset.extend(results)
                    self.start += 1
            except FalconQuotaException as e:
                raise e
        return dataset
