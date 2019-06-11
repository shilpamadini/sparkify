# Sparkify

This folder contains the necessary program files to create Sparkify database and
corresponding etl pipeline to load the database.

## Contents

1. sql_queries.py
    * Contains all the sql queries against the database used in etl.py
2. create_tables.py
    * Drops and recreates tables.
3. etl.py
    * reads and processes files from song_data and log_data and
      loads them into the tables.
4. data/log_data
    * Contains all the file for log_data
5. data/song_data
    * Contains all the files for song_data
5. etl.ipynb
    * Jupyter notebook file used to build the etl process step by step.
6. test.ipynb
    * Jupyter notebook file with test sql to test etl process in development.
5. README.md
6. environment.yaml
    * conda environment file to import the python environment used by the project.


## Installation

### Setup PostgresSQl

You need to have a PostgreSQL database installed on your machine in
order to successfully run the programs. [Here](https://www.codementor.io/engineerapart/getting-started-with-postgresql-on-mac-osx-are8jcopb) is a document that I used to install postgresSQL on my Mac.
Once PostgreSQL is installed run below  commands.
1. Start the postgresSQL

    ```
    pg_ctl -D /usr/local/var/postgres start && brew services start postgresql
    ```

2. connect to posgres using psql
    ```
    psql postgres
    ```

3. Create a new role called "student" at the psql prompt
    ```
    CREATE ROLE student WITH LOGIN PASSWORD 'student';
    ```

4. Verify the creation of database role at the psql prompt
    ```
    \du
    ```

5. Alter the role to give permissions to create db
    ```
    ALTER ROLE student CREATEDB;
    ```

6. Create a new database called studentdb and sparkifydb
    ```
    CREATE DATABASE studentdb;
    ```
    ```
    CREATE DATABASE sparkifydb;
    ```

7. Grant privileges to student on both the databases
    ```
    GRANT ALL PRIVILEGES ON DATABASE studentdb TO student;
    ```
    ```
    GRANT ALL PRIVILEGES ON DATABASE sparkifydb TO student;
    ```

8. use the following command to connect to the database from psql
    ```
    psql -d sparkifydb -U student
    ```

9. Use the following command to see the active sessions on postgres

    ```
    select pid, usename,  datname,  client_addr, application_name, backend_start, state, state_change from pg_stat_activity;
    ```

10. Use the following command to clear any session from the backend. replace pid with the actual pid obtained in the above sql results.

    ```
    select pg_terminate_backend(pid);
    ```

### Setup  Sparkify project

1. Use the following command to clone the project repository.

    ```
    git clone https://github.com/shilpamadini/sparkify.git
    ```

2. Create the environment using below command

    ```
    conda env create -f environment.yaml
    ```

3. Activate the conda environment

    ```
    source activate dand_py3
    ```

4. Run the following commands in order to load sparkifydb
    ```
    python sql_queries.py
    ```
    ```
    python create_tables.py
    ```
    ```
    python etl.py
    ```


5. Test the etl load at any time by using test.ipynb. Run the following command to launch jupyter notebook.
    ```
    jupyter notebook
    ```


## Functionality

A startup called Sparkify wants to analyze the data they've been collecting on
songs and user activity on their new music streaming app. The analytics team is particularly interested in understanding what songs users are listening to.
This project aims to create a Postgres database with tables designed to optimize
queries on song play analysis and an ETL pipeline to load the data into tables.

The song dataset is a subset of real data from the [Million Song](http://millionsongdataset.com) Dataset. Each file is in JSON format and contains metadata about a song and the artist of that song. The second dataset consists of log files in JSON format generated by this [event simulator](https://github.com/Interana/eventsim) based on the songs in the dataset above. These simulate activity logs from a music streaming app based on specified configurations.

To analyze the song play data in its raw form requires to look at data in multiple files and mapping song data between logs files and the song data files. To make the analysis more efficient we should have the files loaded into database tables that are designed to answer the questions asked by analytics team. Since the analytics team is interested in knowing what songs the users are listening to and probably interested in performing ranking ,aggregation to determine which song is played the most, what is most popular song, which artist released most popular songs. Analytics may also be interested in looking at the trends over a period of time.

In order to support the required analytics a star schema design is implemented to design the data warehouse. Songplay table is the fact table and song, user,artist and time are dimension tables. Database integrity is maintained by using Primary key and foreign key constraints in the table definitions.

Here is the ER diagram explaining the schema design.

![Screen Shot 2019-06-10 at 5 40 47 PM](https://user-images.githubusercontent.com/16230330/59241519-d844a280-8bbc-11e9-894e-0dca550dc6ca.png)
