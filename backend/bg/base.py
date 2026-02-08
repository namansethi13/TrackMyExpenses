from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

class TaskPublisherBase(ABC):

    @abstractmethod
    def publish(
        self,
        task_name: str,
        args: Optional[list] = None,
        kwargs: Optional[Dict[str, Any]] = None,
        countdown: Optional[int] = None,
    ) -> None:
        ...
