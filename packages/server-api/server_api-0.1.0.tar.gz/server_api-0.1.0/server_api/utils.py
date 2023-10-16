from datetime import datetime
from typing import Optional, Union
from enum import Enum


class StatusEnum(str, Enum):
    in_progress = "in_progress"
    failure = "failure"
    success = "success"


def create_status(
        start_dt: Optional[datetime], finish_dt: Optional[datetime], success: Optional[bool]
) -> Union[StatusEnum, None]:
    if (start_dt and finish_dt and start_dt > finish_dt) \
            or (start_dt and finish_dt is None):
        return StatusEnum.in_progress

    if success is False:
        return StatusEnum.failure

    if success is True:
        return StatusEnum.success


def create_msg(status: str, task_name: str):
    if status == "failure":
        return f"{task_name} failed."
