# -*- coding: utf-8 -*-
from pyfiglet import Figlet
from PyInquirer import prompt

options = {}


def get_project_name():
    project_name_prompt = {
        "type": "input",
        "name": "project_name",
        "message": "Please input project name",
    }
    options["project_name"] = prompt(project_name_prompt)["project_name"]


def get_author():
    project_name_prompt = {
        "type": "input",
        "name": "author",
        "message": "Please input author",
    }
    options["author"] = prompt(project_name_prompt)["author"]


def get_task():
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
    options["task"] = prompt(task_prompt)["task"]


f = Figlet(font="slant")
print(f.renderText("Earth Coding Lab"))


def get_mlops():
    mlops_prompt = {
        "type": "list",
        "name": "mlops",
        "message": "Choose your MLOps tools?",
        "choices": [
            "Wandb",
            "MLflow",
            "None",
        ],
    }
    options["mlops"] = prompt(mlops_prompt)["mlops"]


def main_cli():
    get_project_name()
    get_author()
    get_task()
    get_mlops()
    return options
