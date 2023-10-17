# cdepy

cdepy is a package for interacting with ***Cludera Data Engineering Virtual Clusters***.

You can find out more about Cloudera Data Engineering in the [Cloudera Documentation](https://docs.cloudera.com/data-engineering/cloud/index.html).

## Installation

You can install this package using

```
pip install cdepy
```

### Features

- CDE Resources: create resources of type Files and Python-Environment
- CDE Jobs: create jobs of type Airflow and Spark
- Job Observability: monitor job status

### Usage

```
from cdepy import cdeconnection
from cdepy import cdejob
from cdepy import cdemanager
from cdepy import cderesource
```

#### Establish Connection to CDE Virtual Cluster

```
JOBS_API_URL = "https://<YOUR-CLUSTER>.cloudera.site/dex/api/v1"
WORKLOAD_USER = "<Your-CDP-Workload-User>"
WORKLOAD_PASSWORD = "<Your-CDP-Workload-Password>"

myCdeConnection = cdeconnection.CdeConnection(JOBS_API_URL, WORKLOAD_USER, WORKLOAD_PASSWORD)

myCdeConnection.setToken()
```

#### Create CDE Files Resource Definition

```
CDE_RESOURCE_NAME = "myFilesCdeResource"
myCdeFilesResource = cderesource.CdeFilesResource(CDE_RESOURCE_NAME)
myCdeFilesResourceDefinition = myCdeFilesResource.createResourceDefinition()
```

#### Create a CDE Spark Job Definition

```
CDE_JOB_NAME = "myCdeSparkJob"
APPLICATION_FILE_NAME = "pysparksql.py"

myCdeSparkJob = cdejob.CdeSparkJob(myCdeConnection)
myCdeSparkJobDefinition = myCdeSparkJob.createJobDefinition(CDE_JOB_NAME, CDE_RESOURCE_NAME, APPLICATION_FILE_NAME)
```

#### Create Resource and Job in CDE Cluster

```
LOCAL_FILE_PATH = "examples"
LOCAL_FILE_NAME = "pysparksql.py"

myCdeClusterManager = cdemanager.CdeClusterManager(myCdeConnection)


myCdeClusterManager.createResource(myCdeFilesResourceDefinition)
myCdeClusterManager.uploadFile(CDE_RESOURCE_NAME, LOCAL_FILE_PATH, LOCAL_FILE_NAME)

myCdeClusterManager.createJob(myCdeSparkJobDefinition)
```

#### Run and Validate CDE Job

```
myCdeClusterManager.runJob(CDE_JOB_NAME)
myCdeClusterManager.listJobRuns()
```
