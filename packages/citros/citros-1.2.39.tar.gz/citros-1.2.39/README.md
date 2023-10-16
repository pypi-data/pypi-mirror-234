# CITROS CLI

# Table of Contents
1. [Description](#Description)
2. [Prerequisites](#Prerequisites)
3. [Installation](#Installation)
4. [CLI Commands](#CLI-Commands)  
   1. [Quick Start](#Quick-Start)
   2. [init](#init)
   3. [setup-ssh](#setup-ssh)
   4. [status](#status)
   5.  [add-remote](#add-remote)
   6.  [commit](#commit)
   7.  [pull](#pull)
   8.  [push](#push)
   9.  [diff](#diff)
   10. [checkout](#checkout)
   11. [merge](#merge)
   12. [discard](#discard)
   13. [login](#login)
   14. [logout](#logout)
   15. [list](#list)
   16. [run](#run)
   17. [docker-build](#docker-build)
   18. [docker-build-push](#docker-build-push)
5. [Citros Repository directory and file Structure](#citros-project-file-structure) 
   1. [notebooks](#notebooks)
   2. [parameter setups](#parameter-setups)
   3. [reports](#reports)
   4. [runs](#runs)
   5. [simulations](#simulations)
   6. [workflows](#workflows)
   7. [project.json](#projectjson)
   8. [settings.json](#settingsjson)
6. [Citros Repository Configuration](#citros-repository-configuration)
    1. [Adding functions to parameter setup](#adding-functions-to-parameter-setup)
        1. [How to Add Function Objects](#how-to-add-function-objects)
        2. [Examples - numpy](#examples---numpy)
        3. [Examples - user-defined](#examples---user-defined)
        4. [Examples - full parameter_setup.json example](#examples---full-parameter_setupjson-example)
        5. [Pitfalls and Gotchas](#pitfalls-and-gotchas)
7. [User Templates](#user-templates)


# Description

Welcome to Citros CLI. [Citros](http://citros.io/) serves as an innovative platform for executing ROS project simulations, automating integration, and conducting in-depth performance analysis.

The Citros CLI offers ROS 2 developers a seamless interface to launch multiple ROS simulations for a specific project with just a single command. Beyond setting static parameter values, it empowers users with the flexibility to utilize function objects. This means you can craft dynamic simulation environments where each execution produces unique parameter values, whether they're sourced from standard numpy functions or tailored via user-defined computations. Moreover, these operations can be executed offline without relying on any external dependencies.

Citros takes its capabilities a notch higher when the user logs in. Once logged in, users can tap into the full potential of Citros, ranging from running parallel simulations in the cloud to utilizing advanced data analysis tools for performance examination. Additionally, automatic report generation is a standout feature, aiding in effortless documentation of your work. Beyond these technical perks, logging in also paves the way for collaborative work, allowing you to engage and exchange ideas with team members.

For additional information, please refer to the Citros documentation. This will provide you with comprehensive insights and detailed instructions for effective usage of Citros in general and Citros CLI in particular, and their full suite of features.

We are dedicated to enriching your ROS project simulation experience, and this package is our contribution to that cause.


# Prerequisites

- [vscode](https://code.visualstudio.com/download)
- [Docker](https://www.docker.com/)
- [Python3](https://www.python.org/downloads/)
- [git](https://git-scm.com/)

# Installation
### option 1: without code:

        $ pip install citros 

### option 2: with code:

1. clone the repo:
    
        $ git clone git@github.com:lulav/citros_cli.git

2.  Within the cloned `citros_cli` folder, Install the package to a global bin folder:

        $ python3 -m pip install .
        $ source ~/.profile

### option 3: with code and soft links
If you are developing the citros_cli package itself, than the best practice is to create a `utils` directory under a ROS project, clone the repo into it, and install the package with soft links to dev environment. I.e. from your ROS project dir:

        $ mkdir utils && cd utils
        $ git clone git@github.com:lulav/citros_cli.git
        $ cd ..
        $ python3 -m pip install -e utils/citros_cli
    
3. Environment Variables. 
   
   `citros_cli` uses several environment variables, some of which you may change according to your needs, although for the most part, the defaults are likely to be what you want. Generally speaking, most of these are only used by developers of the package, and should not be used.

| ENV | Description | used in |
| --- | --- | --- |
| `CITROS_DOMAIN` | The main domain, defaults to `citros.io` | all packages |
| `CITROS_DIR` | Used by the citros cluster, do not use. | citros |
| `CITROS_SIM_RUN_DIR` | The directory under `.citros/runs` in which all simulation data will be saved (see [runs](#runs)). This can be handy, if your code needs to know this location in order to access some of the files, e.g. parameter setups. | citros |


# CLI Commands

### Quick Start:

#### run locally

In essence, the Citros CLI is a collection of numerous commands, but to quickly get started with running a simulation once using the default parameter values, only two straightforward commands are required:

    $ citros init
    User is not logged in. Initialzing Citros locally.
    Intialized Citros repository.
    $ citros run -n "some_batch_name" -m "some_message"

The first command, `citros init`, sets up a new `.citros` repository. If you are logged in, it will clone the `.citros` directory from a remote repository.

The second command, `citros run`, executes a simulation of the provided name a designated number of times. If you don't specify a simulation name (not to be confused with a batch name, which is mandetory by default), an interactive menu will appear, letting you select from the available simulations. If the "completions" value, representing the number of times the simulation should run, isn't specified, a single instance of the simulation will be executed.

#### run remotely (on the cloud)

In order to run your simulation on the cloud, two (possibly three) additional steps are required:

1. First of all, you would need to login to citros by running `citros login`. 
2. After logging in, and before running `citros init`, **if you haven't done so already**, you would need to setup your ssh keys in order communicate with the Citros server. One way to do this is through the [Citros](https://citros.io) web GUI (which provides detailed instructions), but this may also be done through the CLI by running `citros setup-ssh`. see details [below](#setup-ssh).

3. Once ssh is setup, you may run `citros init`. This will pull an existing Citros repository from the Citros server, or create a new one.

4. Now, you will need to build a docker image of your simulation and upload it Citros, by running `citros docker-build-push`.

5. Finally, you may run your simulation on the cloud by simply adding `-r` to the `citros run` command. The image you uploaded in the previous step will be run the number of times you specified.

To sum up, assuming you have already setup your ssh keys, the following example will run a simulation 10 times on the Citros cloud:

    $ citros login
    $ citros init
    $ citros docker-build-push
    $ citros run -n "some_batch_name" -m "some_message" -r -c 10

**Note:** for clarity, the citros output was not given in the above example. See individual commands.

## init
The `init` command is used to initialize a Citros repository. Depending on the user's login status, this behavior varies. For logged-out users, the project initializes locally. However, logged-in users will have the `.citros` directory cloned from the Citros remote repository. If it's a new project, an empty project will be cloned.

The initialization process involves creating a `.citros` directory within your ROS project directory and generating several files and folders therein. These files are set up to allow you to run a simulation of your project with default configurations and settings. You can tailor your Citros repository to your specific needs by manually modifying these files (see the [Project Configuration](#citros-project-configuration) section below for more details).

**Note:** the initialization process will also make sure that within your Citros repo, you are working on a branch whose name is the same as the current branch in your ROS project. It will do so by checking it out (and possibly creating such a branch if it does not already exist).

### parameters:
parameter|description
|--|--|
|`-dir` <folder_name> | Specifies the project's working directory. Defaults to `.`|
|`-d`, `--debug` | Sets the logging level to debug.|
|`-v`, `--verbose` | Enables verbose console output.|
|`-project_name` <proj_name> | Optional name for the project. Defaults to the last folder in the path of *dir*|

### examples

example 1 - initializing while logged out:

    $ citros init
    User is not logged in. Initialzing Citros locally.
    Intialized Citros repository.

example 2 - initializing while logged in:

    $ citros init
    Checking internet connection...
    Checking ssh...
    Updating Citros...
    Waiting for repo to be ready...
    Citros repo successfully cloned from remote.
    Citros successfully synched with local project.
    You may review your changes via `citros status` and commit them via `citros commit`.
    Intialized Citros repository.

Note: The init command can only be executed with effect once per project. If you attempt to initialize an existing Citros repository, you will be notified that the action is redundant, and no changes will be made. Example:

    $ citros init
    The directory /workspaces/cannon has already been initialized.
    No remotes found and user is not logged in. Working offline.

To re-initialize an existing Citros repository, you must first delete the existing .citros directory for your project.

## setup-ssh
The `setup-ssh` command sets up SSH keys for secure communication with the remote Citros repository.

Setting up your ssh keys can be done in several different ways. You can do it manually by yourself, following the instructions on the [citros.io](https://citros.io) website, or you can use the `setup-ssh` command to automate this process.

When using `setup-ssh`, you may run it directly on your computer, in which case you will only ever need to run it once. This, of course, means you'll need to install the citros-cli directly on you computer, rather than inside a dev-container. 

If you'd rather avoid this, you can also run `setup-ssh` inside a dev container, but the price in that case, is that you'll have to run it once for each dev-container you use (and again if you rebuild the dev-container). Also, since you are prompted to give a unique title for the ssh key that will be generated, you will have to do so every time you run `setup-ssh`. 

In any case, you may view (and possibly delete) your keys in your profile settings on the [citros.io](https://citros.io) website. 

**Note:** this command *may* append some bash commands to the end of any of the following user profile files, if they exist in the user's home directory: `~/.bashrc` , `~/.bash_profile`, `~/.zprofile`. 

### prerequisites:
- user must be logged in (using `citros login`).

### parameters:
parameter|description
|--|--|
|`-d`, `--debug` | Sets the logging level to debug.|
|`-v`, `--verbose` | Enables verbose console output.|

## status
The `status` command first syncs any changes in your ROS project with your Citros repository and than retrieves the current state of your Citros repository. Essentially, it acts as a wrapper for the `git status` command specifically for your Citros repository.

This command provides a quick and concise overview of the changes made to your project, giving you insights into tracked, modified, and staged files.

### parameters:
parameter|description
|--|--|
|`-dir` <folder_name> | Specifies the project's working directory. Defaults to `.`|
|`-d`, `--debug` | Sets the logging level to debug.|
|`-v`, `--verbose` | Enables verbose console output.|

### example

In the example below, we employ the `status` command to gain insight into the condition of our Citros repository. This becomes particularly beneficial when there's a divergence between your local and remote branches—like when the remote branch receives updates you haven't pulled yet, while you've committed local changes still awaiting a push to the remote.:

    $ citros status
    On branch main
    Your branch and 'origin/main' have diverged,
    and have 1 and 4 different commits each, respectively.

    nothing to commit, working tree clean
    $ citros pull
    $ citros status
    On branch main
    Your branch is ahead of 'origin/main' by 2 commits.

    nothing to commit, working tree clean
    $ citros push
    $ citros status
    On branch main
    Your branch is up to date with 'origin/main'.

    nothing to commit, working tree clean

## add-remote
The `add-remote` command associates a remote Citros repository, named `origin`, with your local repository. This remote repository is hosted on the Citros servers.

### prerequisites:
`citros setup-ssh` has already been run.

**Important**: If you execute `citros init` while logged in, the `add-remote` command will automatically run in the background, making a direct call unnecessary. However, if you initially ran `citros init` while logged out and later decide to work with the online Citros system (e.g., running commands like `citros push`), you will need to manually run the `add-remote` command.

Furthermore, to ensure secure communication with the server, the `setup-ssh` command should be executed before running add-remote.

### parameters:
parameter|description
|--|--|
|`-dir` <folder_name> | Specifies the project's working directory. Defaults to `.`|
|`-d`, `--debug` | Sets the logging level to debug.|
|`-v`, `--verbose` | Enables verbose console output.|

## commit
The `commit` command captures all modifications to your local Citros repository in a snapshot, essentially serving as a wrapper for the `git commit` command, but tailored to your Citros repository.

By executing this command, you essentially save the current state of your project, allowing you to keep track of your progress, revert changes, and even collaborate more effectively. This forms an integral part of managing and controlling the version history of your Citros repository.

### parameters:
parameter|description
|--|--|
|`-dir` <folder_name> | Specifies the project's working directory. Defaults to `.`|
|`-d`, `--debug` | Sets the logging level to debug.|
|`-v`, `--verbose` | Enables verbose console output.|
|`-m`, `--message` | Commit message|

### example:

    $ citros commit -m "added an awesome feature"

## pull
The `pull` command fetches from and integrates with another Citros repository or a local branch. Essentially, it acts as a wrapper for the `git pull` command within the context of your Citros repo.

**Note:** if there conflicts between your local copy and the remote copy that cannot be resolved automatically, than a manual merge will have to take place. Not to worry - Citros makes this process user-friendly - see [Merge](#merge) for details.

### parameters:
parameter|description
|--|--|
|`-dir` <folder_name> | Specifies the project's working directory. Defaults to `.`|
|`-d`, `--debug` | Sets the logging level to debug.|
|`-v`, `--verbose` | Enables verbose console output.|

### example

    $ citros pull

## push
The `push` command transfers all committed changes in your local Citros repository to the remote repository. Essentially, it acts as a wrapper for the `git push` command within the context of your Citros repo.

By employing the `push` command, you are synchronizing your local project modifications with the remote repository. This is crucial not only for backing up your work on the server but also for enabling seamless collaboration with other team members using the Citros platform.

### parameters:
parameter|description
|--|--|
|`-dir` <folder_name> | Specifies the project's working directory. Defaults to `.`|
|`-d`, `--debug` | Sets the logging level to debug.|
|`-v`, `--verbose` | Enables verbose console output.|

### example

    $ citros push
    35461c6..d60a662

    Successfully pushed to branch `main`.
    $ citros push
    [up to date]

    Successfully pushed to branch `main`.

In the example above you can see that when there is a local commit to be pushed to the remote, `citros push` will push it and specify its commit hash. When running this command while already synched with the remote, you will be notified accordingly. 

## diff
The `diff` command presents you with a detailed description of all differences between the latest commit and your working directory. New lines will be colored in green, and deleted lines will be colored in red.

### parameters:
parameter|description
|--|--|
|`-dir` <folder_name> | Specifies the project's working directory. Defaults to `.`|
|`-d`, `--debug` | Sets the logging level to debug.|
|`-v`, `--verbose` | Enables verbose console output.|

### example:
    $ citros diff
    diff --git a/simulations/simulation_cannon_analytic.json b/simulations/simulation_cannon_analytic.json
    index e7c823f..178c95b 100644
    --- a/simulations/simulation_cannon_analytic.json
    +++ b/simulations/simulation_cannon_analytic.json
    @@ -5,7 +5,7 @@
            "file": "cannon_analytic.launch.py",
            "package": "scheduler"
        },
    -    "timeout": 60,
    +    "timeout": 42,
        "GPU": 0,
        "CPU": 2,
        "MEM": "265MB",

## checkout
The `checkout` command lets you check out a different branch than the one your are currently on. It essentially wraps the `git checkout` command. If you have any uncommitted changes in your Citros working directory, you will be asked if you want to commit those changes. If you decline, the checkout will not take place, since Citros doesn't allow checking out while the working directory is dirty.

If the branch you're attempting to check out exists (locally or on the remote), it will be checked out. If it doesn't exist yet, you will be asked if you would like to create it. If you decline, the checkout will not take place.

### parameters:
parameter|description
|--|--|
|`-dir` <folder_name> | Specifies the project's working directory. Defaults to `.`|
|`-d`, `--debug` | Sets the logging level to debug.|
|`-v`, `--verbose` | Enables verbose console output.|
|`-b`, `--branch` | The name of the branch to be checked out.|

### example

In the following example we checkout the branch `master` (not before confirming we want to commit the changes in our working directory), and then checkout the branch `main`. 

    $ citros checkout -b master
    Cannot checkout: there are uncommitted changes in your repo.
    Would you like to commit them? (y/n) y
    Checking out local branch master
    $ citros checkout -b main
    Checking out local branch main

## merge
The `merge` command enables you to integrate another branch into your current one. You'll be shown a list of accessible branches to select from. When both your branch and the target branch have modifications to the same file, the outcome varies based on the nature of these changes. Non-conflicting changes will be seamlessly merged. 

However, if conflicts arise, the merge operation halts, requiring you to address these discrepancies manually, using a diff/merge tool. 

### example

In the following example we attempt to merge the branch `master` into the current branch:

    $ citros merge
    ? Please choose the branch you wish to merge into the current branch: master
    Merge failed due to conflicting changes between the current branch and `master`.
    Files with conflicts:
    - notebooks/test.ipynb
    Please resolve the conflicts manually.
    ...

If you are not running inside a dev-container, an instance of VS-Code will be automatically opened (pending your aproval) for you to use a merge tool. After all conflicts have been resolved, save the files, close VS-Code and answer `y` to indicate that all conflicts have indeed been resolved. At this point Citros will commit the merge on your behalf.

If you are running inside a dev-container, you'll have to run a few git commands by yourself, but not to worry - Citros will provide you with step-by-step instructions:


    $ citros merge
    ? Please choose the branch you wish to merge into the current branch: test_branch
    Merge failed due to conflicting changes between the current branch and `test_branch`.
    Files with conflicts:
    - parameter_setups/functions/my_func.py
    Please resolve the conflicts manually.
    Since you are running inside a dev-container, you'll have to:
    1. Open a terminal, e.g.
    ctrl-alt-t
    2. Navigate to the .citros directory under your project, e.g.
    cd path/to/your/project/.citros
    3. Run the following two commands to set VS code as the git merge tool for your .citros repo:
    git config merge.tool code
    git config mergetool.code.cmd "code --wait $MERGED"
    (if you already have a merge tool set for git, you may skip this step).
    4. Open your mergetool (i.e. VS code) to resolve the conflict:
    git mergetool

    After all conflicts have been resolved, save the files, close the merge tool, answer y in the terminal and close it.
    Press y to commit the merge or n to abort the merge.
    Note: if you press y and there are still unresolved conflicts, the merge will still be aborted.
    All conflicts resolved (y/n): y
    Conflicts resolved. Committing the merge...


**Note:** For files that Citros manages, like `project.json`, conflicts will be auto-resolved in favor of the current branch's version.

### parameters:
parameter|description
|--|--|
|`-dir` <folder_name> | Specifies the project's working directory. Defaults to `.`|
|`-d`, `--debug` | Sets the logging level to debug.|
|`-v`, `--verbose` | Enables verbose console output.|

## discard
The `discard` command allows to you discard any uncommitted changes in your Citros working directory. Simply specify the file paths of the files you would like to discard. Notice you have to specify the file paths relative to the `.citros` directory. 

If you'd like discard **all** changes in your working directory, effectively checking out the HEAD commit, instead of specifying individual file paths, you may use the --ALL flag.

**Notice**: the effects of this command cannot be undone.

### parameters:
parameter|description
|--|--|
|`-dir` <folder_name> | Specifies the project's working directory. Defaults to `.`|
|`-d`, `--debug` | Sets the logging level to debug.|
|`-v`, `--verbose` | Enables verbose console output.|
|`files` | List of files to revert.|
|`--ALL` | Revert all files.|

### example
```bash
$ citros status
On branch main
Your branch is up to date with 'origin/main'.

Changes not staged for commit:
        modified:   project.json

$ citros discard project.json
$ citros status
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

or, using the --ALL flag:
```bash
$ citros discard --ALL
Warning: all of the following changes will be discarded:
Modified files:
   - project.json
Discard all changes? (yes/no): yes
All changes in the working directory have been reverted to the last commit.
```

## login
The `login` command allows you to authenticate your session with Citros. To use this command, you must already have a registered account with [Citros](citros.io), including a valid username (email) and password.

By logging in, you unlock additional features such as cloud-based simulations, data analysis tools, automated report generation, and collaboration with other Citros users. Use this command to seamlessly integrate your local workspace with the Citros platform and fully utilize its capabilities.

### parameters:
parameter|description
|--|--|
|`-d`, `--debug` | Sets the logging level to debug.|
|`-v`, `--verbose` | Enables verbose console output.|
|`-username` | The user's username (email).|
|`-password` | The user's password|

After entering the command, if either the username or password was not given, you will be prompted for your email (the username) and password.

### example:

    $ citros login
    $ email: shalev@lulav.space
    $ Password: 
    User logged in.


## logout
The logout command terminates your active session with Citros.

### parameters:
parameter|description
|--|--|
|`-d`, `--debug` | Sets the logging level to debug.|
|`-v`, `--verbose` | Enables verbose console output.|

### example:

    $ citros logout
    User logged out.

## list
The `list` command displays all available simulation names. These names are derived from the filenames in the `simulations` folder within your Citros repository. Each of these files corresponds to an available launch file in your ROS project. For instance, if your ROS project contains a launch file named `foo.launch.py`, a corresponding simulation file named `simulation_foo.json` will be generated in your simulations folder.

### parameters:
parameter|description
|--|--|
|`-d`, `--debug` | Sets the logging level to debug.|
|`-v`, `--verbose` | Enables verbose console output.|

### example:

    $ citros list
    1. simulation_cannon_analytic
    2. simulation_cannon_numeric


## run
The `run` command launches a simulation either locally on your machine, or remotely on the Citros cluster.

### prerequisites:
Ensure that the project has been built and sourced, for example:
    
    $ colcon build
    $ source install/local_setup.bash

If you'd like to run your simulation remotely, you would also need to make sure:
1. You're logged in (via `citros login`).
2. You've built and pushed a docker image of your project (using `citros docker-build-push`).
3. Your `.citros` directory is synched with the remote repository (using `citros commit` and `citros push`). 

### parameters:
parameter|description
|--|--|
|`-dir` <folder_name> | Specifies the project's working directory. Defaults to `.`|
|`-d`, `--debug` | Sets the logging level to debug.|
|`-v`, `--verbose` | Enables verbose console output.|
|`-s`, `--simulation_name` | Identifies the simulation you want to run. This is the name of the JSON file (excluding the `json` suffix) in the `simulations` folder. If you don't provide a simulation name, an interactive menu will display allowing you to select from the available simulations.|
|`-b`, `--batch_id` | Batch ID. Intended for Citros internal use only - DO NOT USE.|
|`-n`, `--batch_name` | Assigns a descriptive name for this simulation run, e.g. according to its settings and/or parameter setup. You can disable this option requirement via `settings.json`. If disabled, and no name is given, the default name will be the date and time.|
|`-m`, `--batch_message` | Provides a descriptive message for this simulation run, e.g. according to its settings and/or parameter setup. This can also be disabled via `settings.json`.|
|`-i`, `--run_id` | Simulation run ID. Intended for Citros internal use only - DO NOT USE.|
|`-c`, `--completions` | Sets the number of completions (simulation runs). Defaults to 1 if not specified.|
|`-r`, `--remote` | Executes the simulation remotely on the cluster. See prerequisites above for details.|
|`-k`, `--key` | Authentication key. Intended for Citros internal use only - DO NOT USE.|
|`-l`, `--lan_traffic` | A flag which causes the simulation to receive LAN ROS traffic.|
|`--branch` | The git branch name citros should use when running you simulation remotely. Defaults to active branch. For remote run only, will be ignored otherwise.|
|`--commit` | The git commit hash citros should use when running you simulation remotely. defaults to latest commit. For remote run only, will be ignored otherwise.|


If no simulation name was provided, an interactive session will begin, and you will be prompted to select a simulation from the list of available simulations (via up, down and enter keys). 

### example:

    $ citros run
    ? Please choose the simulation you wish to run 
    ❯ simulation_cannon_analytic
      simulation_cannon_numeric

**Note:** the `-n` and `-m` flags are mandatory by default. If you would like them to be optional, you can set the `force_batch_name` and `force_message` flags in `settings.json` to `"False"`. In that case, batch names will default to the date and time the simulation was run. 


## docker-build
The `docker-build` command is used to construct a Docker image of your ROS project. This image encapsulates your project's environment, facilitating the portability and reproducibility of your simulations across different systems.

### prerequisites
If you are working inside a dev-container, make sure that the `docker-in-docker` feature is enabled in your project's `devcontainer.json`, i.e.:

    "features": {
		"ghcr.io/devcontainers/features/docker-in-docker:2": {
			"version": "latest",
			"moby": true
		}
	}

### parameters:
parameter|description
|--|--|
|`-dir` <folder_name> | Specifies the project's working directory. Defaults to `.`|
|`-d`, `--debug` | Sets the logging level to debug.|
|`-v`, `--verbose` | Enables verbose console output.|
|`-n`, `--image_name` | The requested image name (e.g. the project name). Defaults to the last folder in the path of dir |
|`-t`, `--tag` | the requested tag name for the image. Defaults to `latest`|

### example

    $ citros docker-build
    Building Docker image...
    => building with "default" instance using docker driver
    => ...
    Done.

## docker-build-push
The `docker-build-push` command is used to construct a Docker image of your ROS project and upload it to Docker Hub. This image encapsulates your project's environment, facilitating the portability and reproducibility of your simulations across different systems. 

Two tagged images will be built and pushed: `latest` and the ROS project's latest commit hash, so that it is archived in the docker registry.

### prerequisites
If you are working inside a dev-container, make sure that the `docker-in-docker` feature is enabled in your project's `devcontainer.json`, i.e.:

    "features": {
		"ghcr.io/devcontainers/features/docker-in-docker:2": {
			"version": "latest",
			"moby": true
		}
	}

### parameters:
parameter|description
|--|--|
|`-dir` <folder_name> | Specifies the project's working directory. Defaults to `.`|
|`-d`, `--debug` | Sets the logging level to debug.|
|`-v`, `--verbose` | Enables verbose console output.|
|`-n`, `--image_name` | The requested image name (e.g. the project name). Defaults to the last folder in the path of dir |

### example
    $ citros docker-build-push
    Building Docker image...
    => building with "default" instance using docker driver
    => ...
    Done.
    Pushing Docker image...
    The push refers to repository [us-central1-docker.pkg.dev/citros/lulav/cannon]
    ea97705925b1: Pushed 
    0d42db2cff87: Preparing 
    3752398ae296: Layer already exists 
    ...
    latest: digest: sha256:b5d109f83c1dbbaf97d918e721889988210d9bc1a91f3ecde884fbc394bcca1c size: 5136
    The push refers to repository [us-central1-docker.pkg.dev/citros/lulav/cannon]
    ea97705925b1: Layer already exists 
    5deba67bdae6: Layer already exists 
    ... 
    7f858865b89b41f493d1197c3329c0214996a625: digest: sha256:b5d109f83c1dbbaf97d918e721889988210d9bc1a91f3ecde884fbc394bcca1c size: 5136
    Done.

---

# Citros Repository file Structure

The following folder and file structure is automatically generated for you (when you run `citros init`):

- .citros
  - notebooks
  - parameter_setups
    - functions
      - `my_func.py`
    - `default_param_setup.json`
  - reports
  - runs *(see below)*
  - simulations
    - `simulation_foo.json`
    - `simulation_bar.json`
  - workflows
    - `default_flow.json`
  - `citros_repo_id`
  - `project.json`
  - `settings.json`
  - `user_commit`

The `runs` directory will be populated with further files and folder every time you run a simulation (via `citros run`):

- runs
  - simulation name
    - batch name
      - run id
        - bag
          - `bag_0.db3`
          - `metadata.yaml`
        - config
          - `pkg1.yaml`
          - `pkg2.yaml`
        - msgs
          - `pkg1`
            - `msg`
              - `foo.msg`
          - `pkg2`
            - `msg`
              - `bar.msg`
        - `citros.log`
        - `environment.json`
        - `info.json`
        - `metrics.csv`
        - `otlp_trace`
        - `ros.log`
      - `info.json`

## notebooks

TODO

## parameter setups

The `parameter_setups` directory stores your JSON-formatted parameter setup files. When you initialize your citros repository, a `default_param_setup.json` file is automatically generated. This file consolidates all the default parameters for every node across all the packages in your ROS project, providing a consolidated and easily accessible record of these parameters.

The file `default_param_setup.json` will not be overwritten during citros `init`, `run` or `status` commands. Nevertheless, it is recommended to duplicate this file under a different name within the `parameter_setups` directory before making any modifications. This practice ensures your custom setups are preserved and allows you to experiment with various parameter configurations.

The structured format of the parameter setup files streamlines both the understanding and alteration of parameters for each node in your ROS project. This becomes especially valuable when you're keen to explore the influence of different parameter values on your ROS project's behavior. Take, for instance, a static parameter value like 42. Instead of hard-coding it, you could use a *function object* to derive a value from a normal distribution centered at 42. The introduction of function objects broadens your horizons, enabling you to use any numpy function or even craft user-defined functions for meticulous computational adjustments. A prime example is when parameter values are intricate, making them cumbersome to hard-code; in such scenarios, you can devise a function to fetch them from a file. In essence, this newfound flexibility paves the way for limitless computational and manipulative possibilities for your parameters.

To learn how to add functions to parameter setups, please refer to the [Adding functions to parameter setup](#Adding-functions-to-parameter-setup) section below.

## reports

TODO

## runs

The runs directory stores data and metadata about each run of your simulations. Its structure is as follows:

- Simulation Name: These directories are named after each of the simulations defined in the simulation files. For every simulation file that is run, a corresponding directory is created here. Each Simulation Name directory may include multiple Batch Name directories.
    - Batch Name: This directory holds a batch of simulation runs. A batch consists of multiple runs of the same simulation with different parameters.
        - Run ID: Each unique simulation run has its own directory, identified by a Run ID. Under this directory, there are several files and sub-directories:
            - `bag`: This sub-directory holds the recorded data from the simulation run. It includes:
                - bag_0.db3: This is a ROS bag file that contains all the messages that were sent during the simulation. The default bag format is `sqlite3` (hence the db3 postfix), but you may also use the `mcap` format. See [simulations](#simulations).
                - metadata.yaml: A file holding metadata information associated with the bag file.
            - `config`: This sub-directory contains YAML files (pkg1.yaml, pkg2.yaml, etc.) for each package in your ROS project, detailing the actual parameters used in the simulation. If you used any functions in your parameter setup, the values appearing here will be those that were evaluated according to the function you defined.
            - `msgs`: This sub-directory contains all the ROS msg files you may have in your project, each under yet another sub-directory with a name corresponding to the package the msg file belongs to.
            - `citros.log`: A standard log file that was active during the simulation run, documenting actions and events throughout the simulation.
            - `environment.json`: A file capturing a snapshot of your environment variables and Python packages at the time of the simulation run.
            - `info.json`: A JSON file containing general metadata about the run, such as batch ID, batch name, datetime of the run, user's Git commit and branch information, and Citros' Git commit and branch information, as well as a hash of the bag file.
            - `metrics.csv`: A CSV file recording system performance metrics during the simulation run, including CPU usage, total memory, available memory, used memory, and memory usage percentage.

These files collectively provide a comprehensive record of each simulation run, the conditions under which it was run, and the results it produced. This makes it easy to reproduce and understand the results of each simulation.


## simulations

The `simulations` directory stores your JSON-formatted simulation files.

A simulation json file is an auto-generated file corresponding to each launch file in your ROS project. For instance, a launch file named `foo.launch.py` will have a corresponding `simulation_foo.json` file. This file outlines the details necessary to run the corresponding simulation, specifying parameters, resources, and launch files.

Here's a breakdown of its typical structure and content:

- `description`: This is a descriptive field for the simulation setup. You can modify it to better describe your specific simulation.
- `parameter_setup`: This field points to the parameter setup JSON file that will be used for this simulation. By default, it points to `default_param_setup.json`, but you can point it to any custom parameter setup file you created in the `parameter_setups` directory.
- `launch_file`: Specifies the ROS launch file that will be used to start the simulation. For instance, `foo.launch.py`.
- `timeout`: This is the maximum time (in seconds) the simulation is allowed to run. The default is 60 seconds. If the simulation does not conclude within this timeframe, it will be terminated.
- `GPU`: Specifies the number of GPU resources required for the simulation. The default is 0, indicating that no GPU resources are needed.
- `CPU`: Specifies the number of CPU resources required for the simulation. The default is 2.
- `MEM`: Specifies the amount of memory required for the simulation in megabytes, e.g., 265.
- `storage_type`: This setting determines the storage format for the ROS bag files generated during the simulation's runs. The possible valid value are `SQLITE3` (default) and `MCAP`.

You can modify these fields to suit your simulation needs, just remember to save your customized version under a different name to prevent overwriting during citros `init`, `run`, or `status` commands.

## workflows

The `workflows` directory stores your JSON-formatted workflow files.

A flow.json file (e.g., `default_flow.json` which is auto-generated during `citros init`) is a user-crafted file used to automate and manage the flow of simulations in a citros repository. This file controls when the flow is triggered, which simulations are run, the post-processing analysis using Jupyter notebooks, and the recipients of the final reports. Here is a breakdown of its structure and content:

- `trigger`: This field specifies the event that initiates the flow. It is usually tied to some form of version control event, like a Git push, but can be configured according to the user's needs.
- `simulations`: This is an array of simulations to be run, specified as pairs of simulation name and the number of times to run them. For example, ["sim1", 17] means the simulation "sim1" will be run 17 times. Multiple simulations can be listed and each will be run the specified number of times.
- `notebooks`: This is a list of Jupyter notebooks used for post-processing analysis of the simulation results. For example, ["nb1.ipynb", "nb2.ipynb"] means these two notebooks will be run once the simulations complete, with the results used as their input data.
- `recipients`: This is a list of email addresses that will receive the reports generated from the notebooks' analysis.

The flow.json file helps to streamline and automate your citros repository by tying together simulation runs, data analysis, and report distribution into a single manageable file. You can customize it to suit the specifics of your project.

## project.json

The project.json file is a key component of your Citros repository. It contains metadata about your ROS project, and is automatically generated by the citros `init`, `run` and `status` commands. Here's a description of its top-level fields:

- `citros_cli_version`: the Citros CLI version installed.
- `cover`: A placeholder for a potential image that represents the project.
- `description`: A string for providing a detailed description of the project.
- `git`: The git repository URL associated with the project.
- `image`: A name that corresponds to the docker image of the project.
- `is_active`: A boolean flag indicating whether the project is active or not.
- `launches`: An array for storing metadata about launch files associated with the project. 
**Note**: these are the global launch files, which are not associated with any specific package. Generally, they are less commonly used. For package launch files, see inside the list of *packages*.
- `license`: A string indicating the license of the project.
- `name`: The name of the project. *Note*: this is the only field that you may edit and it will not be overwritten during subsequent citros commands.
- `packages`: An array of objects that describe the ROS packages that exist within the project.
- `path`: The directory path to the project.
- `readme`: The contents of the project's README file.
- `tags`: An array of strings for tagging and categorizing the project.

In the `packages` array, each object describes a specific package within the project. These objects contain similar information to the top-level fields, with additional fields:

- `maintainer`: The maintainer of the package.
- `maintainer_email`: The email address of the maintainer.
- `nodes`: An array of objects describing each node in the package, including their parameters and entry points.
- `package_xml`: The path to the package's XML file.
- `setup_py`: The path to the package's `setup.py` file. For python ROS projects only.
- `cmake`: The path to the package's `CMakeLists.txt` file. For C++ ROS projects only.
- `parameters`: An array of objects that describe the package-level parameters, i.e. parameters which are not associated with any node. As with node-level parameters, this includes their name, type, and value.

The `nodes` array contains objects that describe the ROS nodes within a package. Each object includes the following fields:

- `entry_point`: The entry point for the node, typically the function that should be executed when the node is run.
- `name`: The name of the node.
- `parameters`: An array of objects that describe the parameters associated with the node, including their name, type, and value.
- `path`: The path to the node's Python file.

## settings.json

The settings.json file holds configuration settings for your Citros repository. Here is a breakdown of each field in this file:

- `name`: The name of the current settings profile. This can be useful if you want to maintain different sets of settings for different contexts (e.g., 'default_settings', 'debug_settings', etc.).
- `force_message`: This is a boolean setting (in string format). If set to "True", it enforces that a descriptive message is provided for each batch of simulation runs. This can be helpful for keeping track of the purpose or characteristics of each run batch.
- `force_batch_name`: Similar to force_message, this is a boolean setting (in string format). If set to "True", it enforces that a unique name is provided for each batch of simulation runs. This can be useful for organizing and identifying different batches of runs.

# Citros Repository Configuration

## Adding functions to parameter setup

In order to define a function in your parameter setup file, simply replace any constant parameter value with a `function object`.

Function objects provide a powerful and dynamic way to compute and set values in the parameter_setup.json file for ROS 2 nodes. This feature allows for much greater flexibility and dynamism when setting parameters.

### How to Add Function Objects

Function objects are essentially references to functions (either from numpy or user-defined) that will be executed to compute a value for a particular key.

#### Numpy Functions

To use a numpy function, simply provide its fully qualified name as the value in the dictionary. For example:

    {
        "my_param": {
            "function": "numpy.add",
            "args": [1, 2]
        }
    }

#### User-Defined Functions

For user-defined functions, you need to:

- Define your function in a separate `.py` file and place it under `.citros/parameter_setups/functions`.
- Use the file name (with the `.py` extension) followed by the function name, separated by a colon, as the value of the `function` key.

For instance, if you have a function named `my_function` in a file named `my_functions.py`, you would reference it as:

    {
        "my_param": {
            "function": "my_functions.py:my_function",
            "args": [...]
        }
    }

### Examples - numpy

#### simple arithmetic 

compute the product of two numbers:

    {
        "product_param": {
            "function": "numpy.multiply",
            "args": [4, 7]
        }
    }

#### Using Random Distribution

Generating a random number from a normal distribution with a mean of 0 and standard deviation of 1:

    {
        "random_param": {
            "function": "numpy.random.normal",
            "args": [0, 1]
        }
    }


Drawing a random value between 1 and 10:

    {
        "low": 1.0,
        "high": 10.0,
        "uniform_random_param": {
            "function": "numpy.random.uniform",
            "args": ["low", "high"]
        }
    }

### Examples - user-defined

#### Read from a CSV file

Suppose you want to load a matrix from a csv file into a parameter of type list of lists of floats. Copy the following function to a python file (let's call it `file_utils.py`) and place it in the `functions` directory:

    def load_matrix_from_csv(filename):
        import csv
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            matrix = [list(map(float, row)) for row in reader]
        return matrix

Reference it in your parameter_setup.json as:

    {
        "matrix_param": {
            "function": "file_utils.py:load_matrix_from_csv",
            "args": ["my_data.csv"]
        }
    }

#### function with citros context

Sometimes you may want to access some information that is part of the Citros context. For example, you may want to write a user-defined function that uses the run index of the simulation being run. In such a case, you could write a function with a parameter named `citros_context` (which must appear last in the parameter list):

    def func_with_context(num, citros_context):
        return num + float(citros_context['run_id'])

`citros_context` is a dictionary with key/value pairs describing the current Citros context. Currently the only key is `run_id`, but more may be added in the future. Then, you would call it from your `parameter_setup.json` file:

    "init_speed": {
        "function": "my_func.py:func_with_context",
        "args": [50.0]
    }

Notice that the argument for `citros_context` is added automatically for you - the `args` list only contains the argument for the first parameter (`num`).

### Examples - full parameter_setup.json example

Using the following parameter setup file, the `init_angle` parameter in the `analytic_dynamics` node of the `cannon_analytic` package (taken from the `cannon` project), will get a random value each time the simulation is run. Specifically, 60% of the evaluated values will be between 30 and 60 degrees (a standard deviation of 15 around 45). In addition, the parameter `init_speed` will be evaluated to 50.0 on the first run, and will be incremented by one for every subsequent run (see previous example for details):

    {
        "packages": {
            "cannon_analytic": {
                "analytic_dynamics": {
                    "ros__parameters": {
                        "init_speed": {
                            "function": "my_func.py:func_with_context",
                            "args": [50.0]
                        },
                        "init_angle": {
                            "function": "numpy.random.normal",
                            "args": [45, 15]
                        },
                        "dt": 0.01
                    }
                }
            },
            "cannon_numeric": {
                "numeric_dynamics": {
                    "ros__parameters": {
                        "init_speed": 50.0,
                        "init_angle": 30.0,
                        "dt": 0.01
                    }
                }
            },
            "scheduler": {
                "scheduler": {
                    "ros__parameters": {
                        "dt": 0.1
                    }
                }
            }
        }
    }

So, for example, if you run the following command in the `cannon` project:

    citros run -n "my_batch_name" -m "some_message" -c 10

and choose `simulation_cannon_analytic`, the simulation will be run 10 times, and each time `init_angle` and `init_speed` will be evaluated to different values. You can see for yourself the evaluated values if you open the `cannon_analytic.yaml` under `.citors/runs/simulation_cannon_analytic/my_batch_name/0/config`, after the run has finished.

### Pitfalls and Gotchas

#### User-Defined Functions

- **Import Handling** - Always perform imports inside the function. This ensures the function has all the necessary dependencies when called.
- **Return Types** - The function should return native Python types or numpy scalars. Avoid returning non-scalar numpy values.
- **Function Path** - Only the file name where the function is defined is needed (including the `.py` suffix). Avoid including directory paths.
- **Citros context** - if you're using the `citros_context` parameter in your user-defined function, make sure to add it *last* in the function's parameter list.

#### Numpy functions

- Always use the fully qualified name for numpy functions, such as numpy.random.exponential.

#### General Pitfalls

- **Multi-Level Key References** - When referencing a dictionary key from a function, if the key is not unique across the dictionary, use a multi-level key string to differentiate it, seperating dictionary levels with `'.'`. For example: 

        {
            "outer": {
                "inner_a": 5,
                "inner_b": {
                    "function": "numpy.add",
                    "args": ["inner_a", 3]
                }
            },
            "sum": {
                "inner_b" : 42,
                "function": "numpy.add",
                "args": ["outer.inner_b", 2]
            }
        }

- **Circular Dependencies** - Be wary of creating circular dependencies with key references. This will result in a runtime error.

- **Expected Return Types** - Ensure that the functions you use, be they numpy or user-defined, return the value type your ROS simulation expects. Mismatches (e.g., returning an integer when a float is expected) can cause errors in your simulation.

# User Templates

The Citros CLI provides a convenient way to automatically copy any predefined files (e.g. notebooks)
from the user's project to the Citros repo. Simply create a directory named `citros_template` under your project directory, and inside
it create any files and subdirectories that parallel the `.citros` directory structure.

For example, if you've created a notebook file named `test1.ipynb` which you'd like to always be available by default in your `.citros` notebooks for this project, simply create a `citros_template/notebooks/` directory under
the main directory of your project, and copy the file into it, i.e. 

    <your project>/citros_template/notebooks/test1.ipynb. 

From this point, when you run `citros init`
for this project, the file `test1.ipynb` will be automatically copied to the `notebooks` directory
under `.citros`.