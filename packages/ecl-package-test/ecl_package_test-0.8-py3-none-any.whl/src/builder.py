import shutil
import re
import isort
from abc import *
import sys
import os

REQUIRE_OPTION_FIELDS = ["project_name", "task", "logger"]
LOGGER_LABEL = "LOGGER"


class TemplateBuilder:
    def __init__(self, options: dict) -> None:
        # TODO: Need pydantic to validation options
        self.options = options
        self.project_name = self.options["project_name"]
        self.project_path = self.options["project_path"]
        self.copy_project_source_path = os.path.join(self.project_path, "templates/classification")
        self.copy_project_destination_path = os.path.join(self.project_path, self.project_name)
        #TODO: Custom copy_project_path by user


    @abstractmethod
    def build_template(self):
        pass

    def _copy_dir(self, src, dist) -> None:
        shutil.copytree(src, dist)

    def _replace_code(self, path, prefix, replacement) -> None:
        with open(path, "r") as f:
            file_str = f.read()
        replace_str = re.sub(f"##{prefix} BLOCK[\s\S]*##END", replacement, file_str)
        with open(path, "w") as f:
            f.write(replace_str)

    def _add_import(self, path: str, import_line: str) -> None:
        with open(path, "r+") as f:
            content = f.read()
            f.seek(0, 0)
            f.write(import_line.rstrip("\r\n") + "\n" + content)

    def _isort_file(self, path: str) -> None:
        # TODO: Should isort be called every time in each builders?
        isort.file(path)

    def _build_logger(self, logger_block_path:str) -> None:
        replacement = "logger = None"
        logger_option = self.options["logger"]
        if logger_option == "Wandb":
            replacement = "logger = Wandb()"
        elif logger_option == "MLFlow":
            replacement = "logger = Mlflow()"

        self._replace_code(logger_block_path, LOGGER_LABEL, replacement)

        self._add_import(logger_block_path, "import torch")
        

    def _build_dataset(self) -> None:
        pass

class TextClassificationTemplateBuilder(TemplateBuilder):
    def __init__(self, options: dict) -> None:
        super().__init__(options)

    def build_template(self):
        self._copy_dir(self.copy_project_source_path, self.copy_project_destination_path)
        self._build_logger(os.path.join(self.copy_project_destination_path, "main.py"))
        self._isort_file(os.path.join(self.copy_project_destination_path, "main.py"))