# -*- coding: utf-8 -*-
"""
LinearRegression with Apache SparkML

Created on Thu Nov 28 15:28:55 2019

@author: Qiao Yu
"""
import ibmos2spark

# @hidden_cell
credentials = {
    'endpoint': 'https://s3-api.us-geo.objectstorage.service.networklayer.com',
    'api_key': 'iTfSE_YVE6zqnxjd1oK0E37R2aVYY4dFhXFFCljE1AcJ',
    'service_id': 'iam-ServiceId-d4b06e46-293a-4417-b76c-2f16076a9353',
    'iam_service_endpoint': 'https://iam.ng.bluemix.net/oidc/token'}

configuration_name = 'os_b0f1407510994fd1b793b85137baafb8_configs'
cos = ibmos2spark.CloudObjectStorage(sc, credentials, configuration_name, 'bluemix_cos')

from pyspark.sql import SparkSession
spark = SparkSession.builder.getOrCreate()
# Since JSON data can be semi-structured and contain additional metadata, it is possible that you might face issues with the DataFrame layout.
# Please read the documentation of 'SparkSession.read()' to learn more about the possibilities to adjust the data loading.
# PySpark documentation: http://spark.apache.org/docs/2.0.2/api/python/pyspark.sql.html#pyspark.sql.DataFrameReader.json


df = spark.read.parquet(cos.url('hmp.parquet', 'courseraml-donotdelete-pr-qve0ttzezdeodc'))

df.createOrReplaceTempView('df')
df_energy = spark.sql("""
                      select sqrt(sum(x*x)+sum(y*y)+sum(z*z)) as label, class
                      from df group by class
""")
df_energy.createOrReplaceTempView('df_energy')
df_join = spark.sql('select * from df inner join df_energy on df.class = df_energy.class')
df_join.show()

from pyspark.ml.feature import VectorAssembler
from pyspark.ml.feature import Normalizer

vectorAssembler = VectorAssembler(inputCols = ["x", "y", "z"],
                                  outputCol="features")
normalizer = Normalizer(inputCol = "features", outputCol="features")

from pyspark.ml.regression import LinearRegression
lr = LinearRegression(maxIter = 10, regParam = 0.3, elasticNetParam=0.8)

from pyspark.ml import Pipeline
pipeline = Pipeline(stages=[vectorAssembler, normalizer, lr])

model = pipeline.fit(df_join)

prediction = model.transform(df_join)

prediction.show()

model.stages[2].summary.r2

"""
Linear Regression using Apache SystemML
"""
%matplotlib inline
diabetes = datasets.load_diabetes()
diabetes_x = diabetes.data[:, np.newaxis, 2]
diabetes_x_train = diabetes_x[:-20]
diabetes_x_test = diabetes_x[-20:]
diabetes_y_train = np.matrix(diabetes.target[:-20]).T
diabetes_y_test = np.matrix(diabetes.target[:-20]).T

plt.scatter(diabetes_x_train, diabetes_y_train, color='black')
plt.scatter(diabetes_x_test, diabetes_y_test, color='red')

diabetes_y_train

# Linear Regression
script = """
# add constant feature to x to model interpret
ones = matrix(1, rows = nrow(x), cols = 1)
x = cbind(x, ones)
A = t(x) %*% x
b = t(x) %*% y
w = solve(A, b)
bias = as.scalar(w[nrow(w), 1])
w = w[1:nrow(w)-1,]
"""
prog = dml(script).input(x = diabetes_x_train, y = diabetes_y_train).output('w', 'bias')
w, bias = ml.execute(prog).get('w', 'bias')
w = w.toNumPy()

plt.scatter(diabetes_x_train, diabetes_y_train. color = 'black')
plt.scatter(diabetes_x_test, diabetes_y_test, color='red')

plt.scatter(diabetes_x_test, (w*diabetes_x_test)+bias, color='blue', linestyle='dotted')

'''
Splitting, Training, Validation, Over and Underfitting
'''






















