import boto3
import time

databrew = boto3.client("databrew")


def lambda_handler(event, context):
    job_type = event.get("type", None)
    if not job_type:
        raise Exception(
            "`type` cannot be empty. \
                Please chose either `job`, `ruleset` or `dataset`"
        )

    if job_type == "job":
        delete_jobs()
    elif job_type == "ruleset":
        delete_rulesets()
    elif job_type == "dataset":
        delete_datasets()
    else:
        raise Exception("Unknown Job Type please input `job`, `ruleset`, `dataset`")

    return {"statusCode": 200, "body": "DataBrew maintenance completed successfully."}


def list_datasets():
    # List all DataBrew datasets
    response = databrew.list_datasets()
    datasets = response["Datasets"]
    return datasets


def delete_datasets():
    # Assuming you have a list of dataset names to delete
    error_datasets = []
    while True:
        datasets = list_datasets()
        if datasets:
            dataset_names = [d["Name"] for d in datasets]
            for name in dataset_names:
                try:
                    databrew.delete_dataset(Name=name)
                    print(f"Deleted dataset: {name}")
                    time.sleep(0.33)  # To respect 5 TPS API limit of DataBrew
                except Exception as e:
                    error_datasets.append(name)
                    print(f"Error deleting dataset {name}: {e}")
        else:
            print("No more datasets to delete")
            break
    if error_datasets:
        print(f"Error datasets are: {error_datasets}")


def delete_jobs():
    # List and delete DataBrew jobs
    while True:
        response = databrew.list_jobs()
        jobs = response["Jobs"]
        if jobs:
            for job in jobs:
                try:
                    databrew.delete_job(Name=job["Name"])
                    print(f"Deleted job: {job['Name']}")
                    time.sleep(0.33)  # To respect 5 TPS API limit of DataBrew
                except Exception as e:
                    print(f"Error deleting job {job['Name']}: {e}")
        else:
            print("No more jobs to delete")
            break


def delete_rulesets():
    # List and delete DataBrew rulesets
    while True:
        response = databrew.list_rulesets()
        rulesets = response["Rulesets"]
        if rulesets:
            for ruleset in rulesets:
                try:
                    databrew.delete_ruleset(Name=ruleset["Name"])
                    print(f"Deleted ruleset: {ruleset['Name']}")
                    time.sleep(0.4)  # To respect 5 TPS API limit of DataBrew
                except Exception as e:
                    print(f"Error deleting ruleset {ruleset['Name']}: {e}")
        else:
            print("No more rulesets to delete")
            break
