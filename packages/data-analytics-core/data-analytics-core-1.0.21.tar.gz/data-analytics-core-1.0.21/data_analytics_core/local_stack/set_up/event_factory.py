# TODO: divide event class  into separated classes per event type
# TODO: modularize events depending on which service/microservice is launching the event
class EventS3Put:

    def __init__(self, bucket: str, key: str):
        self.S3_EVENT_PUT["Records"][0]["s3"]["bucket"]["name"] = bucket
        self.S3_EVENT_PUT["Records"][0]["s3"]["object"]["key"] = key
        self.S3_EVENTBRIDGE_PUT["detail"]["bucket"]["name"] = bucket
        self.S3_EVENTBRIDGE_PUT["detail"]["object"]["key"] = key
        self.S3_EVENTBRIDGE_PUT["resources"] = [f"arn: aws:s3:::{bucket}"]

    def get_fixture_event(self) -> dict:
        return self.S3_EVENT_PUT

    def get_fixture_eventbridge_event(self) -> dict:
        return self.S3_EVENTBRIDGE_PUT

    S3_EVENT_PUT = {
        "Records": [
            {
                "eventVersion": "2.0",
                "eventSource": "aws:s3",
                "awsRegion": "eu-central-1",
                "eventTime": "1970-01-01T00:00:00.000Z",
                "eventName": "ObjectCreated:Put",
                "userIdentity": {"principalId": "EXAMPLE"},
                "requestParameters": {"sourceIPAddress": "127.0.0.1"},
                "responseElements": {
                    "x-amz-request-id": "EXAMPLE123456789",
                    "x-amz-id-2": "EXAMPLE123/5678abcdefghijklambdaisawesome/mnopqrstuvwxyzABCDEFGH",
                },
                "s3": {
                    "s3SchemaVersion": "1.0",
                    "configurationId": "testConfigRule",
                    "bucket": {
                        "name": "s3-name",
                        "ownerIdentity": {"principalId": "PRINCIPALID"},
                        "arn": "arn:aws:s3:::s3-data-intake",
                    },
                    "object": {
                        "key": "route/of/my_fantastic_object.json",
                        "size": 1024,
                        "eTag": "0123456789abcdef0123456789abcdef",
                        "sequencer": "0A1B2C3D4E5F678901",
                    },
                },
            }
        ]
    }

    S3_EVENTBRIDGE_PUT = {
        "source": "aws.s3",
        "region": "eu-central-1",
        "resources": [
            "arn:aws:s3:::s3-raw"
        ],
        "detail": {
            "bucket": {
                "name": "s3-raw"
            },
            "object": {
                "key": "sum_provider/and_its_cool.zip"
            }
        }
    }
