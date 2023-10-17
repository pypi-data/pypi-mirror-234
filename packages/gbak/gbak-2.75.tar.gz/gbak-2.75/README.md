# GBackup
Deployment guide

## Git clone
```
cd /path
git clone https://github.com/vtandroid/repo_name.git folder_name
```

## Installation

### Packages
```bash
sudo apt install python3-pip python3-venv python3-dev libpq-dev
```

### Python 3.6
Python 3.6 is installed and ready to be used, verify it by typing:
```bash
python3.6 -V
```

### Turn on the Drive API
```
https://developers.google.com/drive/api/v3/quickstart/python
```
Following **Step 1: Turn on the Drive API**

Run `python manage.py download` command first time in local to get token
> If you are not already logged into your Google account, you will be prompted to log in. If you are logged into multiple Google accounts, you will be asked to select one account to use for the authorization

### Run GBackup
```bash
python3.6 -m venv source_code_dir/venv
$ cd source_code_dir
$ source venv/bin/active
$ pip install -r requirements.txt
```
1. Add `config.json` file to source_code_dir
```
NOTE: `DRIVE_SERVER` max length is 3 chars

{
  "SCOPES": [
    "https://www.googleapis.com/auth/drive"
  ],
  "CRED_FILE": "path/to/credentials.json",
  "TOKEN_FILE": "path/to/token.pickle",
  "DRIVE_SERVER": "FIL",
  "DRIVE_FOLDER_ROOT": "Auto_Backups",
  "KEY": "tungtt",
  "IS_CRYPT": "True"
}
```
2. Run
* `--config` Config path
* `--action` Action name (upload/download)
* `--input` Input value (path/file_id)
* `--output` Output dir
```
cd source_code_dir
python gbackup.py
```

# <3
TungTT
