# DoUEvenLog

## Description:
DoUEvenLog was written to assist in automating running commands and collecting the logs generated from them on a Windows operating system. In particular it was written with ".evtx" format logs in mind. This script utilizes Powershell to execute commands on the endpoint. In order to use this script, it must be executed with sufficient privileges to parse whichever event logs you are wanting. Administrator, by default, will work with nearly everything. You also must have "powershell.exe" in your environment variables which is a default configuration of Windows.

## Use Cases:
This script can be used to verify the logging capabilities of a Windows endpoint i.e. does Sysmon log it when I run XYZ command or is a config change needed. It can also be used to automate log collection when using an attack framework like Red Canary's Atomic Red Team: https://redcanary.com/atomic-red-team/.
                        
## Getting Started:
 
### Dependencies:
Python: https://www.python.org/

XML conversion is dependent on williballenthin's python-evtx https://pypi.org/project/python-evtx/. 
 - Not needed to execute the rest of the script.
 - pip install python-evtx
 
 ### Arguments:
  -h, --help            show this help message and exit
  
  -o OUT_PATH, --out_path OUT_PATH
                        Path the logs will be saved. default: local temp
                        
  -p PARSE_LOG, --parse_log PARSE_LOG
                        Single name of log file i.e. Security or a comma separated list of log names of log files to be parsed.
                        
  -w WAIT_TIME, --wait_time WAIT_TIME
                        Time between running the command and parsing the logs in seconds. Default 10 seconds
                        
  -c COMMAND, --command COMMAND
                        Single command to be run.
                        
  -i INPUT_COMMANDS, --input_commands INPUT_COMMANDS
                        Input text file of commands. New line delimiter.
                        
  -x XML, --xml XML     Convert the evtx files in out_path to xml. default: False
  
  -t TERMINATE, --terminate TERMINATE
                        Terminate the subproccess and parse logs in seconds. default: 60 seconds
                        
 ### Input:
 - out_path should be a full folder path
 - parse_log should be the name or a comman separated list of names of the log(s) that wevtutil will recognize. These names can be discovered by running "wevtutil el" in either command prompt or Powershell
 - wait_time should be a whole number integer
 - command should be a string representing a command that can be executed with Powershell i.e. "net user" or "gci env:"
 - input_commands should be the full path plus file name of a text document. This text document should be in the format of one command per line.
 - xml no input
 - terminate should be a whole number integer
 
 ### Output:
 - The script will save the evtx files in "out_path" default value the local user temp directory.
 - If the -x flag is used an xml document will be saved in the same location
 - Naming schema of output is Log Name + Time of Execution
 
 ## Examples:
 - Run a single command and parse the "Windows Powershell" log
   - python .\douevenlog.py -c "echo Hello World" -p "Windows Powershell"
 - Run a single command and parse multiple logs
   - python .\douevenlog.py -c "echo Hello World" -p "Security,System,Microsoft-Windows-Sysmon/Operational"
 - Run multiple commands using a text document and parse the "Windows Powershell" log
   - python .\douevenlog.py -i C:\Temp\test_commands.txt -p "Windows Powershell"
 - Run a single command adding your own wait times and out put location
   - python .\douevenlog.py -c "echo Hello World" -p "Security,Windows Powershell" -o C:\Temp -w 15 -t 30
