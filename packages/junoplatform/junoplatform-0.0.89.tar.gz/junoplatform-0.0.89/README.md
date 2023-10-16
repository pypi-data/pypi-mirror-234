# Juno Platform

## Description

This is a library providing AI algo runtime and package management cli

## Quick Start

### install

```bash
pip install junoplatform
```

#### junocli 
##### login first before every other subcommands
```bash
junocli login <-u your_op_user> <-p your_op_password> <api>
```

##### create a project
```bash
junocli create <my_algo_project> <PLANT> <MODULE>
```

##### test run
```bash
junocli run
```

##### package

```
junocli package <plant_name> <ALGO_MODULE_NAME>
```

#### upload, deploy, list & status