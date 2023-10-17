from __future__ import annotations

import logging
import os
import warnings

from stdflow.stdflow_path import Path
from stdflow.stdflow_utils.listing import (
    list_csv_files,
    list_excel_files,
    list_files_glob,
    list_non_metadata_files,
)

try:
    from typing import Literal, Optional
except ImportError:
    from typing_extensions import Literal, Optional

from stdflow.config import STEP_PREFIX, VERSION_PREFIX
from stdflow.stdflow_utils import detect_folders, fstep, fv, path_to_str, str_to_path

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class DataPath(Path):
    def __init__(
        self,
        root: str | None = "./data",
        attrs: list | None | str = None,
        step_name: str | None = None,
        version: str | Literal[":last", ":first"] = ":last",
        file_name: str | Literal[":auto"] = None,
        glob: bool = False,
    ):
        """
        At this stage all information are present except the version which is to be detected if not specified
        :param root: first part of the full_path
        :param attrs: seconds parts of the full_path (optional)
        :param step_name: third part of the full_path (optional)
        :param version: last part of the full_path. one of [":last", ":first", "<version_name>", None]
        :param file_name: file name (optional)
        """
        super().__init__(root, file_name)

        # if step is str and contains step_, remove it
        if isinstance(step_name, str) and step_name.startswith(STEP_PREFIX):
            step_name = step_name[len(STEP_PREFIX) :]
        # if version is str and contains v_, remove it
        if isinstance(version, str) and version.startswith(VERSION_PREFIX):
            version = version[len(VERSION_PREFIX) :]

        self.attrs: str = "/".join(attrs) if isinstance(attrs, list) else attrs
        self.step_name = step_name

        self.version = None
        if version in [":last", ":first"]:
            if not os.path.isdir(self.dir_path):
                logger.error(f"Path {self.dir_path} does not exist")
            self.version = self.detect_version(self.dir_path, version)
        elif version is not None and version.startswith(VERSION_PREFIX):
            self.version = version[len(VERSION_PREFIX):]
        elif version is not None:
            self.version = version

        if file_name == ":auto" or glob is True:
            self.file_name = self.detect_file_name(file_name, glob=glob)

    def detect_file_name(self, file_name, glob=False):  # FIXME detect files based on extension
        if not os.path.isdir(self.dir_path):
            logger.error(f"Path {self.dir_path} does not exist")
        if glob is True and file_name is not None and file_name is not ":auto":
            files = list_files_glob(self.dir_path, file_name)
        else:
            files = list_csv_files(self.dir_path)
            if not files:
                files = list_excel_files(self.dir_path)
                if not files:
                    files = list_non_metadata_files(self.dir_path)
        if len(files) == 1:
            logger.debug(f"Using file {files[0]}")
            return files[0]
        elif len(files):
            logger.warning(
                f"Cannot use auto file detection:"
                f"Multiple files found in {self.dir_path}: {files}"
            )
        else:
            logger.warning(f"Cannot use auto file detection:" f"No files found in {self.dir_path}")
        return None

    def detect_version(self, path, version_type):
        if version_type not in [":last", ":first"]:
            logger.warning(f"Unknown version type: {version_type}")
        # Check for versioned directories
        versions = detect_folders(path, VERSION_PREFIX)

        logger.debug(f"ordered versions: {versions}")
        if not versions:
            warnings.warn(
                f"No versioned directories found in {path}"
                f"If you don't intend to use version, set version=None",
                category=UserWarning,
            )

        if version_type == ":last":
            return versions[-1] if versions else None
        elif version_type == ":first":
            return versions[0] if versions else None

        return None

    def __str__(self):
        return path_to_str(self.attrs, self.step_name, self.version, self.file_name)

    def __repr__(self):
        return self.__str__()

    @classmethod
    def from_str(cls, path_str):
        return cls(**str_to_path(path_str))

    @property
    def full_path(self):
        return Path._create_path(
            self.root,
            self.attrs,
            fstep(self.step_name) if self.step_name else "",
            fv(self.version) if self.version else "",
            self.file_name,
        )

    @property
    def full_path_from_root(self):
        return Path._create_path(
            None,
            self.attrs,
            fstep(self.step_name) if self.step_name else "",
            fv(self.version) if self.version else "",
            self.file_name,
        )

    @property
    def dir_path(self) -> str:
        return Path._create_path(
            self.root,
            self.attrs,
            fstep(self.step_name) if self.step_name else "",
            fv(self.version) if self.version else "",
            None,
        )

    @property
    def step_dir(self):
        return Path._create_path(
            self.root,
            self.attrs,
            fstep(self.step_name) if self.step_name else None,
        )

    @property
    def dict_step(self):
        return dict(
            path=self.attrs,
            step_name=self.step_name,
            version=self.version,
        )

    @classmethod
    def from_dict(cls, step_dict, file_name, file_type):
        return cls(
            root=None,
            attrs=step_dict["path"],
            step_name=step_dict["step_name"],
            version=step_dict["version"],
            file_name=f"{file_name}.{file_type}",
        )

    @property
    def metadata_path(self):
        return os.path.join(self.dir_path, "metadata.json")

    @classmethod
    def from_input_params(cls, root, attrs, step, version, file_name, glob=False):
        # if step is True:
        #     # extract step from path
        #     step = retrieve_from_path(path, STEP_PREFIX)
        #     path = remove_dir(path, fstep(step))
        # if version is True:
        #     # extract version from path
        #     version = retrieve_from_path(path, VERSION_PREFIX)
        #     path = remove_dir(path, fv(version))
        # if file_name is True:
        #     # extract file_name from path
        #     file_name = os.path.basename(path)
        #     path = os.path.dirname(path)

        return cls(
            root=root,
            attrs=attrs,
            step_name=step,
            version=version,
            file_name=file_name,
            glob=glob,
        )

    def __eq__(self, other):
        return (
            self.attrs == other.attrs
            and self.step_name == other.step_name
            and self.version == other.version
            and self.file_name == other.file_name
        )


if __name__ == "__main__":
    path = DataPath("./data", attrs="fr", step_name="raw", version=":last")
    assert path.full_path == "./data/fr/step_raw/v_2/", f"src.full_path: {path.full_path}"
