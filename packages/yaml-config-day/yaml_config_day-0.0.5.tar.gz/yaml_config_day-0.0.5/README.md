# yaml_config_day

Slim python library to manage `yaml` configuration files stored in project specific subdirectories of `~/.config/`. Command line creation and editing functions beginning to be tinkered with, core usecase presently is programatic access of standardized config.yaml files.


## Pre-requisites
* For MAC/Linux systems (though should be straightforward to port to Windows).
*  Python >= 3.10 & pip

## .config Directory Structure & yaml Files

* You must have a `~/.config` directory.  Under this directory, each `project_name` must have its own directory. Within each `project_name` directory, there must be a yaml file for each `project_environment`. In the following example, the project, `myproj`, has two `project_environment` yaml files `prod` and `develop`. The `project_environment` allows configuration of multiple working environments for each project.  The default asusmend project_environment is `prod`, but any name may be specified.

```bash
$HOME/.config/myproj/
                     ├── myproj_develop.yaml
                     └── myproj_prod.yaml
```

### Seed with example files
From the cloned yaml_config_day repo top directory.

```bash
mkdir -p ~/.config
cp -r etc/example_yaml/myproj ~/.config/myproj
```

### Install from pypy distro

```bash
pip install yaml_config_day==0.0.5
```

### Install cloned repo with pip

```bash
cd $yaml_config_day cloned repo
pip install .
```

### Development install from source

###  env for dev
* [conda/mamba](https://anaconda.org/conda-forge/mamba)

#### Create Environment

Using mamba.

```bash
mamba env create -n DYAML -f DYAML.yaml
```


#### Usage Fron Cloned Repository

```bash
conda activate DYAML
```

* Be sure to have a `project` `~/.config/` subdirectory which contains a `project.yaml` file.

```bash
project='myproj';
mkdir -p ~/.config/$project
touch ~/.config/$project/$project.yaml
```

* Enter your config key-value pairs via a text editor in the file `~/.congif/myproj/myproj_prod.yaml`.  ie:
  
```bash
---
access_key: aaa
secret_access_key: bbbb
username: myusername
```

* Use in an python shell to fetch the `~/.config/myproj/myproj.yaml` config data as a `dict`.
  
```python

import yaml_config_day.config_manager as YCM

# READ CONFIG YAML
yconfig = YCM.ProjectConfigManager('myproj', 'develop')

# RETURN DICT of YAML CONFIG
yconfig.get_config()

#  Out[3]: {'access_key': 'aaa', 'secret_access_key': 'bbbb', 'username': 'jmmmem'}

# CLEAR CONFIG
yconfig.clear_config()
yconfig.get_config()

# Out[5]: {}

# WRITE NEW YAML (will over-write all values presently, so must specify all)
yconfig.set_config(username='userNAME',access_key='AccessKey',secret_access_key='SecretAccessKey')

# GET NEW YAML AS DICT
yconfig.get_config()
Out[7]: {'access_key': 'AccessKey', 'secret_access_key': 'SecretAccessKey',  'username': 'userNAME'}

```

And after re-writing the default config.yaml, the `~/.config/myproj/myproj_develop.yaml` file now contains:
```bash
cat ~/.config/myproj/myproj_develop.yaml
```

```text
access_key: AccessKey
secret_access_key: SecretAccessKey
username: userNAME
```

# TODO
* Currently, very simple project+environment yaml files are managed.  Move to something that looks more like [myproj_test.yaml](etc/example_yaml/myproj/myproj_test.yaml).


# Notes
## Push to pypi
*  Update setup.py
* `python setup.py sdist bdist_wheel`
* `twine upload dist/*`
