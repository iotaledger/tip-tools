# Schema CLI

This tool generates schema tables for TIPs and can automatically calculate the storage deposit (VByte Min and Max) of such schemas.

## Usage

Install python virtualenv:

```
pip3 install --user virtualenv
```

Create a new virtualenv and install the dependencies:

```
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
```

Then run the tool to generate the table for a given schema:

```
python3 cli.py schema "Ed25519 Address"
```

Hint: When passing an unknown schema name, the cli lists all available schemas.
