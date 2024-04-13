# AWS Data Brew Cleaner
AWS DataBrew cleaner project for deleting DataBrew's Jobs, Rulesets, and Datasets without getting TooManyRequest error. The current limitation on AWS UI console when deleting these entries from Data Brew is that you will get `429 TooManyRequestException`, even though it's their own UI. Based on their support, they have limit of 5-6 API TPS and there are no batch deletion capabilities at the moment.

This repository contains a lambda code that has 3 different deletion capabilities with delay.
1. Deleting `DataBrew Jobs`
2. Deleting `DataBrew Rulesets`
3. Deleting `DataBrew Datasets`

Feel free to adjust delay inside the function as needed. Keep in mind that Lambda function's maximum running time is 15 minutes, if you delete thousands of entries, you might need to run the lambda multiple times.

NB: In order to delete these entries properly, due to dependencies, one need to delete with these order: `Jobs -> Rulesets -> Datasets`

## How to run it on Lambda
1. Deploy code to your lambda (I will put some more information below on manual deployment by uploading `.zip` folder)
2. Go to `Test` tab and put payload as below:
```
{
  "type": "job"
}
```
3. Click on `Test` and lambda will run and delete all entries based on the chosen `type`
There are three different types on this basic functionalities `job|ruleset|dataset`


### Manual deployment to Lambda on local Mac (Tested with Python 3.8)
1. Pull code to your local e.g. `/Users/user123/data-brew-cleaner`
2. Create a new virtual environment `python -m venv /Users/user123/data-brew-cleaner/venv`
3. Activate virtual env: `source venv/bin/activate`
4. Install required libraries (mainly `boto3`): `pip install -r requirements.txt`
5. Deactivate virtual env for zipping preparation: `deactivate`
6. Navigate to the virtual environment's site-packages directory. The path might vary depending on your OS and Python version : `cd venv/lib/python3.8/site-packages`
7. Zip the contents of the site-packages directory: `zip -r9 /Users/user123/data-brew-cleaner/lambda_function.zip .`
8. Add your Lambda function code to the ZIP file: `cd /Users/user123/data-brew-cleaner` && `zip -g lambda_function.zip lambda_function.py`
9. Go to your AWS Console UI => Go to the Lambda section
10. Create a new lambda function and choose `Python 3.8` as the Runtime
11. Choose the function to update and choose the Code tab. Under Code source, choose Upload from. Choose `.zip` file that has been created on step 8, and then choose Upload.
    https://docs.aws.amazon.com/lambda/latest/dg/configuration-function-zip.html
13. By default creation, lambda timeout will be set into 3s, update runtime timeout into max 15 minutes
14. Last but not least, Lambda role needs permission to interact with DataBrew service. Go to your lambda function `Configuration > Permissions` page, click on the lambda role.
15. Add the policy by clicking on `Add Permissions` > `Attach Policies` > Choose `AwsGlueDataBrewFullAccessPolicy` for easiest setup > Check the check box > Click `Add permissions`
16. Lambda is ready to execute job/ruleset/dataset deletion from DataBrew without triggering `TooManyRequestException`


 
