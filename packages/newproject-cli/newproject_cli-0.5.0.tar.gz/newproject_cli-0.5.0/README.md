# new-project-cli

[![codecov](https://codecov.io/gh/utox39/new-project-cli/graph/badge.svg?token=LLIV4AFVY6)](https://codecov.io/gh/utox39/new-project-cli)
[<img alt="PyPI - Version" src="https://img.shields.io/pypi/v/newproject-cli">
](https://pypi.org/project/newproject-cli/)
[<img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dw/newproject-cli">
](https://pypistats.org/packages/newproject-cli)
[<img alt="GitHub Workflow Status (with event)" src="https://img.shields.io/github/actions/workflow/status/utox39/new-project-cli/newproject-cli-tests.yaml">
](https://github.com/utox39/new-project-cli/actions/workflows/newproject-cli-tests.yaml)
---

[![asciicast](https://asciinema.org/a/RduB1EVKNj1zp9Gw0kCbptpFZ.svg)](https://asciinema.org/a/RduB1EVKNj1zp9Gw0kCbptpFZ)

- [Description](#description)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
    - [Customization](#customization)
- [Roadmap](#roadmap)
- [Contributing](#contributing)

## Description

Create a new project from the terminal.

This tool will help you create a minimal structure for your new project.

You can create new:

- Bash projects
- C projects
- Cpp projects
- Go projects
- Java projects
- Lua projects
- OCaml projects
- PHP projects
- Python projects
- Ruby projects
- Rust projects
- Vlang projects
- Web projects (html, css, javascript)

and open them in:

- [Visual Studio Code](https://code.visualstudio.com/)
- [PyCharm](https://www.jetbrains.com/pycharm/)
- [IntelliJ IDEA](https://www.jetbrains.com/idea/)

### Why these programming languages?

I mainly based myself on the percentages reported by
[Stackoverflow's 2023 Developer Survey](https://survey.stackoverflow.co/2023/)
for the
["Programming, scripting, and markup languages"](https://survey.stackoverflow.co/2023/#section-most-popular-technologies-programming-scripting-and-markup-languages)
section, and I selected the most used languages and those
that I consider to be the most promising or interesting

### Default development directories tree

```
$HOME
└──Developer
   └── projects
       ├── bash_projects
       ├── c_projects
       ├── cpp_projects
       ├── go_projects
       ├── java_projects
       ├── lua_projects
       ├── ocaml_projects
       ├── php_projects
       ├── python_projects
       ├── ruby_projects
       ├── rust_projects
       ├── vlang_projects
       └── web_projects
```

### Projects created via commands

E.g: To create a new Rust project, newproject use the following command:

```console
$ cargo new project_name
```

So it use the default command to create a new cargo package.

The same is for Ruby, OCaml and Vlang.

## Requirements

- [Python](https://www.python.org/)
- [pip](https://packaging.python.org/en/latest/tutorials/installing-packages/)

#### To create a Rust projects

- [Rust](https://www.rust-lang.org/learn/get-started)

#### To create a Ruby projects

- [Ruby](https://www.ruby-lang.org/en/documentation/installation/)
- [bundler](https://rubygems.org/gems/bundler)

#### To create a OCaml projects

- [OCaml](https://ocaml.org/install)
- [dune](https://ocaml.org/install)

## Installation

This tool currently only works for [*NIX](https://en.wikipedia.org/wiki/Unix-like) operating systems

Easy as you can see here:

```console
$ pip install newproject-cli
```

Please note: After installing newproject with pip if you have not added ~/.local/bin (macOS/Linux) to $PATH you will be
asked to do so with a warning that should look like this:

```console
WARNING: The script newproject is installed in '/home/ubuntu/.local/bin' which is not on PATH.
Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
```

## Usage

#### Create a new python project

```console
$ newproject --python project_name
```

#### Create a new web project

```console
$ newproject --web project_name
```

This command will create a very simple web project with this structure:

```
project_name
├── README.md
├── index.html
├── scripts
│   └── index.js
└── styles
    └── style.css
```

#### Create a new project and open it in Visual Studio Code

WARNING: In order to open the new project in your favorite IDE you need to have the shell command

```console
$ newproject --code --python project_name
```

### Customization

The default yaml config file is located in site_packages

#### How can I find the default config file?

```console
$ pip3 show newproject-cli
Name: newproject-cli
Version: 0.x.x
Summary: A command-line tool to create new projects
Home-page: https://github.com/utox39/new-project-cli
Author: utox39
Author-email: francescomoccaldi39@gmail.com
License: MIT
Location: path/to/site-packages <-- LOOK HERE
Requires: jsonschema, pyyaml, rich, typer, typing_extensions
Required-by:

$ cd path/to/site-packages/newproject/config
```

#### YAML config file in ~/.config/newproject (macOS/Linux only)

The default configuration file is located in the site_packages folder, but you can also use a configuration file that
you
can create in the ~/.config/newproject folder.

ATTENTION: Using this config file does not involve updating to the latest features involving the default
config file (located in the site_packages), therefore it requires manual intervention

Let's see how you can do it:

- Create the configuration folder and the YAML config file

```console
$ cd ~/.config
$ mkdir newproject
$ touch newproject_config.yaml
```

- Open the YAML file in your editor of choice

- Copy the contents
  of [this](https://github.com/utox39/new-project-cli/blob/main/newproject/config/newproject_config.yaml) file into the
  YAML file

- Done

#### Customize the Development folder

In newproject_config.yaml:

```yaml
development_dir_path: path/to/your/development/folder/
```

E.g:

```yaml
development_dir_path: Documents/projects/
```

#### Customize a programming language projects folder

In newproject_config.yaml:

```yaml
project_folder_names:
  python_projects_dir_name: python_projects
```

#### Customize a programming language file content

In newproject_config.yaml:

You can customize the content of the files only of the following programming languages:

- Bash
- C
- Cpp
- Go
- Java
- Lua
- PHP
- Python
- Web projects (html, css, javascript)

```yaml
cpp:
  file_content: |
    #include <iostream>

    int main()
    {
        std::cout<<"hello world"<<'\n';
        return 0;
    }
```

#### Customize the .gitignore for a specific programming language

In newproject_config.yaml:

You can customize the content of the .gitignore only of the following programming languages:

- Bash
- C
- Cpp
- Go
- Java
- Lua
- PHP
- Python
- Web projects (html, css, javascript)

```yaml
python:
  gitignore_content: |
    DS_Store
    .env
    .vscode/
    .idea/
    test/
    venv/
```

#### Customize the default .gitignore

```yaml
default_gitignore_content: |
  .DS_Store
  .env
  .vscode/
  .idea/
  test/
  foo/
```

## Roadmap

- Improve customization
- Add more programming languages
- Add more IDE
- Improve user output and experience
- Publish this project to package managers

## Contributing

If you would like to contribute to this project just create a pull request which I will try to review as soon as
possible.
