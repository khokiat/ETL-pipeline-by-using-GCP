# ETL-pipeline-by-using-GCP 
Beginning ETL pipeline by using google cloud platform.
## Purpose
This project would analyze statistic of covid situation in Thailand. the project would explain step of ETL process since Extracting step until visualization. All feature that were included in this process contained in google cloud platform  

## Tool
1. Google colab
2. cloud composer (Apache airflow)
3. google bigquery
4. Looker studio

![](https://github.com/khokiat/ETL-pipeline-by-using-GCP/blob/main/Picture/chart.jpg?raw=true)

### Google collab
is a product from Google Research. Colab allows anybody to write and execute arbitrary python code through the browser. we use colab to preview the code that we would generate in this project

### cloud composer
Cloud Composer is a fully managed workflow orchestration service, enabling you to create, schedule, monitor, and manage workflow pipelines that span across clouds and on-premises data centers. Cloud Composer is built on the popular Apache Airflow open source project and operates using the Python programming language.

### google bigquery
Google BigQuery is a cloud-based big data analytics web service for processing very large read-only data sets. BigQuery was designed for analyzing data on the order of billions of rows, using a SQL-like syntax (Data warehouse).

### Looker studio
is an online tool for converting data into customizable informative reports and dashboards

### Procedure
 1. Use google colab to preview the code step by step, we can check preview check our table before operating by import pandas and request library to retreive data form api and transform to dataframe to check the table
#### code
```python
import pandas as pd
import requests

url = 'https://covid19.ddc.moph.go.th/api/Cases/timeline-cases-by-provinces'
r = requests.get(url)
file = r.json()
report = pd.DataFrame(file)
report['update_date']= pd.to_datetime(report['update_date']).dt.date
report.head()
report.to_csv('Covid_report',index=True)
```

![](https://github.com/khokiat/ETL-pipeline-by-using-GCP/blob/main/Picture/02FBF003-2CB5-4255-9176-D9DC6C7705D0.jpeg?raw=true)

2. Compose cloud composer to set VM and apache airflow by setting name of composer, environment resources then create the composer. the composer would appear in the page and you would get bucket of this composer in cloud storage when running the code, the dag and data will be contained in buucket of composer.
![](https://github.com/khokiat/ETL-pipeline-by-using-GCP/blob/main/Picture/1BCF8D5A-2DED-483D-AF6F-802AD8EE54F4.jpeg?raw=true)


3. Prepare data warehouse, by create table and dataset in google bigquery this it the data warehouse that final result of pipeline will be located. we need to prepare table to specifie address of table in the code.
![](https://github.com/khokiat/ETL-pipeline-by-using-GCP/blob/main/Picture/4DE1CF96-3179-4657-AEB5-9AE3B101118A.jpeg?raw=true)

4. To prepare the DAG of pipeline, we need to prepare DAG script to control apache airflow. you can see the detail of DAG in the link --> [Pipeline definition](https://airflow.apache.org/docs/apache-airflow/stable/tutorial/fundamentals.html) 
for DAG script of this project i've attached code in DAGS folder.

5. After getting the script, copy the DAG script into dags folder of composer bucket to run the pipeline. you can check status of pipeline by reaching to UI of airflow by acessing through composer, There is a link to connect to apache airflow. 
![](https://github.com/khokiat/ETL-pipeline-by-using-GCP/blob/main/Picture/28DA3722-A5E5-4C11-9B6E-109F6C76D729.jpeg?raw=true)

6. Check the pipeline status in the page, if pipline run successfully, all task in of pipeline would be green color
![](https://github.com/khokiat/ETL-pipeline-by-using-GCP/blob/main/Picture/F5F765EF-05D5-46B1-B58A-735A3E96113F.jpeg?raw=true)
![](https://github.com/khokiat/ETL-pipeline-by-using-GCP/blob/main/Picture/9939BCD5-2C12-44AC-8FC4-64F5859D1F84.jpeg?raw=true)
7. After pipeline operating sucessfully,
final data will be save into data warehouse that we set at the 3rd step.you can select or make temp view of table by query on google bigquery. after then making data visualization by using google looker studio



8. Use Looker  studio to cennect to our table to make visualization

