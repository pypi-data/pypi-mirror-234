from __future__ import annotations

import json
import logging
import os
from stdflow.config import RUN_ENV_KEY, PATHS_ENV_KEY, prefix

try:
    from typing import Any, Literal, Optional, Tuple, Union
except ImportError:
    from typing_extensions import Any, Literal, Tuple, Union

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)


class FlowEnv:  # has to be singleton
    config = "rel"

    def __init__(self):
        self.cwd = None
        FlowEnv.is_valid()

    @staticmethod
    def running() -> bool:
        return os.environ.get(RUN_ENV_KEY, None) is not None

    @property
    def id(self):
        return len(self.paths) - 1

    @property
    def path(self) -> str | None:
        paths = self.paths
        if len(paths) == 0:
            return None

        return paths[self.id]  # Redundant but allows to check if env variables are always correct

    @property
    def dir(self) -> str:
        """
        Current working directory relative to the execution directory.
        this can be absolute if the step at depth 1 is specified with absolute path or if config != rel
        :return:
        """
        path = self.path
        if path is not None:
            return os.path.dirname(path)
        return "./" if FlowEnv.config == "rel" else os.getcwd()

    @property
    def paths(self) -> list[str]:
        if not os.environ.get(PATHS_ENV_KEY):
            return []
        return os.environ.get(PATHS_ENV_KEY).split(":")

    @staticmethod
    def is_valid() -> bool:
        assert FlowEnv.running() == (PATHS_ENV_KEY in os.environ), "invalid environment"
        return True

    @staticmethod
    def remove_last_path() -> None:
        os.environ[PATHS_ENV_KEY] = ":".join(os.environ[PATHS_ENV_KEY].split(":")[:-1])
        if len(os.environ[PATHS_ENV_KEY]) == 0:
            del os.environ[PATHS_ENV_KEY]

    @staticmethod
    def add_path(path: str) -> None:
        if FlowEnv.running():
            os.environ[PATHS_ENV_KEY] = f"{os.environ[PATHS_ENV_KEY]}:{path}"
        else:
            os.environ[PATHS_ENV_KEY] = path

    def set_vars(self, variables):
        logger.debug(f"setting variables {variables}")
        os.environ[f"{prefix}{self.id}__vars"] = json.dumps(variables)

    def var(self, key) -> str | None:
        json_str = os.environ.get(f"{prefix}{self.id}__vars", None)
        if json_str is None:
            return None
        return json.loads(json_str).get(key, None)

    def remove_vars(self):
        del os.environ[f"{prefix}{self.id}__vars"]

    # def get_adjusted_worker_path(self, worker_path: str) -> str:
    #     if not os.path.isabs(worker_path):
    #         worker_path = os.path.join(self.dir, worker_path)
    #         worker_path = os.path.normpath(worker_path)
    #     return worker_path

    def start_run(self, workspace, path, variables: dict[str, str] | None = None) -> None:
        self.add_path(path)
        self.set_vars(variables or {})  # Must be after add_path
        os.environ[RUN_ENV_KEY] = "True"
        # save current working directory
        self.cwd = os.getcwd()
        # change working directory
        # os.chdir(workspace)  # Now this operation is done by giving an argument when running the notebook

    def end_run(self) -> None:
        self.remove_vars()  # Must be before remove_last_path
        self.remove_last_path()
        if self.id == -1:
            del os.environ[RUN_ENV_KEY]
        # change working directory back
        # os.chdir(self.cwd)
