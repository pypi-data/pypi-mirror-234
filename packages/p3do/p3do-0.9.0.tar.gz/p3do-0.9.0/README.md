<div align="center">

# p3do - let 'em minions do it

[![PyPI - License](https://img.shields.io/pypi/l/p3do)](https://github.com/poolparty-semantic-suite/p3do/blob/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/p3do)](https://pypi.org/project/p3do/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/p3do)](https://www.python.org/)
[![Publish](https://github.com/poolparty-semantic-suite/p3do/actions/workflows/publish.yml/badge.svg)](https://github.com/poolparty-semantic-suite/p3do/actions)


p3do (pronounced _pee-three-duh_) is a collection of command-line utilities for
p3d. It allows you to conjure some tedious operations right from your magic little
fingertips.

<img src="res/p3do-animation.gif?raw=true" alt="p3do in action" width="75%"/>

<p />

[Installation](#installation) •
[Getting started](#getting-started) •
[Commands](#commands) •
[Contribute](#contribute)

</div>

## Installation
<img src="res/p3do-logo.png?raw=true" alt="p3do logo" align="right" width="180px"/>

`p3do` is built with Python 3.8 or later. You can get Python from your package
manager du jour or download and install it from
https://www.python.org/downloads/ (looking at you Windows. Mac.
Whyihavetobother. Veryannoyingyouare.)

`p3do` is published to the [CheeseShop](https://pypi.org/project/p3do/) and
hence can be installed with pip:

```bash
pip install p3do
```

To upgrade `p3do` to the latest version, run:

``` bash
pip install --upgrade p3do
```

`p3do` installs itself as a command. If your `$PATH` is set up correctly you
will be able to just invoke `p3do` like so

```bash
p3do --help
```

### Shell Completion

`p3do` supports shell completion (tab completion). Shell completion is supported
for bash, zsh and fish shells. For each of these, the autocompletion script is
different.

Bash 4.4 and later:
``` bash
# add to your ~/.bashrc
eval "$(_P3DO_COMPLETE=bash_source p3do)"
```

Zsh:
``` bash
# add to your ~/.zshrc:
eval "$(_P3DO_COMPLETE=zsh_source p3do)"
```

Fish:
``` bash
#  ~/.config/fish/completions/p3do.fish
eval (env _P3DO_COMPLETE=fish_source p3do)
```

## Getting Started

<img src="res/p3do-logo2.png?raw=true" alt="p3do logo" align="left" width="180px"/>

Light a bonfire and whisper _p3do_ in the most conspirative voice available to
you. Then start a terminal.

`p3do` is hierarchical, self-documenting and discoverable. The best way to start
is to just type `p3do`. This will show you the available commands and some
description. From there you can drill down the hierarchy for useful sub-command.

Each sub-command/command group has special flags and configuration. How to use
them is explained in [Commands](#commands) for each of them separately. You can
also use `p3d <group> <command> --help` in your terminal for concise on-line
help.

## Commands

`p3do` is hierarchical. Commands are batched into groups which can be further
nested into parent groups. We follow the same principle in the documentation
here.

* [`jk`](#jk): Jenkins commands
    - [`build`](#build): Run the `P3D-BUILD` jenkins job with smart branch
      detection
    - [`deploy`](#deploy): Run the `P3D-Build-Deploy-PoolParty-(parent-pom)`
      jenkins job with smart branch detection

* [`pp`](#pp): PoolParty commands
    - [`encrypt`](#encrypt): Encrypt a clear text with poolparty encryption
    - [`decrypt`](#decrypt): Decrypt a secret text with poolparty encryption
    - [`install-snapshot`](#install-snapshot): Download and run latest snapshot installer. Linux only.
    - [`mock-server`](#mock-server): Run a mock server for debugging external
      services integration (Semantic Middleware Configurator).
    - [`encrypt-license`](#encrypt-license): Encrypt a PoolParty license
    - [`decrypt-license`](#decrypt-license): Decrypt a PoolParty license

* [`kc`](#kc): Keycloak commands
    - [KC Configuration](#kc-configuration): Not a command but read this first!
    - [`add-mappers`](#add-mappers): Add mappers to IdPs from realm export
    
* [`gh`](#gh): GitHub commands
    - [`deploy-key`](#deploy-key): Add a deployment key to a GitHub repository

* [`gs`](#gs): GraphSearch commands
    - [`create-documents`](#create-documents): Push dummy documents into a ppgs searchspace

### jk

Commands in this group allow to perform common operations on Jenkins.

#### build

Start the `P3D-BUILD` job from the command line with smart branch detection.
For this command `git` has to be installed.

Per default (and outside a git repository) builds the `develop` branch of
PoolParty.

When inside a git repository p3do will automatically detect the current
branch and build it. This behavior can be disabled with `--no-autodetect`.

The branch to build can be specified via `--branch` (note that this implies
`--no-autodetect` inside a git repository).

With `--api-user` and `--api-key` you can specify the credentials accessing the
Jenkins API. These credentials are cached and only need to be specified once. If
not specified and no cached credentials are found, p3do will ask for them
interactively. You can generate a token for `--api-key` in your [Jenkins Account
Settings](https://ci2.semantic-web.at/user/<username>/configure). `--api-user`
is the username you use to log in to Jenkins.

``` bash
# Build branch PoolParty develop without branch detection
p3do jk build --branch develop
```

#### deploy

Start the `P3D-Build-Deploy-PoolParty-(parent-pom)` job from the command line
with smart branch detection. For this command `git` has to be installed.

Per default (and outside a git repository) deploys the `develop` branch of
PoolParty.

When inside a git repository `p3do` will automatically detect the current branch
and deploy it. This behavior can be disabled with --no-autodetect.

The branch to deploy can be specified via --branch (note that this implies
--no-autodetect inside a git repository).

With `--api-user` and `--api-key` you can specify the credentials accessing the
Jenkins API. These credentials are cached and only need to be specified once. If
not specified and no cached credentials are found, p3do will ask for them
interactively. You can generate a token for `--api-key` in your [Jenkins Account
Settings](https://ci2.semantic-web.at/user/<username>/configure). `--api-user`
is the username you use to log in to Jenkins.

The `SERVER` argument is mandatory and must be a valid ssh server name.
PoolParty will be deployed to this server.

``` bash
# Deploy PoolParty develop branch to pp-lazer-kittens-dev without branch detection
p3do jk deploy --branch develop pp-lazer-kittens-dev
```

### pp

Commands in this group allow to perform operations useful for or related to
our dear PoolParty.

#### encrypt

Encrypt a clear text with PoolParty encryption. The parameters for encryption
used by PoolParty can usually be found in the `poolparty.properties` file.

This command can be used by specifying the encryption parameters directly as
options to p3do (`--password`, `--salt`, `--strength`) or with an interactive
prompt (just specify the clear text and leave out the options).

To make sure that your command line processor does not mingle the input, always
wrap the clear text, password, and salt it in quotes if you are passing them as
options to p3do.

For interactive prompt do _not_ wrap them in quotes.

Interactive prompt:
``` bash
# encrypt mysecret with 
# password H7dwBFDh3gEVDH1YecgikmOBpx9kKZ9nj1wJ5ZuhEeg=
# salt Y+Fw/4dHBajqEGxOsEyfNSGsYYXE7JUyLmc3nRFrB84=
# and 256 rounds
p3do pp encrypt "mysecret"
Password: H7dwBFDh3gEVDH1YecgikmOBpx9kKZ9nj1wJ5ZuhEeg= # interactive prompt
Salt: Y+Fw/4dHBajqEGxOsEyfNSGsYYXE7JUyLmc3nRFrB84= # interactive prompt
Strength: 256 # interactive prompt
eYRLg0SUzGNSlfmS6MYrt8pnu5MTYU3EWVmNp1q/JFQ=
```

With options:
``` bash
# encrypt mysecret with 
# password H7dwBFDh3gEVDH1YecgikmOBpx9kKZ9nj1wJ5ZuhEeg=
# salt Y+Fw/4dHBajqEGxOsEyfNSGsYYXE7JUyLmc3nRFrB84=
# and 256 rounds
p3do pp encrypt --password "H7dwBFDh3gEVDH1YecgikmOBpx9kKZ9nj1wJ5ZuhEeg=" --salt "Y+Fw/4dHBajqEGxOsEyfNSGsYYXE7JUyLmc3nRFrB84=" --strength 256 "mysecret"
```

#### decrypt
Decrypt a secret text encrypted by PoolParty. The parameters for encryption/decryption used
by PoolParty can usually be found in the `poolparty.properties` file.

This command can be used by specifying the encryption parameters directly as
options to p3do (`--password`, `--salt`, `--strength`) or with an interactive
prompt (just specify the clear text and leave out the options).

To make sure that your command line processor does not mingle the input, always
wrap the clear text, password, and salt it in quotes if you are passing them as
options to p3do.

For interactive prompt do _not_ wrap them in quotes.

Interactive prompt:
``` bash
# decrypt 6NjzLmQp7kGM7bbezhQX1G2hrqCoqLrC32ayBTjQVjU= with 
# password H7dwBFDh3gEVDH1YecgikmOBpx9kKZ9nj1wJ5ZuhEeg=
# salt Y+Fw/4dHBajqEGxOsEyfNSGsYYXE7JUyLmc3nRFrB84=
# and 256 rounds
p3do pp decrypt "6NjzLmQp7kGM7bbezhQX1G2hrqCoqLrC32ayBTjQVjU="
Password: H7dwBFDh3gEVDH1YecgikmOBpx9kKZ9nj1wJ5ZuhEeg= # interactive prompt
Salt: Y+Fw/4dHBajqEGxOsEyfNSGsYYXE7JUyLmc3nRFrB84= # interactive prompt
Strength: 256 # interactive prompt
eYRLg0SUzGNSlfmS6MYrt8pnu5MTYU3EWVmNp1q/JFQ=
```

With options:
``` bash
# decrypt 6NjzLmQp7kGM7bbezhQX1G2hrqCoqLrC32ayBTjQVjU= with 
# password H7dwBFDh3gEVDH1YecgikmOBpx9kKZ9nj1wJ5ZuhEeg=
# salt Y+Fw/4dHBajqEGxOsEyfNSGsYYXE7JUyLmc3nRFrB84=
# and 256 rounds
p3do pp decrypt --password "H7dwBFDh3gEVDH1YecgikmOBpx9kKZ9nj1wJ5ZuhEeg=" --salt "Y+Fw/4dHBajqEGxOsEyfNSGsYYXE7JUyLmc3nRFrB84=" --strength 256 "6NjzLmQp7kGM7bbezhQX1G2hrqCoqLrC32ayBTjQVjU=" 
```

#### install-snapshot

Download and invoke the latest snapshot installer. Specify `--path` to download
the installer to a specific folder. Otherwise, the installer will be installed
to a temporary directory. 

This command is restricted to Linux for now.

``` bash
p3do pp install-snapshot
```

#### mock-server

Runs a mock server for testing and debugging external integrations

PoolParty provides several integrations with external APIs/services (cf.
Semantic Middleware Configurator). This command starts a mock server for
debugging/testing such integrations.

The port on which to run the server can be specified via --port. It defaults
to 5000.

##### Webhook consumer
Starts a server and echoes any request (+ auxiliary information) coming in.
In addition starts a healthcheck endpoint that just always returns `200 OK`.

The webhook consumer url (to configure in Semantic Middleware Configurator)
is `http://localhost:5000/hook`.

``` bash
p3do pp mock-server
```


#### encrypt-license
Encrypts PoolParty license data with the PoolParty standard encryption and the
given encryption key

KEY must be the base64 encoded encryption key for PoolParty licenses
LICENSE path to the license data that shall be encrypted as PoolParty license file

#### decrypt-license
Decrypts a PoolParty license with the PoolParty standard decryption and the given encryption key

KEY must be the base64 encoded encryption key for PoolParty licenses
LICENSE is the path to an encrypted license file usually ending in .key

### kc

Commands in this group allow to perform operations for Keycloak. Most of them
need authentication and server information. Please read [KC
Configuration](#kc-configuration) first on how to add your configuration.

Commands:
* [KC Configuration](#kc-configuration): Not a command but read this first!
* [`add-mappers`](#add-mappers): Add mappers to IdPs from realm export

#### KC Configuration

kc commands usually need some information about the server, realm and
authentication. This information can be read from a configuration file, given
via CLI parameters or interactively if information is missing. CLI parameters
take precendence and override any configuration read from a configuration file.

***Note:*** you don't need a configuration file at all. All (partial) parameters
can be specified via CLI arguments. Just leave out the `--auth_config` and
`--auth` flags.

A full configuration file which specifies all available options looks like this:

```ini
[test]
server=https://keycloak.example.com/auth/
username=admin
user_realm_name=master
password=password
realm_name=my-app
```

`[test]` is the name of the configuration. You can have multiple configurations
for different servers in your config file. `server`, `username`, `password` are
rather self-explanatory. `user_realm_name` is the realm the _user_ is in. This
is not necessarily the same realm as the one you want to modify. `realm_name` is
the realm name you want to modify (it usually does not make sense to put this
into the config file).

To specify the config file and config name you want to use, invoke a `p3do` command like this:

```bash
# `config.ini` is the config file, `test` is the config section you want to use
p3do kc add-mappers --auth_config config.ini --auth test <...other arguments...>
```

Note that you can override any configuration via CLI arguments:

```bash
# Override `admin` from `config.ini` with `admin2`
p3do kc add-mappers --auth_config config.ini --auth test --username admin2 <...other arguments...>
```

The configuration can also be partial:
```ini
[partial-test]
server=https://keycloak.example.com/auth/
username=admin
user_realm_name=master
```

Note that we don't specify a `password` or `realm_name` here. You can now invoke `p3do` with

```bash
# Complete `partial-test` via arguments
p3do kc add-mappers --auth_config config.ini --auth partial-test --password password --realm_name my-other-app <...other arguments...>
```

You can also just invoke `p3do` as before and will be asked interactively to fill out the missing pieces:

```bash
# No `password` or `realm_name` from `config.ini` or cli arguments
p3do kc add-mappers --auth_config config.ini --auth partial-test <...other arguments...>
# `p3do` will ask you to complete them interactively
Password: password
Realm_name: my-other-app
```

#### add-mappers

Add IdP mappers from a realm export `.json` to a realm. The IdP must already
exist and correspond to the IdP name specified in the mapper config. Keycloak
does not import mapper configuration by itself (yet?).

```bash
# `realm-export.json` is the path the the export file
p3do kc add-mappers --auth_config config.ini --auth test realm-export.json
```

### gh

Commands in this group allow to perform operations on GitHub
`poolparty-semantic-suite` organization. Most operations need an access token.
This can be generated in GitHub user settings
https://github.com/settings/tokens.

Commands:
* [`deploy-key`](#deploy-key): Add a deployment key to a GitHub repository

#### deploy-key

Add a deployment key to a GitHub repository.

### gs

Commands in this group allow to perform operations useful for or related to
GraphSearch.

Commands:
* [`create-documents`](#create-documents): Push dummy documents into a ppgs searchspace

#### create-documents

Create a certain number of documents into an existing ppgs searchspace. `p3do` prompts the user for required arguments.

Interactive prompt:
``` bash
p3do gs create-documents
Amount [5]: 
Url [http://localhost:8081]: 
Searchspace id: 57e726ed-f2b1-44af-977e-dd156e50c6c5
Username [superadmin]: 
Password: 
```


## Contribute

***`p3do` is licensed under MIT and published to PyPI (including source). Do not
add sensitive company data. Any sensitive data has to be read from external
configuration files.***

### Contributors

All contributions are welcome. This can be new commands, improvements to the
on-line help, documentation or spelling mistakes. Just open a PR with your
changes. If your changes are larger, you find a bug but don't know how to fix
it, or you are just unsure if your idea fits, open an issue on GitHub first.

### Maintainers

The `p3do` main branch is protected and PRs have to be approved by by
[maintainers](CODEOWNERS) (code owners in GitHub lingo). Tooling like this can
easily grow out of control. Maintainers ensure that this is not happening to
`p3do`. Here are some guidelines.

- Every command in `p3do` must have a well known and feasible (manual)
  alternative
- `p3do` must not smear over too complicated process. If a process is too
  complicated fix the process.
- `p3do` must not obfuscate processes. If knowledge about how things work isn't
  spread enough, spread it.
- `p3do` must not gatekeep processes. It is not a mechanism for access
  management.
- `p3do` believes in the competency of its users

### Release Maintainers

Releases are pushed to [PyPI](https://pypi.org/project/p3do/). This requires
a token with Maintainer or Owner status on PyPI.

Releases are automatically created and pushed by a [GitHub
Action](https://github.com/swc-friedla/p3do/actions/workflows/publish.yml) when
a tagged release is created in GitHub.

Repository and release maintainers is probably but not necessarily the same set
of people.
