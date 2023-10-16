---
id: deployments
title: Deployments
sidebar_label: Deployments
---

One of the Soil design principles is to make deployments easy and scalable. The same code should run in many deployments at the same time. Each deployment can have a different configuration. The configuration in a Soil app is located in `soil.yml` and the `config` folder.


## Autodeployment of a Soil Application

The code for an application should be only in one repository. The config folder and soil.yml files in it will only be used for local development.

Add the following .gitlab-ci.yml

```yaml
include:
  - project: 'amalfianalytics/devops/ci-templates'
    ref: master
    file: /bundles/soil-app.yml
```

Every time you push to the following branches: master, release/demo, release/production you will deploy to the following environments dev, demo prod.

## Creating a Soil Application Deployment
To create a new soil deplyoment create a new repo in the deployments group. Then add the `soil.yml` and `config` files and a `.gitlab-ci.yml` file with the following code:

```yaml
stages:
 - release

include:
  - project: 'amalfianalytics/devops/ci-templates'
    ref: master
    file: /release/release-alpha-beta-production.yml
```

Then ask the systems admin for the "soil line" setup with one or more of the following environments: dev, demo, prod.

Every time you push to the following branches: master, release/demo, release/production you will deploy to the following environments dev, demo prod.
