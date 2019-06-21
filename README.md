# Project Title

A web based platform to achieve following tasks

1. Time series analysis of variation of various available indexes used to analyse vegetation, water level etc using Landsat satellite data

2. Adding your own customised indices via a GUI

3. Visualizing terrain profile along a path using various available DEMs namely ASTER and SRTM

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them

* [Open Data Cube](https://datacube-core.readthedocs.io/en/latest/) project 
* Landsat images of the region with corresponding metadata files (in .yaml format)

### Installing

1. Add conda forge channel

    ```python
    conda config --add channels conda-forge
    ```

2. Create a virtualenv in conda

    ```python
        conda create --name cubeenv python=3.6 datacube
    ```

3. Activate environment

    ```python
    source activate cubeenv
    ```

4. Install other packages

    ```python
    conda install jupyter matplotlib scipy
    ```

5.Setting up database
* Install [PostgreSQL](https://sourceforge.net/projects/postgresqlportable/) portable launcher
* Create a user 
    `create role <username> superuser login`
* Create a database 
    `create database datacube`

6. Add config file and add it's path to DATACUBE_CONFIG_PATH environment variable
    
    ```
    [datacube]
    db_database: datacube

    # A blank host will use a local socket. Specify a hostname (such as localhost) to use TCP.
    db_hostname:

    # Credentials are optional: you might have other Postgres authentication configured.
    # The default username otherwise is the current user id.
    # db_username:
    # db_password:
    ```

7. Add metadata types ( like eo, telemetry_data ) to the datacube using `datacube metadata add <path to your metadata types .yaml file>`

8. Add product definitions (It defines what type of products your datacube can hold.) using `datacube product add <path to your product definition yaml>`
    Examples of some [product definitions](https://github.com/opendatacube/datacube-core/tree/develop/docs/config_samples/dataset_types)

9.For each dataset add it's metadata file. At a minimum, you need the dimensions or fields your want to search by, such as lat, lon and time, but you can include any information you deem useful.
It is typically stored in YAML documents, but JSON is also supported. It is stored in the index for searching, querying and accessing the data.
For third party datasets https://datacube-core.readthedocs.io/en/latest/ops/prepare_scripts.html#prepare-scripts

10. Install all the requirements using 
    ```python
    pip install -r requirements.txt
    ```

11. Apply the migrations

    ```python
    python manage.py makemigrations
    python manage.py migrate
    ```
12. To run project

    ```python
    python manage.py runserver
    ```

## Authors

* **Harpinder Jot Singh** - [Github](https://github.com/HarpinderJotSingh) [LinkedIn](https://in.linkedin.com/in/harpinder-jot-singh-248b92155)
* **Kavya Gupta** - [Github](https://github.com/kavyagupta1107) [LinkedIn](https://in.linkedin.com/in/kavya-gupta-57530516b)

## Acknowledgments

* **Harish Chandra** [Profile](https://www.iirs.gov.in/Dr.Harish.C.Karnatak-profile) 
* Hat tip to anyone whose code was used
* StackOverflow :P


