Si on veut gérer de grosses volumétries de données, on pourra utiliser des moteurs de calcul distribuer comme Apache Spark.
On passera de CSV/JSON à Parquet (colonne + compression) pour réduire I/O et coûts.
On pourra partitionner la data par date ou source (journaux ..)
Dans ce cas on aurra besoin de modifier le DAG pour introduire d'autre Tasks pour lancer les jobs sparks.
