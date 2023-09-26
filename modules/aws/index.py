import abc
import os
import time
import json
import typing
import urllib3
import base64
import gzip
import logging
import dataclasses
from datetime import datetime
import dateutil.parser

logging.basicConfig(format="%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@dataclasses.dataclass
class GuancePoint:
    measurement: str
    tags: dict[str, str]
    fields: dict[str, typing.Any]
    time: int


@dataclasses.dataclass
class GuanceData:
    points: list[GuancePoint]


def parse(raw: dict, measurement=None) -> GuanceData:
    """ Parse AWS log data

    :param raw: AWS log data passed by AWS Lambda
    :param measurement: measurement name
    """
    if 'awslogs' in raw:
        return _parse_logs(raw, measurement=measurement or "lambda_logs")
    else:
        return _parse_event(raw, measurement=measurement or "lambda_events")


def _parse_logs(raw: dict, measurement: str) -> GuanceData:
    """ Parse AWS log data

    >>> aws_event_raw = { "awslogs": { "data": "H4sIAAAAAAAAAHWPwQqCQBCGX0Xm7EFtK+smZBEUgXoLCdMhFtKV3akI8d0bLYmibvPPN3wz00CJxmQnTO41whwWQRIctmEcB6sQbFC3CjW3XW8kxpOpP+OC22d1Wml1qZkQGtoMsScxaczKN3plG8zlaHIta5KqWsozoTYw3/djzwhpLwivWFGHGpAFe7DL68JlBUk+l7KSN7tCOEJ4M3/qOI49vMHj+zCKdlFqLaU2ZHV2a4Ct/an0/ivdX8oYc1UVX860fQDQiMdxRQEAAA==" } }
    >>> _parse_logs(aws_event_raw, "lambda_logs")
    GuanceData(points=[GuancePoint(measurement='lambda_logs', tags={}, fields={'id': 'eventId1', 'message': '[ERROR] First test message'}, time=1440442987000), GuancePoint(measurement='lambda_logs', tags={}, fields={'id': 'eventId2', 'message': '[ERROR] Second test message'}, time=1440442987001)])
    """
    aws_event_data = raw["awslogs"]["data"]
    aws_event_data = base64.b64decode(aws_event_data.encode("utf-8"))
    aws_event_data = gzip.decompress(aws_event_data).decode("utf-8")
    aws_event = json.loads(aws_event_data)
    raw_events = aws_event.get("logEvents")

    return GuanceData([
        GuancePoint(
            measurement=measurement,
            time=e.pop('timestamp', round(time.time_ns() / 1000000)),
            tags={},
            fields={
                "id": e.pop('id', ''),
                "message": e.pop('message', ''),
            }
        )
        for e in raw_events
    ])


def _parse_event(raw: dict, measurement: str) -> GuanceData:
    """ Parse AWS event data

    >>> testdata = {
    ...   "id": "cdc73f9d-aea9-11e3-9d5a-835b769c0d9c",
    ...   "detail-type": "Scheduled Event",
    ...   "source": "aws.events",
    ...   "account": "123456789012",
    ...   "time": "1970-01-01T00:00:01Z",
    ...   "region": "us-east-1",
    ...   "resources": [
    ...       "arn:aws:events:us-east-1:123456789012:rule/ExampleRule"
    ...   ],
    ...   "detail": {}
    ... }
    >>> _parse_event(testdata, "lambda_events")
    GuanceData(points=[GuancePoint(measurement='lambda_events', tags={'detail-type': 'Scheduled-Event', 'source': 'aws.events', 'account': '123456789012', 'region': 'us-east-1'}, fields={'id': 'cdc73f9d-aea9-11e3-9d5a-835b769c0d9c', 'message': '{"resources": ["arn:aws:events:us-east-1:123456789012:rule/ExampleRule"], "detail": {}}'}, time=1000)])
    """
    tag_names = ["detail-type", "source", "account", "region"]
    rfc3339 = raw.pop('time', '')
    if rfc3339:
        timestamp = round(dateutil.parser.isoparse(rfc3339).timestamp() * 1000)
    else:
        timestamp = round(time.time_ns() / 1000000)
    return GuanceData([
        GuancePoint(
            measurement=measurement,
            time=timestamp,
            tags={
                tag_name: raw.pop(tag_name, '').replace(' ', '-')
                for tag_name in tag_names
                if tag_name in raw
            },
            fields={
                "id": raw.pop('id', ''),
                "message": json.dumps(raw),
            }
        )
    ])


class Client(abc.ABC):
    def __init__(self, endpoint: str) -> None:
        self.endpoint: str = endpoint

    @abc.abstractmethod
    def send(self, data: GuanceData):
        """Send data to Guance"""
        pass

    @staticmethod
    def http_request(url: str, body: typing.Any, is_json=False):
        http = urllib3.PoolManager()
        params = {
            "method": "POST",
            "url": url,
            "body": body
        }
        if is_json:
            params["body"] = json.dumps(body)
            params["headers"] = {"Content-Type": "application/json"}
        response = http.request(**params)
        logger.debug(f"push response status: ${response.status}")


class DataKitClient(Client):
    def __init__(self, endpoint: str) -> None:
        super().__init__(endpoint=endpoint)

    def send(self, data: GuanceData):
        """Send data to Guance"""
        return self.http_request(f"{self.endpoint}/v1/write/logging", data, is_json=True)


class TestClient(Client):
    def __init__(self, endpoint: str, token: str) -> None:
        super().__init__(endpoint=endpoint)
        self.token = token

    def send(self, data: GuanceData):
        """Send data to Guance"""
        payload = "\n".join([self.build_line_proto(d) for d in data.points])
        logger.debug(f"push payload: ${payload}")
        return self.http_request(f"{self.endpoint}/v1/write/logging?token={self.token}&epoch=ms", payload)

    @staticmethod
    def build_line_proto(data: GuancePoint):
        raw = f'{data.measurement}'
        if data.tags:
            raw += ',' + ",".join([f'{k}={v}' for k, v in data.tags.items()])
        raw += ' ' + ",".join([
            '{}="{}"'.format(k, v.replace('"', '\\"')) if isinstance(v, str) else f'{k}={v}'
            for k, v in data.fields.items()
        ])
        raw += f' {data.time}'
        return raw


# Load environment variables
GUANCE_ENDPOINT = os.getenv('GUANCE_ENDPOINT')
GUANCE_WORKSPACE_TOKEN = os.getenv('GUANCE_WORKSPACE_TOKEN')


def lambda_handler(event, context):
    if not GUANCE_WORKSPACE_TOKEN:
        client = DataKitClient(endpoint=GUANCE_ENDPOINT)
    else:
        client = TestClient(endpoint=GUANCE_ENDPOINT, token=GUANCE_WORKSPACE_TOKEN)
    client.send(parse(event))
    return


def integration_test():
    aws_logs = {
        "awslogs": {
            "data": "H4sIAAAAAAAAAHWPwQqCQBCGX0Xm7EFtK+smZBEUgXoLCdMhFtKV3akI8d0bLYmibvPPN3wz00CJxmQnTO41whwWQRIctmEcB6sQbFC3CjW3XW8kxpOpP+OC22d1Wml1qZkQGtoMsScxaczKN3plG8zlaHIta5KqWsozoTYw3/djzwhpLwivWFGHGpAFe7DL68JlBUk+l7KSN7tCOEJ4M3/qOI49vMHj+zCKdlFqLaU2ZHV2a4Ct/an0/ivdX8oYc1UVX860fQDQiMdxRQEAAA=="
        }
    }
    aws_events = {
        "id": "cdc73f9d-aea9-11e3-9d5a-835b769c0d9c",
        "detail-type": "Scheduled Event",
        "source": "aws.events",
        "account": "123456789012",
        "time": datetime.now().isoformat(),
        "region": "us-east-1",
        "resources": [
            "arn:aws:events:us-east-1:123456789012:rule/ExampleRule"
        ],
        "detail": {}
    }
    lambda_handler(aws_logs, None)
    lambda_handler(aws_events, None)
