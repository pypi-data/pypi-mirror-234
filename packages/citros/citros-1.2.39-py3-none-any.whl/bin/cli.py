from bin.cli_impl import *

from pathlib import Path
import argparse


def main():
    parser = argparse.ArgumentParser(
        prog='CITROS CLI',
        description=f'''
==============================================
 ██████╗██╗████████╗██████╗  ██████╗ ███████╗
██╔════╝██║╚══██╔══╝██╔══██╗██╔═══██╗██╔════╝
██║     ██║   ██║   ██████╔╝██║   ██║███████╗
██║     ██║   ██║   ██╔══██╗██║   ██║╚════██║
╚██████╗██║   ██║   ██║  ██║╚██████╔╝███████║
 ╚═════╝╚═╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚══════╝
==============================================
CITROS CLI tool for interaction with the CITROS system. V[{citros_version}]
        ''',
        epilog='''
-----------------------------------------  
\t Powered by Lulav Space

        ''',
        formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-V', "--version",
                        action="version",
                        version=citros_version)
    
    subparsers = parser.add_subparsers(title="commands", help="citros commands", 
                                       dest='command', required=True)

    current_folder_name = str(Path.cwd().name)

    # -----------------------------------------
    build_parser = subparsers.add_parser("init", help="init citros project")
    build_parser.add_argument("-dir", default=".", help="The working dir of the project")
    build_parser.add_argument("-d", "--debug", action='store_true', help="set logging level to debug")
    build_parser.add_argument("-v", "--verbose", action='store_true', help="use verbose console prints")
    build_parser.add_argument("-project_name", default=current_folder_name, help="The project name for the project being initialized.")
    build_parser.set_defaults(func=init_citros)

    # -----------------------------------------
    build_parser = subparsers.add_parser("setup-ssh", help="setup ssh keys for secure communication with the remote citros repo.")
    build_parser.add_argument("-d", "--debug", action='store_true', help="set logging level to debug")
    build_parser.add_argument("-v", "--verbose", action='store_true', help="use verbose console prints")
    build_parser.set_defaults(func=setup_ssh)

    # -----------------------------------------
    build_parser = subparsers.add_parser("status", help="get the citros repo status.")
    build_parser.add_argument("-dir", default=".", help="The working dir of the project")
    build_parser.add_argument("-d", "--debug", action='store_true', help="set logging level to debug")
    build_parser.add_argument("-v", "--verbose", action='store_true', help="use verbose console prints")
    build_parser.set_defaults(func=status)

    # -----------------------------------------
    build_parser = subparsers.add_parser("add-remote", help="add remote citros repo to existing local repo.")
    build_parser.add_argument("-dir", default=".", help="The working dir of the project")
    build_parser.add_argument("-d", "--debug", action='store_true', help="set logging level to debug")
    build_parser.add_argument("-v", "--verbose", action='store_true', help="use verbose console prints")
    build_parser.set_defaults(func=add_remote)

    #------------------------------------------
    build_parser = subparsers.add_parser("commit", help="commit changes to local citros repo.")
    build_parser.add_argument("-dir", default=".", help="The working dir of the project")
    build_parser.add_argument("-d", "--debug", action='store_true', help="set logging level to debug")
    build_parser.add_argument("-v", "--verbose", action='store_true', help="use verbose console prints")
    build_parser.add_argument("-m", "--message", default="", help="commit message.")
    build_parser.set_defaults(func=commit)

    #------------------------------------------
    build_parser = subparsers.add_parser("push", help="push commits to remote citros repo.")
    build_parser.add_argument("-dir", default=".", help="The working dir of the project")
    build_parser.add_argument("-d", "--debug", action='store_true', help="set logging level to debug")
    build_parser.add_argument("-v", "--verbose", action='store_true', help="use verbose console prints")
    build_parser.set_defaults(func=push)

    #------------------------------------------
    build_parser = subparsers.add_parser("pull", help="pull changes from remote citros repo.")
    build_parser.add_argument("-dir", default=".", help="The working dir of the project")
    build_parser.add_argument("-d", "--debug", action='store_true', help="set logging level to debug")
    build_parser.add_argument("-v", "--verbose", action='store_true', help="use verbose console prints")
    build_parser.set_defaults(func=pull)

    #------------------------------------------
    build_parser = subparsers.add_parser("diff", help="see the difference between the .citros working directory and the last commit.")
    build_parser.add_argument("-dir", default=".", help="The working dir of the project")
    build_parser.add_argument("-d", "--debug", action='store_true', help="set logging level to debug")
    build_parser.add_argument("-v", "--verbose", action='store_true', help="use verbose console prints")
    build_parser.set_defaults(func=diff)

    #------------------------------------------
    build_parser = subparsers.add_parser("checkout", help="check out a branch by the given name.")
    build_parser.add_argument("-dir", default=".", help="The working dir of the project")
    build_parser.add_argument("-d", "--debug", action='store_true', help="set logging level to debug")
    build_parser.add_argument("-v", "--verbose", action='store_true', help="use verbose console prints")
    build_parser.add_argument("-b", "--branch", help="branch name.")
    build_parser.set_defaults(func=checkout)

    #------------------------------------------
    build_parser = subparsers.add_parser("merge", help="merge one of the local branches into the current branch.")
    build_parser.add_argument("-dir", default=".", help="The working dir of the project")
    build_parser.add_argument("-d", "--debug", action='store_true', help="set logging level to debug")
    build_parser.add_argument("-v", "--verbose", action='store_true', help="use verbose console prints")
    build_parser.set_defaults(func=merge)

    #------------------------------------------
    build_parser = subparsers.add_parser("discard", help="discard changes in the working directory.")
    build_parser.add_argument("-dir", default=".", help="The working dir of the project")
    build_parser.add_argument("-d", "--debug", action='store_true', help="set logging level to debug")
    build_parser.add_argument("-v", "--verbose", action='store_true', help="use verbose console prints")
    build_parser.add_argument("--ALL", action="store_true", help="Discard all files.")
    build_parser.add_argument("files", nargs='*', help="List of files to discard.")
    build_parser.set_defaults(func=discard)


    #------------------------------------------
    build_parser = subparsers.add_parser("login", help="log in to citros")
    build_parser.add_argument("-d", "--debug", action='store_true', help="set logging level to debug")
    build_parser.add_argument("-v", "--verbose", action='store_true', help="use verbose console prints")
    build_parser.add_argument("-username", default=None, help="username")
    build_parser.add_argument("-password", default=None, help="password")
    build_parser.set_defaults(func=login)
    
    # -----------------------------------------
    build_parser = subparsers.add_parser("logout", help="log out of the system")
    build_parser.add_argument("-d", "--debug", action='store_true', help="set logging level to debug")
    build_parser.add_argument("-v", "--verbose", action='store_true', help="use verbose console prints")
    build_parser.set_defaults(func=logout)
    
    # -----------------------------------------
    build_parser = subparsers.add_parser("list", help="lists all simulation names.")
    build_parser.add_argument("-dir", default=".", help="The working dir of the project")
    build_parser.add_argument("-d", "--debug", action='store_true', help="set logging level to debug")
    build_parser.add_argument("-v", "--verbose", action='store_true', help="use verbose console prints")
    build_parser.set_defaults(func=list_project)
        
    # -----------------------------------------
    build_parser = subparsers.add_parser("run", help="run a simulation")
    build_parser.add_argument("-dir", default=".", help="The working dir of the project")
    build_parser.add_argument("-d", "--debug", action='store_true', help="set logging level to debug")
    build_parser.add_argument("-v", "--verbose", action='store_true', help="use verbose console prints")
    build_parser.add_argument("-s", "--simulation_name", nargs='?', default=None, help="Simulation name")
    build_parser.add_argument("-b", "--batch_id", nargs='?', default=None, help="Batch id")
    build_parser.add_argument("-n", "--batch_name", nargs='?', default=None, help="Batch name")
    build_parser.add_argument("-m", "--batch_message", nargs='?', default=None, help="Batch name")
    build_parser.add_argument("-i", "--run_id", nargs='?', default='', help="run id")
    build_parser.add_argument("-c", "--completions", nargs='?', default=1, help="number of times to run the simulation")
    build_parser.add_argument("-r", "--remote", action='store_true', help="run the simulation remotely on the citros cloud")
    build_parser.add_argument("-k", "--key", nargs='?', default=None, help="authentication key")
    build_parser.add_argument("-l", "--lan_traffic", action='store_true', help="receive LAN ROS traffic in your simulation.")
    build_parser.add_argument("--branch", default=None, help="branch name. defaults to active branch. for remote run only.")
    build_parser.add_argument("--commit", default=None, help="commit hash. defaults to latest commit. for remote run only.")
    build_parser.set_defaults(func=run)
    
    # -----------------------------------------
    build_parser = subparsers.add_parser("docker-build", help="Builds the project")
    build_parser.add_argument("-dir", default=".", help="The working dir of the project")
    build_parser.add_argument("-d", "--debug", action='store_true', help="set logging level to debug")
    build_parser.add_argument("-v", "--verbose", action='store_true', help="use verbose console prints")
    build_parser.add_argument("-n", "--image_name", default=current_folder_name, help="the requested image name (e.g. the project name)")
    build_parser.add_argument("-t", "--tag", default='latest', help="tag for the image")
    build_parser.set_defaults(func=docker_build)

    # -----------------------------------------
    build_parser = subparsers.add_parser("docker-build-push", help="Builds and pushes the project")
    build_parser.add_argument("-dir", default=".", help="The working dir of the project")
    build_parser.add_argument("-d", "--debug", action='store_true', help="set logging level to debug")
    build_parser.add_argument("-v", "--verbose", action='store_true', help="use verbose console prints")
    build_parser.add_argument("-n", "--image_name", default=current_folder_name, help="the requested image name (e.g. the project name)")
    build_parser.set_defaults(func=docker_build_push)

    # -----------------------------------------
    #build_parser = subparsers.add_parser("docker", help="run an arbitrary docker command")
    #build_parser.add_argument("-d", default="Dockerfile", help="The docker to build")
    #build_parser.set_defaults(func=docker)

    args, argv = parser.parse_known_args()
    
    args.func(args, argv)
