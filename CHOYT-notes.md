# Notes
1. followed docker neo4j steps at:  https://www.amundsen.io/amundsen/installation/
2. updated "psycopg2-binary" and "pandas-profiling" to end requirements.txt before install requirements step
3. made copy and modified sample_postgres_loader_CAH.py to include connection info, schema and DB to import before running that sample instead of the one referenced in step #1 instructions
    $ python3 -m venv venv
    $ source venv/bin/activate
    $ pip3 install --upgrade pip
    $ pip3 install -r requirements.txt
    $ python3 setup.py install
    $ python3 example/scripts/sample_data_loader.py      <USE BELOW CUSTOM CAH EXAMPLES IN PLACE OF THIS>

# Commands
1. start docker compose
    neo4j version: docker-compose -f docker-amundsen.yml up -d
    atlas version: docker-compose -f docker-amundsen-atlas.yml up -d
    local version: docker-compose -f docker-amundsen-local.yml up -d
2. run python loaders for postgres from databuilder/ directory:  
    python3 example/scripts/sample_postgres_loader_CAH_bsf.py
    python3 example/scripts/sample_postgres_loader_CAH_edw.py
    python3 example/scripts/sample_pandas_profiling_column_stats_loader_CAH_bsf.py      --RUNS FOR 1 TABLE ONLY
3. stop docker compose w/ destroy: 
    docker-compose -f docker-amundsen.yml down --rmi 'all'
    docker-compose -f docker-amundsen-atlas.yml down --rmi 'all'
    docker-compose -f docker-amundsen-local.yml down --rmi 'all'

# References
* check running containers:  docker ps
* check container logs; usefual running detached (-d) docker-compose up
    docker-compose -f docker-amundsen.yml logs -f -t
    docker-compose -f docker-amundsen-atlas.yml logs -f -t
    docker-compose -f docker-amundsen-local.yml logs -f -t
# App Usage
Amundsen UI - http://localhost:5000/
Neo4j backend - http://localhost:7474/browser

# Troubleshooting
If es_amundsen (elasticsearch) throws "es_amundsen exited with code 137" from docker compose then OOM and increase Docker Member from 2GB to 3GB:  https://www.amundsen.io/amundsen/installation/#troubleshooting

# Demo
* basic search
* advanced search
* tags list
* add tag
* add description metadata (table + column)
* add owners
* show bookmarks
* search for new metadata (description, owners, etc.)
* search for tag (e.g. has_profile_data)
* view our tables examples - common.application_status, common.application_sub_status, origination.application
* view profile data for column statistics on our  tables
* view hive gold test_schema.test_table1 tls o show column statistics + customizations for github + airflow + badges integration
* show postgresql loaders
* show pandas profiling loaders
* show Looker loaders
* search Looker objects
* show docker-compose?
* show backend neo4j http://localhost:7474/ and elasticsearch root and http://localhost:9200/_cat/indices or ?
* show potential fargate implementation - https://aws.amazon.com/blogs/database/building-a-data-discovery-solution-with-amundsen-and-amazon-neptune/