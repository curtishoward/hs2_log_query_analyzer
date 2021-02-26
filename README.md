Crude script to extract basic Hive query metadata from HS2 logs

1.  Extract from the HS2 logs:<br/>
```cat hadoop-cmf-hive1-HIVESERVER2-* | python parse_queries.py > query_data.tsv```
2.  Load into HDFS:<br/>
```hdfs dfs -put query_data.tsv /hdfs/path/to/query_data/```
3.  Define the Hive table:<br/>
```hive -f create_hive_table.sql```
