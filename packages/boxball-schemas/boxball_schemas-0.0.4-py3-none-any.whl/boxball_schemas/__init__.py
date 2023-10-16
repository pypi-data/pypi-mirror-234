from typing import List
from sqlalchemy import MetaData
from src.boxball_schemas.retrosheet import metadata as retrosheet_metadata
from src.boxball_schemas.baseballdatabank import metadata as baseballdatabank_metadata

all_metadata: List[MetaData] = [baseballdatabank_metadata, retrosheet_metadata]
