import argparse
import site
import subprocess
import re


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

    args = parser.parse_args()

    if getattr(args, "sub_command") == 'service':
        if args.action == 'start':
            port = 9999
            if args.port:
                port = args.port
            print('service port: ' + str(port))
            manage_path = site.getsitepackages()[0] + '/promptmanager/manage.py'
            subprocess.run(['python', f"{manage_path}", 'runserver', f"{port}", '--settings=PromptManager.settings.dev'])
        elif args.action == 'stop':
            pid = get_pid('manage.py runserver')
            if not pid:
                print('service PID not found!')
            else:
                print('PID ' + pid + ' will be killed!')
                subprocess.run(['kill', pid])
            print('service stop done')


def get_pid(process_name):
    cmd = 'ps aux | grep \"' + process_name + '\" | grep -v grep | awk "{{print $2}}"'
    output = subprocess.check_output(cmd, shell=True)
    pid_pattern = re.compile(r'\b(\d+)\b')
    pids = pid_pattern.findall(output.decode())
    return pids[0]


if __name__ == "__main__":
    main()
