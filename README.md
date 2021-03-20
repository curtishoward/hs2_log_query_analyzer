Crude script to extract basic Hive query metadata from HS2 logs

1.  Extract from the HS2 logs:<br/>
```python parse_queries.py > query_data.tsv```
```hdfs dfs -put query_data.tsv /hdfs/path/to/query_data/```
2.  Group the data (e.g. by first 100 queryText character pattern):
```cat query_data.tsv | python parse_queries.py > grouped_data.tsv```
```hdfs dfs -put grouped_data.tsv /hdfs/path/to/grouped_data/```
3.  Group table accesses:
4.  ```cat query_data.tsv | python tables.py > tables.tsv```
5.  Define the Hive tables:<br/>
```hive -f create_hive_table.sql```
