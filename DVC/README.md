# DVC Workflow Setup

This project uses Data Version Control (DVC) to manage data and model versioning. Below are the commands used for initializing and setting up the project.

## Initialization
Initialize a new DVC repository in the current directory, enabling version control for data and models.

```bash
dvc init
```

## Directory Setup
Create the `data` directory for storing input datasets.

```
mkdir ./data
```
Create the `models` directory for storing trained models.
```
mkdir ./models
```
Create the `report` directory for storing analysis or reports related to the project.
```
mkdir ./report
```
Create the `scripts` directory for storing Python or shell scripts used in the project.
```
mkdir ./scripts
```
Create the `local_storage` directory for storing Python or shell scripts used in the project.
```
mkdir ./local_storage
```

## Setting up Remote Storage

Add a remote storage location (using local storage as remote storage) (`local_storage/`) for DVC to track and store data files.
```
dvc add remote -d local_remote ./local_storage/
```

After creating dvc.yaml, run:

```
dvc repro
```

Push Data to remote storage:

```
dvc push
```

