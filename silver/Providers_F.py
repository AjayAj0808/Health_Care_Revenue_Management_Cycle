# Databricks notebook source
from pyspark.sql import SparkSession, functions as f

#Reading Hospital A departments data 
df_hosa=spark.read.parquet("/Volumes/hrcm_files/default/hosa/providers")

#Reading Hospital B departments data 
df_hosb=spark.read.parquet("/Volumes/hrcm_files/default/hosb/providers")

#union two departments dataframes
df_merged = df_hosa.unionByName(df_hosb)
display(df_merged)

df_merged.createOrReplaceTempView("providers")


# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE IF NOT EXISTS dbx_bronze_cat.hrcm_silver.providers (
# MAGIC ProviderID string,
# MAGIC FirstName string,
# MAGIC LastName string,
# MAGIC Specialization string,
# MAGIC DeptID string,
# MAGIC NPI long,
# MAGIC datasource string,
# MAGIC is_quarantined boolean
# MAGIC )
# MAGIC USING DELTA;

# COMMAND ----------

# MAGIC %sql
# MAGIC truncate table dbx_bronze_cat.hrcm_silver.providers

# COMMAND ----------

# MAGIC %sql 
# MAGIC insert into dbx_bronze_cat.hrcm_silver.providers
# MAGIC select 
# MAGIC distinct
# MAGIC ProviderID,
# MAGIC FirstName,
# MAGIC LastName,
# MAGIC Specialization,
# MAGIC DeptID,
# MAGIC try_cast(NPI as INT) NPI,
# MAGIC datasource,
# MAGIC     CASE 
# MAGIC         WHEN ProviderID IS NULL OR DeptID IS NULL THEN TRUE
# MAGIC         ELSE FALSE
# MAGIC     END AS is_quarantined
# MAGIC from providers