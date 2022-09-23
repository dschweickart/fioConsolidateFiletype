
# fioConsolidateFiletype

Application to scan frame.io API for files of a certain type and copying them into a new directory.
This was designed for Criminal Minds Sony Venice + Transfer OCF Pull workflow.

Version: 0.1.0


## Installation

fioConsolidateFiletype

Requirements:
```bash
git
python
pip
frameioclient
```

To Clone Repo
```bash
cd /path/to/project
git clone https://github.com/Frameio/assetScan .
```

To Install
```bash
cd /path/to/project/fioConsolidateFiletype
python -m pip install frameioclient==2.0.1a3
```

To Authenticate Script
```bash
Team Member logs into frame.io (must by team member, not collaborator)
Navigate to https://developer.frame.io/app/tokens
Create API TOKEN with at least "Asset Create" and "Asset Read" permissions.
```

To Configure Default Settings
```bash
Open main.py in text editor of choice.
Edit the fields at the bottom of the file after "else" :
NOTE: These are correct values for Criminial Minds workflow.
    token =         args[0] if args[0] else {API_TOKEN}
    projectID =     args[1] if args[1] else 'aef0e6cf-2099-4400-97bf-0b210c710543'
    accountID =     args[2] if args[2] else '520272e0-158c-462c-9dea-9cc10d1e7889'
    target_folder = args[3] if args[3] else '059419e6-83aa-4e55-b707-aa0c2d276e02'
    file_ext =      args[4] if args[4] else '.mxf'
NOTE:
You can get IDs from get IDs
```

To Run:
```bash
Option #1 (Use Defaults)
python main.py

Option #2 (Pass Arguments)
python main.py {API_TOKEN} {projectID} {accountID} {target_folder} {file_ext}
```
