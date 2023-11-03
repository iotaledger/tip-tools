# Schema CLI

This tool generates schema tables for TIPs and can automatically calculate the storage deposit (VByte Min and Max) of such schemas.

## Usage

Install python virtualenv:

```sh
pip3 install --user virtualenv
```

Create a new virtualenv and install the dependencies:

```sh
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
```

Then you can run the cli.

To generate the table for a given schema pass the schema name:

```sh
python3 cli.py schema generate "Ed25519 Address"
```

To replace a schema directly in the TIP it is defined in, pass the path to the tips repo and the schema name:

```sh
python3 cli.py schema replace ../../tips/ "Foundry Output"
```

To update all schemas defined in a given TIP, pass the path to the tips repo and the TIP number:

```sh
python3 cli.py schema update ../../tips/ 44
```

To generate the deposit table for a given schema:

```sh
python3 cli.py deposit "Basic Output"
```

The deposit command only makes sense to be called on outputs, as it automatically adds the offset for outputs.

Hint: When passing an unknown schema name, the cli lists all available schemas.
