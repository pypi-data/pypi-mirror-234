# Certificates Generation Tools

![build](https://github.com/LeConTesteur/certificates-generation-tools/actions/workflows/build.yml/badge.svg)


## Description

This tools can generate customs certificates for testing. The certificate be able not standard.

This tools use yaml or json file descriptor for define tasks to execute.

### Example

For exemple, we can generate certificate with **notAfter** previous to **notBefore** :
```yaml
---
- kind: key
  name: world
  bits: 8192
- kind: cert
  name: world
  private_keyid: world
  autosign: true
  notBefore: '1990-01-01'
  notAfter: '2000-11-30'
  subject:
    CN: world
  isCa: false
  CrlDP:
    uris:
    - http://aroundtheworld.cam
```

And the command to run: `certs-gen-tools -f example.yaml -F yaml`.

More example are present into *examples* directory.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install certificates-generation-tools
```

## Usage

```bash
certs-gen-tools --help
usage: certs-gen-tools [-h] -f FILE [-F {json,yaml}] [-d WORKDIR] [-D] [-C]

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Define the file contains actions list
  -F {json,yaml}, --format {json,yaml}
                        Define the format of files
  -d WORKDIR, --workdir WORKDIR
                        Define the workdir where files will be generating
  -D, --debug           Activate debug mode
  -C, --clean-except-keys
                        Generate all the certificates except not the keys
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Tests

Run tests with tox command :

```bash
tox
tox -e testsacc
```