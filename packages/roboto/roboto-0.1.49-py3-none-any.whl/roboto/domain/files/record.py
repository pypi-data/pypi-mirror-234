import datetime
import urllib.parse

import pydantic


class FileRecord(pydantic.BaseModel):
    association_id: str  # e.g. dataset_id, collection_id, etc.; GSI PK of "association_id" index.
    file_id: str  # Table PK
    modified: datetime.datetime  # Persisted as ISO 8601 string in UTC
    relative_path: str  # path relative to some common prefix. Used as local path when downloaded.
    size: int  # bytes
    org_id: str
    uri: str  # GSI PK of "uri" index; GSI SK of "association_id" index
    upload_id: str = "NO_ID"  # Defaulted for backwards compatability

    @property
    def bucket(self) -> str:
        parsed_uri = urllib.parse.urlparse(self.uri)
        return parsed_uri.netloc

    @property
    def key(self) -> str:
        parsed_uri = urllib.parse.urlparse(self.uri)
        return parsed_uri.path.lstrip("/")
