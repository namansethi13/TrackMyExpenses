#task publisher factory
from bg.base import TaskPublisherBase
from bg.celery_pub import CeleryTaskPublisher
import os



_instances: dict[str, TaskPublisherBase] = {} # singleton instances for each mode

_FACTORIES = { # creation policies for different modes
    "celery": CeleryTaskPublisher,
}

def get_task_publisher() -> TaskPublisherBase:
    """
    Factory function to get the appropriate TaskPublisher instance based on the BG_TASK_MODE environment variable.
    Defaults to "celery" if not set.
    """
    mode = os.getenv("BG_TASK_MODE", "celery")

    if mode not in _instances:
        try:
            _instances[mode] = _FACTORIES[mode]()
        except KeyError:
            raise ValueError(f"Unknown mode: {mode}")

    return _instances[mode]

def reset_publishers_for_tests():
    _instances.clear()
