DROP TABLE IF EXISTS default.queries_from_hs2_logs;

CREATE EXTERNAL TABLE default.queries_from_hs2_logs (
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
