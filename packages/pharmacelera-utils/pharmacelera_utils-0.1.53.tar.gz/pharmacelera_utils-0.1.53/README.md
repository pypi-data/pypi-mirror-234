# Pharmacelera util pip package to run and control an experiment
This is a simple pip package to be able to call the API from command line directly with the yaml file.
When install this package, you can run directly from the terminal:

`pharmacelera-launch config.yaml` 

It will launch the experiments that are configured inside the yaml file
(Check the config.yaml file from Mocks folder for the yaml structure).

After launch an experiment, there is a helper commands to check and controll the experiments.

`pharmacelera-cmd`

This command accepts multiple arguments as a parameter.

`--option`:  OPTION    Type of the command to call Pharmacelera endpoint. Possible options: `get`, `list`, `download`, `kill`, `remove`, `upload`. Default: `get`. Note: `list` option supports filter by status, eg: `list?status=running`.

`--id`: ID            Unique id of the experiment

`--uri` URI          Host name of the endpoint. Default: http://localhost

`--port` PORT        endpoint port number. Default: 8080

`--type` TYPE        Type of the binary to upload: [pharmqsar, pharmscreen]. default: pharmqsar

`--binary` BINARY    Path and filename of the binary file to upload

`--license` LICENSE  Path and filename of the license file to upload.

To get one experiment status: 

`pharmacelera-cmd --uri http:127.0.0.1 --port 3000 --id 507f1f77bcf86cd799439011`

## Production install

```bash

install pharmacelera-utils

```

## Local install

to be able to test the `pharmacelera-utils` package in local environment:

```bash

cd pharmaceleraModule
pip install -e .

```

This will use source code of the package from folder and install it as a library.

## Deployment
Install depoy dependencies

```bash

pip install wheel
pip install build
conda install -c anaconda twine

```

simply run `publish.sh` to deploy new version of pip package into the production. For testing purpose, run 
`publish_test.sh` to deploy it to test.pypi.

for installing it from test repo:

Linux: python3 -m pip install --index-url https://test.pypi.org/simple/ pharmacelera-utils

Windows: py -m pip install --index-url https://test.pypi.org/simple/ pharmacelera-utils
