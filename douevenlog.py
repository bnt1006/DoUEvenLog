"""
DoUEvenLog

Author: Brian Thacker @bnt1006

Script that was built to allow the user to automate running commands
and collecting logs from a Windows box.
"""

import subprocess
import argparse
from datetime import datetime
import time
import os

"""
Description: execute the commands supplied, wait a specified amount of time, and
parse chosen logs around the time frame (right before execution to time after wait) to the given directory

Arguments: out_path: path to save logs, parse_logs: list of windows logs to be parsed, wait_time: time to wait
after command is initiated, commands: command(s) to execute, terminate: time to wait for command to run before 
terminating the process
"""
def run_command(out_path, parse_logs, wait_time, commands, terminate):

    for command in commands:
        before_time = datetime.utcnow().isoformat()
        command = 'Invoke-Expression \"' + command.strip() + '\"'
        try:
            print("Attempting to execute: " + command)
            subprocess.Popen(["powershell.exe", command]).wait(terminate)
            time.sleep(wait_time)
        except subprocess.TimeoutExpired:
            print("Process Timed out. Attempting parse logs")
        after_time = datetime.utcnow().isoformat()
        for log in parse_logs:
            export_file = out_path + "\\" + log.replace("/","_") + before_time.split(".")[0].replace(":","_") + ".evtx"
            print("Writing logs to: " + export_file)
            parse_command = 'wevtutil epl \"' + log + "\" \"" + export_file + \
                            '\" /q:"*[System[TimeCreated[@SystemTime>=' + "\'" + before_time + "\'" + ' and @SystemTime<' + "\'" + after_time + "\'" + ']]]"'
            try:
                subprocess.Popen(["powershell.exe", parse_command]).wait(terminate)
            except subprocess.TimeoutExpired:
                print("Writing to logs timed out.")

"""
Description: convert evtx files found in the out_path directory to XML

Arguments: out_path: path to save logs
"""
def convert_xml(out_path):
    import Evtx.Evtx as evtx
    import Evtx.Views as e_views

    for file in os.listdir(out_path):
        if file[-5:] == ".evtx":
            in_file = out_path + "\\" + file
            convert_file = out_path + "\\" + file[:-5] + ".xml"
            xml_logs = open(convert_file, "w")
            with evtx.Evtx(in_file) as evtx_logs:
                xml_logs.write(e_views.XML_HEADER)
                for record in evtx_logs.records():
                    xml_logs.write(record.xml())
            xml_logs.close()

"""
Description: setup arguments, control flow of program
"""
def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('-o', '--out_path', required=False, dest='out_path',
                        help='Path the logs will be saved. default: local temp', default='%temp%')
    parser.add_argument('-p', '--parse_log', required=True, dest='parse_log',
                        help='Single name of log file i.e. Security or a comma separated list of log names of log files to be parsed.')
    parser.add_argument('-w', '--wait_time', required=False, dest='wait_time',
                        help='Time between running the command and parsing the logs in seconds. Default 10 seconds', default=10)
    parser.add_argument('-c', '--command', required=False, dest='command',
                        help='Single command to be run.')
    parser.add_argument('-i', '--input_commands', required=False, dest='input_commands',
                        help='Input text file of commands. New line delimiter.')
    parser.add_argument('-x', '--xml', required=False, dest='xml',
                        help='Convert the evtx files in out_path to xml. default: False', default=False)
    parser.add_argument('-t', '--terminate', required=False, dest='terminate',
                        help='Terminate the subproccess and parse logs in seconds. default: 60 seconds', default=60)

    args = parser.parse_args()

    if ',' in args.parse_log:
        args.parse_log = args.parse_log.split(',')
    else:
        args.parse_log = [args.parse_log]

    if args.input_commands:
        commands = []
        with open(args.input_commands) as input_file:
            commands = input_file.readlines()
    else:
        commands = [args.command]

    if args.out_path == "%temp%":
        args.out_path = os.getenv("temp")
    else:
        if not os.path.isdir(args.out_path):
            print('Provided out_path is invalid!')
            exit()

    run_command(args.out_path, args.parse_log, args.wait_time, commands, args.terminate)

    if args.xml:
        convert_xml(args.out_path)


if __name__ == "__main__":
    main()
