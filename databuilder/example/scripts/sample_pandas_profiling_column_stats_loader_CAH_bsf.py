import os

import pandas as pd
import pandas_profiling
from pyhocon import ConfigFactory
from sqlalchemy import create_engine

from databuilder.extractor.pandas_profiling_column_stats_extractor import PandasProfilingColumnStatsExtractor
from databuilder.job.job import DefaultJob
from databuilder.loader.file_system_neo4j_csv_loader import FsNeo4jCSVLoader
from databuilder.publisher.neo4j_csv_publisher import Neo4jCsvPublisher
from databuilder.task.task import DefaultTask

schema_name = 'common'
#table_name = '<redacted>'
table_name = '<redacted>'

host = '<redacted>'
port = '<redacted>'
user = '<redacted>'
db = '<redacted>'
password = '<redacted>'

# Load table contents to pandas dataframe
db_uri = f'postgresql://{user}:{password}@{host}:{port}/{db}'
engine = create_engine(db_uri, echo=True, connect_args={'options': '-csearch_path={}'.format(schema_name)})

df = pd.read_sql_table(
    table_name,
    con=engine
)

# Calculate pandas-profiling report on a table
report_file = f'/tmp/amundsen/{schema_name}_{table_name}_report.json'

report = df.profile_report(sort=None)
report.to_file(report_file)

# Run PandasProfilingColumnStatsExtractor on calculated report
tmp_folder = f'/tmp/amundsen/column_stats'

node_files_folder = f'{tmp_folder}/nodes'
relationship_files_folder = f'{tmp_folder}/relationships'

neo_host = os.getenv('CREDENTIALS_NEO4J_PROXY_HOST', 'localhost')
neo_port = os.getenv('CREDENTIALS_NEO4J_PROXY_PORT', 7687)

NEO4J_ENDPOINT = f'bolt://{neo_host}:{neo_port}'

neo4j_endpoint = NEO4J_ENDPOINT

neo4j_user = 'neo4j'
neo4j_password = 'test'

dict_config = {
#    f'loader.filesystem_csv_neo4j.{FsNeo4jCSVLoader.NODE_DIR_PATH}': f'{tmp_folder}/nodes',
#    f'loader.filesystem_csv_neo4j.{FsNeo4jCSVLoader.RELATION_DIR_PATH}': f'{tmp_folder}/relationships',
    f'loader.filesystem_csv_neo4j.{FsNeo4jCSVLoader.NODE_DIR_PATH}': node_files_folder,
    f'loader.filesystem_csv_neo4j.{FsNeo4jCSVLoader.RELATION_DIR_PATH}': relationship_files_folder,
    f'loader.filesystem_csv_neo4j.{FsNeo4jCSVLoader.SHOULD_DELETE_CREATED_DIR}': True,
    'extractor.pandas_profiling.table_name': table_name,
    'extractor.pandas_profiling.schema_name': schema_name,
    'extractor.pandas_profiling.database_name': 'postgres',     #See https://www.amundsen.io/amundsen/databuilder/ to change USE_CATALOG_AS_CLUSTER_NAME behavior
    'extractor.pandas_profiling.cluster_name': 'bsf',           #See https://www.amundsen.io/amundsen/databuilder/ to change USE_CATALOG_AS_CLUSTER_NAME behavior
    'extractor.pandas_profiling.file_path': report_file,
    'publisher.neo4j.node_files_directory': node_files_folder,
    'publisher.neo4j.relation_files_directory': relationship_files_folder,
    'publisher.neo4j.neo4j_endpoint': neo4j_endpoint,
    'publisher.neo4j.neo4j_user': neo4j_user,
    'publisher.neo4j.neo4j_password': neo4j_password,
    'publisher.neo4j.neo4j_encrypted': False,
    'publisher.neo4j.job_publish_tag': 'unique_tag'

}

job_config = ConfigFactory.from_dict(dict_config)

task = DefaultTask(extractor=PandasProfilingColumnStatsExtractor(), loader=FsNeo4jCSVLoader())

#job = DefaultJob(conf=job_config,
#                 task=task)
job = DefaultJob(conf=job_config,
                 task=task,
                 publisher=Neo4jCsvPublisher())

job.launch()
