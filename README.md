# banking-marketingd

- [x] problem description
- [x] experiment tracking
- [x] experiment registry - local
- [x] workflow orchestration - local
- [x] persist changes on mlflow
- [x] save artifacts
- [x] pip install requirements in mage container
- [x] promote top model to production
- [x] deployment - model container
- [ ] split data by season
- [ ] model monitoring in grafana
- [ ] trigger retraining if performance decrease (test with data from different season)
- [ ] modify ingest to read data from personal github repo instead of uci url, to get data for specific season
- [ ] documentation
- [ ] unit tests
- [ ] integration test
- [ ] linting / formatting
- [ ] makefile
- [ ] pre-commit hooks
- [ ] ci/cd
- [ ] experiment registry - cloud
- [ ] workflow orchestration - cloud (check volumes in docker_compose.yaml, don't upload ssh keys to cloud)
- [ ] iac 
- [ ] hyperparameter tuning
- [ ] copy only necessary files to mage docker container (./:/home/src copies everything)

## Evaluation Criteria

* Problem description
    * 0 points: The problem is not described
    * 1 point: The problem is described but shortly or not clearly 
    * 2 points: The problem is well described and it's clear what the problem the project solves
* Cloud
    * 0 points: Cloud is not used, things run only locally
    * 2 points: The project is developed on the cloud OR uses localstack (or similar tool) OR the project is deployed to Kubernetes or similar container management platforms
    * 4 points: The project is developed on the cloud and IaC tools are used for provisioning the infrastructure
* Experiment tracking and model registry
    * 0 points: No experiment tracking or model registry
    * 2 points: Experiments are tracked or models are registered in the registry
    * 4 points: Both experiment tracking and model registry are used
* Workflow orchestration
    * 0 points: No workflow orchestration
    * 2 points: Basic workflow orchestration
    * 4 points: Fully deployed workflow 
* Model deployment
    * 0 points: Model is not deployed
    * 2 points: Model is deployed but only locally
    * 4 points: The model deployment code is containerized and could be deployed to cloud or special tools for model deployment are used
* Model monitoring
    * 0 points: No model monitoring
    * 2 points: Basic model monitoring that calculates and reports metrics
    * 4 points: Comprehensive model monitoring that sends alerts or runs a conditional workflow (e.g. retraining, generating debugging dashboard, switching to a different model) if the defined metrics threshold is violated
* Reproducibility
    * 0 points: No instructions on how to run the code at all, the data is missing
    * 2 points: Some instructions are there, but they are not complete OR instructions are clear and complete, the code works, but the data is missing
    * 4 points: Instructions are clear, it's easy to run the code, and it works. The versions for all the dependencies are specified.
* Best practices
    * [ ] There are unit tests (1 point)
    * [ ] There is an integration test (1 point)
    * [ ] Linter and/or code formatter are used (1 point)
    * [ ] There's a Makefile (1 point)
    * [ ] There are pre-commit hooks (1 point)
    * [ ] There's a CI/CD pipeline (2 points)


## Bank Marketing Problem Description

In 2012 a Portuguese banking institution collected data for several direct marketing campaigns it conducted in order to analyze it and to build machine learning models that can increase the efficiency of future marketing campaigns.

A marketing campaign is a concentrated effort by the bank in which it contacts its customers by phone and asks them to subscribe to a term deposit. Term deposits, aka certificate depoists, are deposits by customers that are made for a specific period of time and tradionally return more interest than savings accounts. They provide a guarantee for the banks that the money will remain available for a known period of time, which helps them better manage their available capitol.

In this project, I'll be using the this dataset which can be downloaded from the UCI repository [here](https://archive.ics.uci.edu/dataset/222/bank+marketing)

My goal is to train an ML model that can predict whether a customer will subscribe to a term deposit. I'll priortize profit making over regulating spending. In other words, I'll prefer a model with a lower false negative rate over one with a lower false positive rate. 

The dataset has 16 features, and one target variable: 

| Variable Name | Role     | Type        | Demographic       | Description | Units | Missing Values |
|---------------|----------|-------------|-------------------|-------------|-------|----------------|
| age           | Feature  | Integer     | Age               |             |       | no             |
| job           | Feature  | Categorical | Occupation        |             |       | no             |
| marital       | Feature  | Categorical | Marital Status    |             |       | no             |
| education     | Feature  | Categorical | Education Level   |             |       | no             |
| default       | Feature  | Binary      |                   | has credit in default? | | no |
| balance       | Feature  | Integer     |                   | average yearly balance | euros | no |
| housing       | Feature  | Binary      |                   | has housing loan? | | no |
| loan          | Feature  | Binary      |                   | has personal loan? | | no |
| contact       | Feature  | Categorical |                   | contact communication type (categorical: 'cellular','telephone') | | yes |
| day_of_week   | Feature  | Date        |                   | last contact day of the week | | no |
| month         | Feature  | Date        |                   | last contact month of year (categorical: 'jan', 'feb', 'mar', ..., 'nov', 'dec') | | no |
| duration      | Feature  | Integer     |                   | last contact duration, in seconds (numeric). Important note: this attribute highly affects the output target (e.g., if duration=0 then y='no'). Yet, the duration is not known before a call is performed. Also, after the end of the call y is obviously known. Thus, this input should only be included for benchmark purposes and should be discarded if the intention is to have a realistic predictive model. | | no |
| campaign      | Feature  | Integer     |                   | number of contacts performed during this campaign and for this client (numeric, includes last contact) | | no |
| pdays         | Feature  | Integer     |                   | number of days that passed by after the client was last contacted from a previous campaign (numeric; -1 means client was not previously contacted) | | yes |
| previous      | Feature  | Integer     |                   | number of contacts performed before this campaign and for this client | | no |
| poutcome      | Feature  | Categorical |                   | outcome of the previous marketing campaign (categorical: 'failure','nonexistent','success') | | yes |
| y             | Target   | Binary      |                   | has the client subscribed a term deposit? | | |:

Plan layout:  
1- Data preparation  
2- Exploratory data analysis  
3- Feature Engineering / Transformations  
4- Model training and assessment   
5- Deploy model using flask  
6- Manage package dependency using Pipfile  
7- Create a docker container image  


#### Running the code 

You can run the docker image of the app using this command:  

`docker run -it --rm -p 9696:9696 bank-marketing`  

To test the app, run the following command in a separate terminal:  

`python predict-test.py`

```bash
# to build a docker image. 
docker build -t response_predictor:v001 -f predict.dockerfile .

docker run -it response_predictor:v001 /bin/bash

# use the -p option to bind the image to a port to access the webservice
docker run -it --rm -p 9696:9696 response_predictor:v001
```