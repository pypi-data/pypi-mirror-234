from pyfiglet import Figlet
from PyInquirer import prompt
import os


class Dashboard:
    def __init__(self) -> None:
        self.options = {}

    def get_options(self) -> dict:
        return self.options

    def show(self) -> None:
        self.options["project_name"] = self._get_project_name()
        self.options["author"] = self._get_author()
        self.options["task"] = self._get_task()
        self.options["logger"] = self._get_logger()
        self.options["project_path"] = self._get_project_path()

    def _get_project_name(self) -> str:
        project_name_prompt = {
            "type": "input",
            "name": "project_name",
            "message": "Please input project name",
        }
        return prompt(project_name_prompt)["project_name"]

    def _get_author(self) -> str:
        project_name_prompt = {
            "type": "input",
            "name": "author",
            "message": "Please input author",
        }
        return prompt(project_name_prompt)["author"]

    def _get_task(self) -> str:
        task_prompt = {
            "type": "list",
            "name": "task",
            "message": "Choose your task?",
            "choices": [
                "Token Classification",
                "Translation",
                "Summarization",
                "Question Answering",
            ],
        }
        return prompt(task_prompt)["task"]

    def _get_logger(self) -> str:
        logger_prompt = {
            "type": "list",
            "name": "logger",
            "message": "Choose your Logging tools?",
            "choices": [
                "Wandb",
                "MLflow",
                "None",
            ],
        }
        return prompt(logger_prompt)["logger"]
    

    def _get_project_path(self) -> str:
        #TODO: Ask to user by prompt
        return os.getcwd()

