import dataclasses
import logging
import gzip
import json
from typing import Optional

logger = logging.getLogger(__name__)


class StrDefaultEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return str(o)


class IngestIOHelper:
    def __init__(self, s3_bucket: str, s3_path: str, local_file_path: str):
        self.s3_bucket = s3_bucket
        self.s3_path = (s3_path,)
        # EVERYTHING in this file path will (potentially) be uploaded to S3!
        # DO NOT put any creds file in this path!!!!
        self.local_file_path = local_file_path

    def _get_file_name(self, object_name: str, batch_number: Optional[int] = 0):
        return f'{object_name}{batch_number if batch_number else ""}.json.gz'

    def write_json_data_to_local(
        self,
        object_name: str,
        json_data: dict | list[dict],
        batch_number: Optional[int] = 0,
    ):
        try:
            file_name = self._get_file_name(
                object_name=object_name, batch_number=batch_number
            )
            full_file_path = f"{self.local_file_path}/{file_name}"
            logger.info(f"Attempting to save {object_name} data to {full_file_path}")
            with gzip.open(full_file_path, "w") as f:
                f.write(
                    json.dumps(json_data, indent=2, cls=StrDefaultEncoder).encode(
                        "utf-8"
                    )
                )
                logger.debug(
                    f"File: {full_file_path}, Size: {round(f.tell() / 1000000, 1)}MB"
                )
        except Exception as e:
            logger.error(
                f"Exception encountered when attempting to write data to local file! Error: {e}"
            )

    def upload_files_to_s3(self):
        # TODO: Write multi threaded uploader to upload this local_file_path
        raise NotImplementedError("Function not implemented!")
