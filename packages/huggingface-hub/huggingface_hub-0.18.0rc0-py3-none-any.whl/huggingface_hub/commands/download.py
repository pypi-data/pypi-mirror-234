# coding=utf-8
# Copyright 2023-present, the HuggingFace Inc. team.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Contains command to download files from the Hub with the CLI.

Usage:
    huggingface-cli download --help

    # Download file
    huggingface-cli download gpt2 config.json

    # Download entire repo
    huggingface-cli download fffiloni/zeroscope --repo-type=space --revision=refs/pr/78

    # Download repo with filters
    huggingface-cli download gpt2 --include="*.safetensors"

    # Download with token
    huggingface-cli download Wauplin/private-model --token=hf_***

    # Download quietly (no progress bar, no warnings, only the returned path)
    huggingface-cli download gpt2 config.json --quiet

    # Download to local dir
    huggingface-cli download gpt2 --local-dir=./models/gpt2
"""
import warnings
from argparse import Namespace, _SubParsersAction
from typing import List, Literal, Optional, Union

from huggingface_hub import logging
from huggingface_hub._snapshot_download import snapshot_download
from huggingface_hub.commands import BaseHuggingfaceCLICommand
from huggingface_hub.constants import HF_HUB_ENABLE_HF_TRANSFER
from huggingface_hub.file_download import hf_hub_download
from huggingface_hub.utils import disable_progress_bars, enable_progress_bars


logger = logging.get_logger(__name__)


class DownloadCommand(BaseHuggingfaceCLICommand):
    @staticmethod
    def register_subcommand(parser: _SubParsersAction):
        download_parser = parser.add_parser("download", help="Download files from the Hub")
        download_parser.add_argument(
            "repo_id", type=str, help="ID of the repo to download from (e.g. `username/repo-name`)."
        )
        download_parser.add_argument(
            "filenames", type=str, nargs="*", help="Files to download (e.g. `config.json`, `data/metadata.jsonl`)."
        )
        download_parser.add_argument(
            "--repo-type",
            choices=["model", "dataset", "space"],
            default="model",
            help="Type of repo to download from (e.g. `dataset`).",
        )
        download_parser.add_argument(
            "--revision",
            type=str,
            help="An optional Git revision id which can be a branch name, a tag, or a commit hash.",
        )
        download_parser.add_argument(
            "--include", nargs="*", type=str, help="Glob patterns to match files to download."
        )
        download_parser.add_argument(
            "--exclude", nargs="*", type=str, help="Glob patterns to exclude from files to download."
        )
        download_parser.add_argument(
            "--cache-dir", type=str, help="Path to the directory where to save the downloaded files."
        )
        download_parser.add_argument(
            "--local-dir",
            type=str,
            help=(
                "If set, the downloaded file will be placed under this directory either as a symlink (default) or a"
                " regular file. Check out"
                " https://huggingface.co/docs/huggingface_hub/guides/download#download-files-to-local-folder for more"
                " details."
            ),
        )
        download_parser.add_argument(
            "--local-dir-use-symlinks",
            choices=["auto", "True", "False"],
            default="auto",
            help=(
                "To be used with `local_dir`. If set to 'auto', the cache directory will be used and the file will be"
                " either duplicated or symlinked to the local directory depending on its size. It set to `True`, a"
                " symlink will be created, no matter the file size. If set to `False`, the file will either be"
                " duplicated from cache (if already exists) or downloaded from the Hub and not cached."
            ),
        )
        download_parser.add_argument(
            "--force-download",
            action="store_true",
            help="If True, the files will be downloaded even if they are already cached.",
        )
        download_parser.add_argument(
            "--resume-download", action="store_true", help="If True, resume a previously interrupted download."
        )
        download_parser.add_argument(
            "--token", type=str, help="A User Access Token generated from https://huggingface.co/settings/tokens"
        )
        download_parser.add_argument(
            "--quiet",
            action="store_true",
            help="If True, progress bars are disabled and only the path to the download files is printed.",
        )
        download_parser.set_defaults(func=DownloadCommand)

    def __init__(self, args: Namespace) -> None:
        self.token = args.token
        self.repo_id: str = args.repo_id
        self.filenames: List[str] = args.filenames
        self.repo_type: str = args.repo_type
        self.revision: Optional[str] = args.revision
        self.include: Optional[List[str]] = args.include
        self.exclude: Optional[List[str]] = args.exclude
        self.cache_dir: Optional[str] = args.cache_dir
        self.local_dir: Optional[str] = args.local_dir
        self.force_download: bool = args.force_download
        self.resume_download: bool = args.resume_download
        self.quiet: bool = args.quiet

        # Raise if local_dir_use_symlinks is invalid
        self.local_dir_use_symlinks: Union[Literal["auto"], bool]
        use_symlinks_lowercase = args.local_dir_use_symlinks.lower()
        if use_symlinks_lowercase == "true":
            self.local_dir_use_symlinks = True
        elif use_symlinks_lowercase == "false":
            self.local_dir_use_symlinks = False
        elif use_symlinks_lowercase == "auto":
            self.local_dir_use_symlinks = "auto"
        else:
            raise ValueError(
                f"'{args.local_dir_use_symlinks}' is not a valid value for `local_dir_use_symlinks`. It must be either"
                " 'auto', 'True' or 'False'."
            )

    def run(self) -> None:
        if self.quiet:
            disable_progress_bars()
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                print(self._download())  # Print path to downloaded files
            enable_progress_bars()
        else:
            logging.set_verbosity_info()
            print(self._download())  # Print path to downloaded files
            logging.set_verbosity_warning()

    def _download(self) -> str:
        # Warn user if patterns are ignored
        if len(self.filenames) > 0:
            if self.include is not None and len(self.include) > 0:
                warnings.warn("Ignoring `--include` since filenames have being explicitly set.")
            if self.exclude is not None and len(self.exclude) > 0:
                warnings.warn("Ignoring `--exclude` since filenames have being explicitly set.")

        if not HF_HUB_ENABLE_HF_TRANSFER:
            logger.info(
                "Consider using `hf_transfer` for faster downloads. This solution comes with some limitations. See"
                " https://huggingface.co/docs/huggingface_hub/hf_transfer for more details."
            )

        # Single file to download: use `hf_hub_download`
        if len(self.filenames) == 1:
            return hf_hub_download(
                repo_id=self.repo_id,
                repo_type=self.repo_type,
                revision=self.revision,
                filename=self.filenames[0],
                cache_dir=self.cache_dir,
                resume_download=self.resume_download,
                force_download=self.force_download,
                token=self.token,
                local_dir=self.local_dir,
                local_dir_use_symlinks=self.local_dir_use_symlinks,
                library_name="huggingface-cli",
            )

        # Otherwise: use `snapshot_download` to ensure all files comes from same revision
        elif len(self.filenames) == 0:
            allow_patterns = self.include
            ignore_patterns = self.exclude
        else:
            allow_patterns = self.filenames
            ignore_patterns = None

        return snapshot_download(
            repo_id=self.repo_id,
            repo_type=self.repo_type,
            revision=self.revision,
            allow_patterns=allow_patterns,
            ignore_patterns=ignore_patterns,
            resume_download=self.resume_download,
            force_download=self.force_download,
            cache_dir=self.cache_dir,
            token=self.token,
            local_dir=self.local_dir,
            local_dir_use_symlinks=self.local_dir_use_symlinks,
            library_name="huggingface-cli",
        )
