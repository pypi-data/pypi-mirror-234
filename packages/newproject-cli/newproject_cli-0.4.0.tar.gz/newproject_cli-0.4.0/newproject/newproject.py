#!/usr/bin/env python3

import errno
import json
import logging
import os
import site
import subprocess
import sys
from pathlib import Path
from shutil import which
from typing import Final

import jsonschema
import typer
import yaml
from rich.console import Console
from typing_extensions import Annotated

# rich config
console = Console()

# Logging config
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s %(message)s')
logger = logging.getLogger(__name__)

# Outputs
DONE: Final[str] = "✓ Done.\n"
PROJECT_STRUCTURE_GEN: Final[str] = "[dodger_blue1]Creating the project structure...[/dodger_blue1]"
HAPPY_CODING: Final[str] = "[gold1]⫸ Happy Coding![/gold1]"
COULD_NOT_CREATE_PROJECT: Final[str] = "[red3]𝙓 Could not create the project[/red3]"
CREATING_NEW_PROJECT: Final[str] = "[dodger_blue1]Creating your new project...[/dodger_blue1]\n"


class Check:
    @staticmethod
    def config_file_validator(config_file, json_schema) -> bool:
        try:
            jsonschema.validate(instance=config_file, schema=json_schema)
            return True
        except jsonschema.ValidationError as validation_error:
            if validation_error.relative_path:
                print(f"{validation_error.relative_path[0]}:")

                message_len = len(validation_error.relative_path) - 1
                if validation_error.validator == "required":
                    print(f"  {validation_error.message[1:-24]} (missing)\n")
                else:
                    print(f"  {validation_error.relative_path[message_len]}:(type error)\n")

            print(f"newproject: yaml config file error: {validation_error.message}")
            if validation_error.context:
                print(validation_error.context)
            if validation_error.cause:
                print(validation_error.cause)
            return False

    @staticmethod
    def dev_dir_check(dev_dir) -> bool:
        """
        Check if the development folder exists
        :return bool: True if the development folder exists
        """
        if not os.path.isdir(dev_dir):
            console.print(f"newproject: error: [red3]{dev_dir} does not exist[/red3]")
            console.print("[dark_orange3]Change it the YAML config file[/dark_orange3]")
            return False
        else:
            return True

    @staticmethod
    def projects_path_check(projects_dir_to_check: str) -> None:
        """
        Check if the specified programming language project folder exists
        :param projects_dir_to_check: (str) name of the programming language projects folder
        """
        if not os.path.isdir(projects_dir_to_check):
            console.print(f"newproject: error: [red3]{projects_dir_to_check} does not exist[/red3]")
            console.print("[dark_orange3]Change it the YAML config file[/dark_orange3]")
            sys.exit(errno.ENOENT)

    @staticmethod
    def project_name_check(project_name: str):
        """
        Checks if the project name contains a space
        :param project_name: (str) the name of the project
        """
        if " " in project_name:
            print("newproject: error: invalid project name. The project name can't contain spaces'")
            sys.exit(2)


class NewProject:

    def __init__(self):
        # Config file and JSON Schema
        self.YAML_CONFIG_FILE: Final[str] = select_config_file()
        self.JSON_SCHEMA_FILE: Final[str] = f"{get_config_path()}/schema/json_schema.json"

        # Loads YAML config file
        try:
            with open(self.YAML_CONFIG_FILE) as config_file:
                self.newproject_config = yaml.safe_load(config_file)
        except FileNotFoundError as yaml_file_not_found_error:
            logger.error(yaml_file_not_found_error)
            sys.exit(errno.ENOENT)

        # Loads JSON Schema file
        try:
            with open(self.JSON_SCHEMA_FILE) as json_schema_f:
                self.json_schema = json.load(json_schema_f)
        except FileNotFoundError as json_schema_not_found_error:
            logger.error(json_schema_not_found_error)
            sys.exit(errno.ENOENT)

        # Default Development folder
        self.DEV_DIR: Final[str] = f"{Path.home()}/{self.newproject_config['development_dir_path']}"

        self.check = Check()

        if self.check.config_file_validator(config_file=self.newproject_config, json_schema=self.json_schema):
            # Project folder names
            self.PROJECTS_DIR_NAMES: Final[dict] = {
                "bash": self.newproject_config["bash"]["projects_dir_name"],
                "c_lang": self.newproject_config["c_lang"]["projects_dir_name"],
                "cpp": self.newproject_config["cpp"]["projects_dir_name"],
                "go": self.newproject_config["go"]["projects_dir_name"],
                "java": self.newproject_config["java"]["projects_dir_name"],
                "lua": self.newproject_config["lua"]["projects_dir_name"],
                "ocaml": self.newproject_config["ocaml"]["projects_dir_name"],
                "php": self.newproject_config["php"]["projects_dir_name"],
                "python": self.newproject_config["python"]["projects_dir_name"],
                "ruby": self.newproject_config["ruby"]["projects_dir_name"],
                "rust": self.newproject_config["rust"]["projects_dir_name"],
                "vlang": self.newproject_config["vlang"]["projects_dir_name"],
                "web": self.newproject_config["web"]["projects_dir_name"],
            }
        else:
            sys.exit(2)

    @staticmethod
    def open_in_ide(ide_command: str, project_dir: str) -> None:
        """
        Open the project in the specified IDE
        :param ide_command: (str) the console command to open the IDE
        :param project_dir: (str) the project directory to open in the IDE
        """
        if which(f"{ide_command}") is not None:
            if ide_command in ["code", "pycharm", "idea"]:
                try:
                    subprocess.run([f"{ide_command}", project_dir])
                except Exception as open_in_ide_error:
                    logging.error(open_in_ide_error)
        else:
            print(f"newproject: {ide_command}: ide command not found")

    def git_init_command(self, project_dir: str, content: str) -> None:
        """
        Initialize a local git repository
        :param project_dir: (str) project directory
        :param content: (str) the content of the .gitignore file
        """
        console.print(
            "[dodger_blue1]Initializing [underline]git[/underline] repository[/dodger_blue1]"
        )
        if which("git") is not None:
            try:
                subprocess.run(["git", "init", project_dir])

                # Creating .gitignore file
                try:
                    with open(f"{project_dir}/.gitignore", "w") as gitignore_f:
                        if content != "":
                            gitignore_f.write(content)
                        else:
                            gitignore_f.write(self.newproject_config["default_gitignore_content"])

                        console.print("▶ [underline].gitignore[/underline] created.")

                        print(DONE)

                except Exception as gitignore_error:
                    logging.error(gitignore_error)
                    console.print("[red3]𝙓 Can't create .gitignore file[/red3]")

            except Exception as git_error:
                logging.error(git_error)
                console.print("[red3]𝙓 git repository not initialized[/red3]")

    @staticmethod
    def create_and_write_file(new_project_dir: str, file_name: str, content: str) -> None:
        """
        Creates and writes a file
        :param new_project_dir: (str) the directory of the new project
        :param file_name: (str) file's name
        :param content: (str) content to write to file
        """
        # Creating the file structure
        console.print(PROJECT_STRUCTURE_GEN)
        try:
            with open(f"{new_project_dir}/{file_name}", "w") as project_file:
                project_file.write(content)
                console.print(f"▶ [underline]{file_name}[/underline] created.")
            print(DONE)
        except Exception as create_and_write_file_error:
            logging.error(create_and_write_file_error)

    @staticmethod
    def create_python_venv(new_project_path: str) -> None:
        """
        Create a python venv
        :param new_project_path: (str) path of the new python project
        """
        console.print(
            "[dodger_blue1]Generating the [underline]venv[/underline]...[/dodger_blue1]"
        )
        try:
            # MacOS and Linux
            if sys.platform.startswith("darwin") or sys.platform.startswith("linux"):
                with console.status("[dodger_blue1]Generating...[/dodger_blue1]", spinner="aesthetic"):
                    subprocess.run(["python3", "-m", "venv", f"{new_project_path}/venv"])
            # Windows
            elif sys.platform.startswith("win32"):
                with console.status("[dodger_blue1]Generating...[/dodger_blue1]", spinner="aesthetic"):
                    if which("virtualenv") is not None:
                        subprocess.run(["virtualenv", f"{new_project_path}/venv"])
                    else:
                        subprocess.run(["python3", "-m", "venv", f"{new_project_path}/venv"])
            print(DONE)
        except Exception as venv_exception:
            logging.error(venv_exception)
            console.print("[red3]𝙓 Can't create venv [/red3]")

    @staticmethod
    def create_readme(new_project_dir, project_name):
        try:
            with open(f"{new_project_dir}/README.md", "w") as readme:
                readme.write(f"# {project_name}")
        except Exception as readme_error:
            logging.error(readme_error)
            console.print("[red3]𝙓 Can't create README.md file[/red3]")

    def create_project(
            self,
            projects_dir_name: str,
            project_name: str,
            file_name: str,
            file_content: str,
            gitignore_content: str,
            ide: str = "",
    ):
        """
        Create a new project
        :param projects_dir_name: (str) the name of the specified programming language's directory
        :param project_name: (str) the name of the new project
        :param file_name: (str) the name of the file
        :param file_content: (str) content to write to file
        :param gitignore_content: (str) the content of the .gitignore file
        :param ide: (str) the name of the IDE where you want to open the new project
        """
        if self.check.dev_dir_check(dev_dir=self.DEV_DIR):
            # check if the specified projects folder exists
            projects_path = os.path.join(self.DEV_DIR, projects_dir_name)

            self.check.projects_path_check(projects_dir_to_check=projects_path)
            # Creating the project folder
            new_project_dir = f"{projects_path}/{project_name}"

            try:
                console.print(CREATING_NEW_PROJECT)

                os.mkdir(new_project_dir)

                if projects_dir_name == self.PROJECTS_DIR_NAMES["python"]:
                    # Generating a python venv for the project
                    self.create_python_venv(new_project_path=new_project_dir)

                # Creating the file structure
                self.create_and_write_file(new_project_dir=new_project_dir, file_name=file_name, content=file_content)

                # Creating the README for the new project
                self.create_readme(new_project_dir=new_project_dir, project_name=project_name)

                # git init
                self.git_init_command(project_dir=new_project_dir, content=gitignore_content)

                # Open in IDE
                self.open_in_ide(ide_command=ide, project_dir=new_project_dir)

                console.print(HAPPY_CODING)

            except FileExistsError:
                console.print(
                    f"{new_project_dir} [bold red3]already exists![/bold red3]"
                )
                console.print(COULD_NOT_CREATE_PROJECT)
                sys.exit(errno.EEXIST)
        else:
            sys.exit(2)

    def create_project_with_commands(
            self,
            projects_dir_name: str,
            project_name: str,
            ide: str = "",
    ):
        """
        Create a new project via dedicated commands.
        :param projects_dir_name: (str) the name of the specified programming language's directory
        :param project_name: (str) the name of the new project
        :param ide: (str) the name of the IDE where you want to open the new project
        """
        if self.check.dev_dir_check(dev_dir=self.DEV_DIR):

            projects_path = os.path.join(self.DEV_DIR, projects_dir_name)

            self.check.projects_path_check(projects_dir_to_check=projects_path)
            # Creating the project folder
            new_project_dir = f"{projects_path}/{project_name}"

            try:
                if os.path.isdir(new_project_dir):
                    raise FileExistsError(errno.ENOENT, os.strerror(errno.ENOENT), new_project_dir)
                # Creating the project folder and file structure for the project
                console.print(CREATING_NEW_PROJECT)

                commands = []

                if projects_dir_name == self.PROJECTS_DIR_NAMES["rust"]:
                    commands = ["cargo", "new", new_project_dir]
                elif projects_dir_name == self.PROJECTS_DIR_NAMES["ruby"]:
                    commands = ["bundler", "gem", new_project_dir]
                elif projects_dir_name == self.PROJECTS_DIR_NAMES["ocaml"]:
                    commands = ["dune", "init", "project", new_project_dir]
                elif projects_dir_name == self.PROJECTS_DIR_NAMES["vlang"]:
                    commands = ["v", "new", new_project_dir]

                if which(commands[0]) is not None:
                    try:
                        subprocess.run(commands)
                        print(DONE)

                        # Open in IDE
                        self.open_in_ide(ide_command=ide, project_dir=new_project_dir)

                        console.print(HAPPY_CODING)
                    except Exception as command_exception:
                        logging.error(command_exception)
                        console.print(COULD_NOT_CREATE_PROJECT)
                else:
                    console.print(f"[red][underline]{commands[0]}[/underline]: command not found...[/red]")
            except FileExistsError:
                console.print(
                    f"{new_project_dir} [bold red3]already exists![/bold red3]"
                )
                console.print(COULD_NOT_CREATE_PROJECT)
                sys.exit(errno.EEXIST)
        else:
            sys.exit(2)

    def create_web_project(
            self,
            projects_dir_name: str,
            project_name: str,
            html_file_content: str,
            css_file_content: str,
            javascript_file_content: str,
            gitignore_content: str,
            ide: str = "",
    ):
        """
        Create a basic new web project
        :param projects_dir_name: (str) the name of the specified programming language's directory
        :param project_name: (str) the name of the new project
        :param html_file_content: (str) the content of the html file
        :param css_file_content: (str) the content of the css file
        :param javascript_file_content: (str) the content of the javascript file
        :param gitignore_content: (str) the content of the .gitignore file
        :param ide: (str) the name of the IDE where you want to open the new project
        """
        if self.check.dev_dir_check(dev_dir=self.DEV_DIR):
            # check if the specified projects folder exists
            projects_path = os.path.join(self.DEV_DIR, projects_dir_name)

            self.check.projects_path_check(projects_dir_to_check=projects_path)
            # Creating the project folder
            new_project_dir = f"{projects_path}/{project_name}"

            try:
                console.print(CREATING_NEW_PROJECT)

                os.mkdir(new_project_dir)
                os.mkdir(f"{new_project_dir}/styles")
                os.mkdir(f"{new_project_dir}/scripts")

                # Creating the file structure

                # Creating Html file
                self.create_and_write_file(new_project_dir=new_project_dir, file_name="index.html",
                                           content=html_file_content)
                # Creating Css file
                self.create_and_write_file(new_project_dir=f"{new_project_dir}/styles", file_name="style.css",
                                           content=css_file_content)
                # Creating Javascript file
                self.create_and_write_file(new_project_dir=f"{new_project_dir}/scripts", file_name="index.js",
                                           content=javascript_file_content)

                # Creating the README for the new project
                self.create_readme(new_project_dir=new_project_dir, project_name=project_name)

                # git init
                self.git_init_command(project_dir=new_project_dir, content=gitignore_content)

                # Open in IDE
                self.open_in_ide(ide_command=ide, project_dir=new_project_dir)

                console.print(HAPPY_CODING)

            except FileExistsError:
                console.print(
                    f"{new_project_dir} [bold red3]already exists![/bold red3]"
                )
                console.print(COULD_NOT_CREATE_PROJECT)
                sys.exit(errno.EEXIST)
        else:
            sys.exit(2)

    def handle(
            self,
            project_name: Annotated[str, typer.Argument(help="The name of the new project")],
            bash: Annotated[bool, typer.Option(help="create a bash project")] = False,
            clang: Annotated[bool, typer.Option(help="create a c project")] = False,
            cpp: Annotated[bool, typer.Option(help="create a cpp project")] = False,
            go: Annotated[bool, typer.Option(help="create a go project")] = False,
            java: Annotated[bool, typer.Option(help="create a java project")] = False,
            lua: Annotated[bool, typer.Option(help="create a lua project")] = False,
            ocaml: Annotated[bool, typer.Option(help="create an ocaml project")] = False,
            php: Annotated[bool, typer.Option(help="create a php project")] = False,
            python: Annotated[bool, typer.Option(help="create a python project")] = False,
            ruby: Annotated[bool, typer.Option(help="create a ruby project")] = False,
            rust: Annotated[bool, typer.Option(help="create a rust project")] = False,
            vlang: Annotated[bool, typer.Option(help="create a vlang project")] = False,
            web: Annotated[bool, typer.Option(help="create a basic web project")] = False,
            code: Annotated[bool, typer.Option(help="open the project in VS Code")] = False,
            idea: Annotated[bool, typer.Option(help="open the project in Intellij IDEA")] = False,
            pycharm: Annotated[bool, typer.Option(help="open the project in PyCharm")] = False
    ):
        """
        Create a new project via terminal

        Coded with <3 by utox39
        """

        # Checks if the project_name contains a space
        check = Check()
        check.project_name_check(project_name)

        ide_name = ""
        if code:
            ide_name = "code"
        elif pycharm:
            ide_name = "pycharm"
        elif idea:
            ide_name = "idea"

        project_mapping = {
            python: (self.create_project,
                     self.PROJECTS_DIR_NAMES["python"],
                     project_name,
                     f"{project_name}.py",
                     self.newproject_config["python"]["file_content"],
                     self.newproject_config["python"]["gitignore_content"],
                     ide_name
                     ),
            java: (self.create_project,
                   self.PROJECTS_DIR_NAMES["java"],
                   project_name,
                   "Main.java",
                   self.newproject_config["java"]["file_content"],
                   self.newproject_config["java"]["gitignore_content"],
                   ide_name
                   ),
            go: (self.create_project,
                 self.PROJECTS_DIR_NAMES["go"],
                 project_name,
                 "main.go",
                 self.newproject_config["go"]["file_content"],
                 self.newproject_config["go"]["gitignore_content"],
                 ide_name
                 ),
            bash: (self.create_project,
                   self.PROJECTS_DIR_NAMES["bash"],
                   project_name,
                   f"{project_name}.sh",
                   self.newproject_config["bash"]["file_content"],
                   self.newproject_config["bash"]["gitignore_content"],
                   ide_name
                   ),
            cpp: (self.create_project,
                  self.PROJECTS_DIR_NAMES["cpp"],
                  project_name,
                  "main.cpp",
                  self.newproject_config["cpp"]["file_content"],
                  self.newproject_config["cpp"]["gitignore_content"],
                  ide_name
                  ),
            clang: (self.create_project,
                    self.PROJECTS_DIR_NAMES["c_lang"],
                    project_name,
                    "main.c",
                    self.newproject_config["c_lang"]["file_content"],
                    self.newproject_config["c_lang"]["gitignore_content"],
                    ide_name
                    ),
            php: (self.create_project,
                  self.PROJECTS_DIR_NAMES["php"],
                  project_name,
                  "index.php",
                  self.newproject_config["php"]["file_content"],
                  self.newproject_config["php"]["gitignore_content"],
                  ide_name
                  ),
            lua: (self.create_project,
                  self.PROJECTS_DIR_NAMES["lua"],
                  project_name,
                  "main.lua",
                  self.newproject_config["lua"]["file_content"],
                  self.newproject_config["lua"]["gitignore_content"],
                  ide_name
                  ),
            rust: (self.create_project_with_commands,
                   self.PROJECTS_DIR_NAMES["rust"],
                   project_name,
                   ide_name
                   ),
            ruby: (self.create_project_with_commands,
                   self.PROJECTS_DIR_NAMES["ruby"],
                   project_name,
                   ide_name
                   ),
            ocaml: (self.create_project_with_commands,
                    self.PROJECTS_DIR_NAMES["ocaml"],
                    project_name,
                    ide_name
                    ),
            vlang: (self.create_project_with_commands,
                    self.PROJECTS_DIR_NAMES["vlang"],
                    project_name,
                    ide_name),
            web: (self.create_web_project,
                  self.PROJECTS_DIR_NAMES["web"],
                  project_name,
                  self.newproject_config["web"]["html_file_content"],
                  self.newproject_config["web"]["css_file_content"],
                  self.newproject_config["web"]["javascript_file_content"],
                  self.newproject_config["web"]["gitignore_content"],
                  ide_name
                  )
        }

        for flag, func_and_proj_info in project_mapping.items():
            if flag:
                create_func, *args = func_and_proj_info
                create_func(*args)
                break
        else:
            console.print("[bold red]No option provided[/bold red]")


def get_config_path():
    # Gets the site-packages path
    site_packages = ""
    if sys.platform.startswith("darwin"):
        site_packages = site.getsitepackages()[0]
    elif sys.platform.startswith("linux"):
        if os.path.exists(site.getusersitepackages()):
            site_packages = site.getusersitepackages()
    elif sys.platform.startswith("win32"):
        site_packages = site.getsitepackages()[1]

    newproject_cli_config_files_path = os.path.join(site_packages, "newproject/config")

    return newproject_cli_config_files_path


def select_config_file() -> str:
    """
    Checks the presence of the configuration file in .config and if it exists it returns its path,
    otherwise it returns the path of the one located in site_packages.
    :return: (str) the config file path
    """
    dot_config_yaml_file = f"{Path.home()}/.config/newproject/newproject_config.yaml"
    site_packages_config_file = f"{get_config_path()}/newproject_config.yaml"

    if os.path.exists(dot_config_yaml_file):
        return dot_config_yaml_file
    else:
        return site_packages_config_file


def main():
    typer.run(NewProject().handle)


if __name__ == "__main__":
    main()
