<p align="center">
  <a href="">
    <img alt="GitPoint" title="GitPoint" src="https://github.com/user-attachments/assets/88845961-0ca1-4fb8-b599-9b3adeb239c5" width="450">
  </a>
</p>

<p align="center">
  Cloud is on your under control.

## Introduction

This is a Cloud tool for DevOps/Cloud Engineers and Operations team members.
It can help you if you want to focus on hard tasks, because it can handle typical issues and troubleshooting them.

**Available for Linux/Windows and MacOs**
**Download it:** docker pull attilaszabocde/skyfix:latest
**Docker Reposirotry:** [Skyfix App](https://hub.docker.com/r/attilaszabocde/skyfix)

## Preconditions:
- Git
- Docker & Docker Compose
- Azure Cloud account

## Reasons Table:
- VM:
  - highcpu (Stoping the VM)
  - memoryusage (Scale up the VM)
  - vmstopped (VM restart)
- Containers:
  - contdown (Restarting the container)
  - conthighmem (Scale the container)
  - contmiss (Replace the container)

## Step by step
### 1. Please click on **releases** folder and download the file or copy it.

### 2. After that, please run this command where the file is: 
```bash
docker compose -f docker-compose_v1.yml up -d
```

### 3. Create an Azure Bot:
**Commands:**
```bash
az login
az account set --subscription "Your Subscription ID"
az ad sp create-for-rbac \
     --name "my-devops-bot" \
     --role Contributor \
     --scopes /subscriptions/$(az account show --query id -o tsv)
```
The output:
```bash
    {
    "appId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "displayName": "my-devops-bot",
    "password": "xxxxxxxxxxxxxxxxxxxxxxxx",
    "tenant": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
    }
```
### 4. Login into Skyfix and Add Data source in Grafana (Use Azure Monitor)

### 5. Create an Contract points where you have to add these informations:
- Add a name like: Skyfix webhook
- Add an Integration: Webhook
- URL: http://<container-ip-address>:<webapp-port>/alert
- HTTP Method: POST
- Extra Headers: Name: Content-Type, Value: application/json

### 6. Create an Alert:
- Enter a name
- Enter a query
- Add folder ands labels: --- **IMPORTANT** ----
  Add new label: key=reason, value=<choose one form reason>
- Fill up the other things and Done!

## Technology
* **Cloud** - ![Azure](https://img.shields.io/badge/azure-%230072C6.svg?style=for-the-badge&logo=microsoftazure&logoColor=white)
* **CI/CD** - ![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)
* **Framework** - ![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
* **Back-end** - ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
* **Front-end** - ![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white) ![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)
* **Database** - ![MySQL](https://img.shields.io/badge/mysql-4479A1.svg?style=for-the-badge&logo=mysql&logoColor=white)
* **Scripts** - ![Bash Script](https://img.shields.io/badge/bash_script-%23121011.svg?style=for-the-badge&logo=gnu-bash&logoColor=white) ![PowerShell](https://img.shields.io/badge/PowerShell-%235391FE.svg?style=for-the-badge&logo=powershell&logoColor=white)

## Picture of Fixing Dashboard
<img width="1920" height="1080" alt="Képernyőfotó 2025-10-01 - 19 16 43" src="https://github.com/user-attachments/assets/1d24897d-0ae3-46f0-abc1-2dbf44a5aadc" />
<img width="1920" height="1080" alt="Képernyőfotó 2025-10-01 - 19 14 45" src="https://github.com/user-attachments/assets/adcb6dcc-698d-46ad-8548-0b7b2a44902d" />
<img width="1920" height="1080" alt="Képernyőfotó 2025-10-01 - 19 08 19" src="https://github.com/user-attachments/assets/4d7ed769-67ad-4a7c-81e3-b0df418d3ead" />
<img width="1920" height="1080" alt="Képernyőfotó 2025-10-01 - 19 06 11" src="https://github.com/user-attachments/assets/2868734c-362c-40d0-8c81-e38c8cd49497" />
<img width="1920" height="1080" alt="Képernyőfotó 2025-10-01 - 19 06 33" src="https://github.com/user-attachments/assets/600d203b-02ec-4210-9ff8-c7d4f1168bb0" />
