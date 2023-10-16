# yaml_config_day


## Pre-requisites
* For MAC/Linux systems (though should be straightforward to port to Windows).
*  Python >= 3.10 & pip

### Install from pypy distro

```bash
pip install yaml_config_day
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

* Enter your config key-value pairs
```bash
---
access_key: aaa
secret_access_key: bbbb
username: jmmmem
```

* Use in an ipython shell
```python

import yaml_config_day.config_manager as YCM
yconfig = YCM.ProjectConfigManager('jem')
yconfig.get_config()

# Out: {'access_key': 'aaa', 'secret_access_key': 'bbbb', 'username': 'jmmmem'}
```


# TODO
* tinker with the command line config creation/editing. For now, only pre-existing `yaml` file querying is tested.
* allow for more complex `config.yaml` files, as well as handling toggling beteen `prod` and various `dev` configs.... potentiall by appending an `$env` value in between `$project` and `.yaml`, ie: `~/.config/$project/$project_$env.yaml`.
