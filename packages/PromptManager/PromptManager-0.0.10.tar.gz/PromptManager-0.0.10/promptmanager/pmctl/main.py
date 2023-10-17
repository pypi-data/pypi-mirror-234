import argparse
import subprocess
import psutil
import operator
import platform
import os

from pathlib import Path


def main():
    parser = argparse.ArgumentParser(prog='pmctl')

    parser.add_argument(
        "-v", "--version", action="version",
        version=f"{parser.prog} version 0.0.1"
    )

    subparsers = parser.add_subparsers(dest='sub_command', help='sub-command help')

    service_parser = subparsers.add_parser('service')
    service_parser.add_argument('action', choices=['start', 'stop'], help='action to perform on the service')
    service_parser.add_argument('-port', type=int, help='specify the port number')
    service_parser.add_argument('-proxy', type=str, help='http/https proxy')

    args = parser.parse_args()

    if getattr(args, "sub_command") == 'service':
        if args.action == 'start':
            port = 9999
            if args.port:
                port = args.port
            print('service port: ' + str(port))
            if args.proxy:
                proxy = args.proxy
                print('proxy: ' + proxy)
                os.putenv('http_proxy', proxy)
                os.putenv('https_proxy', proxy)
            manage_path = str(Path(__file__).resolve().parent.parent / 'manage.py')
            print('manege_path: ' + manage_path)
            subprocess.run(['python', f"{manage_path}", 'runserver', f"{port}", '--settings=PromptManager.settings.install'])
        elif args.action == 'stop':
            pids = get_runserver_pids()
            if not pids:
                print('service PID not found!')
            else:
                for pid in pids:
                    print('PID ' + str(pid) + ' will be killed!')
                    os.kill(pid, 9)
            print('service stop done')

def get_runserver_pids():
    pids = []
    system = platform.system()
    if system == 'Windows':
        name = 'promptmanager\manage.py'
    else:
        name = 'promptmanager/manage.py'
    for process in psutil.process_iter(['pid', 'cmdline']):
        cmdline = process.info['cmdline']
        if cmdline:
            for line in cmdline:
                if operator.contains(line, name):
                    pids.append(process.pid)
    return pids


if __name__ == "__main__":
    main()
