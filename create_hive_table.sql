DROP TABLE IF EXISTS default.queries_from_hs2_logs_raw;

CREATE EXTERNAL TABLE default.queries_from_hs2_logs_raw (
    hs2_instance string,
    username STRING,
    tstamp BIGINT,
    duration BIGINT,
    jobids array<STRING>,
    engine STRING,
    dbname STRING,
    read_tables array<STRING>,
    write_tables array<STRING>,
    query_text STRING
)
ROW FORMAT DELIMITED 
FIELDS TERMINATED BY '\t'
COLLECTION ITEMS TERMINATED BY '#'
STORED AS TEXTFILE
LOCATION '/hdfs/path/to/query_data/';

drop table if exists default.queries_from_hs2_logs; 
create table default.queries_from_hs2_logs stored as parquet as select * from default.queries_from_hs2_logs_raw;


drop table if exists default.hs2_grouped_data_raw;
create external table default.hs2_grouped_data_raw (
query_first_100_chars string,
hs2_instance string,
duration_min bigint,
duration_mean bigint,
duration_max bigint,
duration_total bigint,
occurences int,
hive_mr_jobs int,
engine string,
unique_read_table_count int,
unique_write_table_count int,
read_tables string,
write_tables string,
control_tables_used_flag int,
control_read_tables string,
control_write_tables string
)
ROW FORMAT DELIMITED 
FIELDS TERMINATED BY '\t'
stored as textfile
location '/hdfs/path/to/grouped_data';

drop table if exists default.hs2_grouped_data; 
create table default.hs2_grouped_data stored as parquet as select * from default.hs2_grouped_data_raw;


drop table if exists default.hs2_table_access_raw;
create external table default.hs2_table_access_raw (
read_or_write string,
table_name string,
job_duration_weighted_query_references float,
num_query_references int
)
ROW FORMAT DELIMITED 
FIELDS TERMINATED BY '\t'
stored as textfile
location '/hdfs/path/to/table_access_data';

drop table if exists default.hs2_table_access; 
create table default.hs2_table_access stored as parquet as select * from default.hs2_table_access_raw;

