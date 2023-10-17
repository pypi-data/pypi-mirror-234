# DAGWorks Platform SDK: Client Code &amp; Related

Welcome to using the DAGWorks Platform!

Here are instructions on how to get started with tracking, and managing your Hamilton
DAGs with the DAGWorks Platform.

## Getting Started

For the latest documentation, please consult our
[DAGWorks Platform documentation](https://docs.dagworks.io/).

For a quick overview of Hamilton, we suggest [tryhamilton.dev](https://www.tryhamilton.dev/).

## Using the DAGWorks Driver

First, you'll need to install the DAGWorks SDK package. Assuming you're using pip, you
can do this with:

```bash
# install the package & cli into your favorite python environment.
pip install dagworks-sdk

# And validate -- this should not error.
python -c "from dagworks import driver"
```

Next, you'll need to modify your Hamilton driver. You'll only need to use one line of code to
replace your driver with ours:

```python
from dagworks import driver

...
dr = driver.Driver(
    your_config,  # standard hamilton config
    *your_modules,  # standard hamilton modules
    adapter=your_adapter, # Optional. Standard hamilton adapter.
    # Note: Ray, Dask, Spark are not supported yet.
    project_id=1, # The ID of your project. Create one in the UI first if you don't have one.
    api_key="safely_load_your_api_key", # e.g. os.environ["DAGWORKS_API_KEY"]
    username="your_email_address",
    dag_name="name_of_your_dag",
    tags={"tag1": "value1", "tag2": "value2"}, # Optional
)
```
*Project ID*: You'll need a project ID. Grab one from https://app.dagworks.io/dashboard/projects.
Create a project if you don't have one, and take the ID from that.

*API Key*: You'll need an API key. Create one here https://app.dagworks.io/dashboard/settings.

*username*: This is the email address you used to sign up for the DAGWorks Platform.

*dag_name*: for a project, the DAG name is the top level way to group DAGs.
E.g. ltv_model, us_sales, etc.

*tags*: these are optional are string key value paris. They allow you to filter and curate
various DAG runs.

Then run Hamilton as normal! Each DAG run will be tracked, and you'll have access to it in the
DAGWorks Platform. Visit https://app.dagworks.io/dashboard/projects to see your projects & DAGs.

## Starter Projects
There are several starter projects that you can use to get started with the DAGWorks Platform.

Starter Projects:

* hello_world: a simple hello world DAG.
* data_processing: a simple data processing DAG, pulling from CSVs and normalizing the data.
* machine_learning: a simple machine learning DAG using the iris dataset.
* time_series_feature_engineering: a simple time series feature engineering DAG.

To use the starter project, run the dagworks CLI:

```bash
dagworks init \
      --api-key API_KEY_HERE \
      --username EMAIL_HERE \
      --project-id PROJECT_ID_FROM_DAGWORKS_PLATFORM \
      --template STARTER_PROJECT_NAME \
      --location LOCATION
```
Where:

* *API_KEY_HERE*: is your DAGWorks Platform API Key. Create one here
https://app.dagworks.io/dashboard/settings.
* *EMAIL_HERE*: is the email address you signed up for the DAGWorks Platform with.
* *PROJECT_ID_FROM_DAGWORKS_PLATFORM*: is the project ID you want to use. Create one here
https://app.dagworks.io/dashboard/projects.
* *STARTER_PROJECT_NAME*: is the name of the starter project you want to use. Your options
are hello_world, data_processing, machine_learning, time_series_feature_engineering.
* *LOCATION*: is the location you want to create the project in. This is a local directory.

# License
The use of this software is governed by the "The DAGWorks Enterprise license".
Email support@dagworks.io for more information.
