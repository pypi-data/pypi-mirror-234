from typing import TypedDict, Optional, Any, List, Dict
from pathlib import Path
from logging import Logger

Setup = TypedDict('Setup',
                  non_public=bool,
                  port=int,
                  json_files=List[Path],
                  workdir=Optional[Path],
                  debug=bool,
                  quiet=bool,
                  channel=str,
                  interface=str,
                  bitrate=Optional[str],
                  logger=Logger)

ConfigJson = TypedDict('ConfigJson',
                       mappings=List[Any],
                       items=List[Any],
                       view=List[Any])

ProjectInfo = TypedDict('ProjectInfo',
                        id=int,
                        created=str,
                        updated=str,
                        name=str)

Project = TypedDict('Project',
                    info=ProjectInfo,
                    versions=int)

Config = Dict[str, Any]

ConfigWithMeta = TypedDict('ConfigWithMeta',
                           id=int,
                           proejct=str,
                           version=int,
                           config=Config,
                           created=str)

FirmwareInfo = TypedDict('FirmwareInfo',
                         id=int,
                         name=str,
                         created=str)

BoxInfo = TypedDict('BoxInfo',
                    box_id=int,
                    running=str,
                    updating=bool,
                    failed=bool,
                    using_secondary=bool,
                    version_id=str,
                    revision=int,
                    first_missing_chunk=int)
