---
name: azure-devops
description: Senior Azure DevOps engineering capabilities for comprehensive cloud DevOps operations. Use PROACTIVELY for Azure DevOps pipelines, Azure CLI commands, AKS deployments, infrastructure as code, and CI/CD workflows.
triggers:
  - azure
  - devops
  - pipeline
  - aks
  - azure devops
  - azdo
  - az cli
  - azure cli
  - yaml pipeline
  - azure repos
  - azure boards
  - azure artifacts
  - service connection
  - variable group
  - agent pool
  - bicep
  - arm template
  - terraform azure
---

# Azure DevOps Skill

## Overview

This skill provides senior-level Azure DevOps engineering capabilities. It covers the complete Azure DevOps ecosystem including Azure CLI, Azure DevOps CLI extension, YAML pipeline authoring, Infrastructure as Code, and enterprise CI/CD patterns.

## Prerequisites

### Required Tools
```bash
# Azure CLI
brew install azure-cli  # macOS
winget install Microsoft.AzureCLI  # Windows

# Azure DevOps CLI extension
az extension add --name azure-devops

# Optional but recommended
brew install bicep  # Bicep CLI
brew install terraform  # Terraform
```

### Authentication
```bash
# Login to Azure
az login

# Login with service principal (CI/CD)
az login --service-principal -u <app-id> -p <password-or-cert> --tenant <tenant-id>

# Set default subscription
az account set --subscription "<subscription-id-or-name>"

# Configure Azure DevOps defaults
az devops configure --defaults organization=https://dev.azure.com/<org> project=<project>
```

## Core Capabilities

---

## 1. Azure CLI Reference

### Account & Subscription Management

```bash
# List all subscriptions
az account list --output table

# Show current subscription
az account show

# Set subscription
az account set --subscription "<subscription-id>"

# List tenants
az account tenant list

# Clear account cache
az account clear
```

### Resource Groups

```bash
# Create resource group
az group create --name myResourceGroup --location eastus

# List resource groups
az group list --output table

# Show resource group details
az group show --name myResourceGroup

# Delete resource group (DANGEROUS)
az group delete --name myResourceGroup --yes --no-wait

# Export template from resource group
az group export --name myResourceGroup > template.json

# Wait for resource group operations
az group wait --name myResourceGroup --created
```

### Resource Management

```bash
# List all resources in a group
az resource list --resource-group myResourceGroup --output table

# Show specific resource
az resource show --ids <resource-id>

# Delete resource
az resource delete --ids <resource-id>

# Move resource to another group
az resource move --destination-group newGroup --ids <resource-id>

# Tag resources
az resource tag --ids <resource-id> --tags Environment=Production Team=Platform

# Lock resource (prevent deletion)
az lock create --name MyLock --resource-group myResourceGroup --resource-type Microsoft.Storage/storageAccounts --resource-name mystorageaccount --lock-type CanNotDelete
```

---

## 2. Azure DevOps CLI Extension

### Organization & Project Management

```bash
# List organizations
az devops organization list

# Show organization details
az devops organization show --org https://dev.azure.com/<org>

# Create project
az devops project create --name "MyProject" --description "Project description" --visibility private --source-control git --process Agile

# List projects
az devops project list --output table

# Show project
az devops project show --project "MyProject"

# Update project
az devops project update --project "MyProject" --description "New description"

# Delete project
az devops project delete --project "MyProject" --yes

# Get project properties
az devops project show --project "MyProject" --query "properties"
```

### Repositories (Azure Repos)

```bash
# Create repository
az repos create --name "MyRepo" --project "MyProject"

# List repositories
az repos list --project "MyProject" --output table

# Show repository
az repos show --repository "MyRepo" --project "MyProject"

# Delete repository
az repos delete --repository "MyRepo" --project "MyProject" --yes

# Create branch policy
az repos policy branch create --project "MyProject" --repository-id <repo-id> --branch main --policy-type "Minimum number of reviewers" --settings '{"minimumApproverCount": 2, "creatorVoteCounts": false, "allowDownvotes": false}'

# List branch policies
az repos policy list --project "MyProject" --repository-id <repo-id> --branch main

# Create PR
az repos pr create --project "MyProject" --repository "MyRepo" --source-branch feature/my-feature --target-branch main --title "My PR" --description "PR description"

# List PRs
az repos pr list --project "MyProject" --repository "MyRepo" --status active

# Update PR
az repos pr update --id <pr-id> --status completed --merge-commit-message "Merged PR"

# Create PR reviewer
az repos pr reviewer add --id <pr-id> --reviewers <user-id>

# Create policy for required reviewers
az repos policy required-reviewer create --project "MyProject" --repository-id <repo-id> --branch main --enabled true --blocking true --settings '{"requiredReviewerIds": ["<user-id>"], "message": "Requires review"}'
```

### Pipelines

```bash
# Create pipeline (from YAML file)
az pipelines create --name "MyPipeline" --project "MyProject" --repository "MyRepo" --repository-type tfsgit --branch main --yml-path azure-pipelines.yml

# List pipelines
az pipelines list --project "MyProject" --output table

# Show pipeline
az pipelines show --name "MyPipeline" --project "MyProject"

# Run pipeline
az pipelines run --name "MyPipeline" --project "MyProject" --branch main

# Run with parameters
az pipelines run --name "MyPipeline" --project "MyProject" --parameters env=production version=1.0.0

# Run with variables
az pipelines run --name "MyPipeline" --project "MyProject" --variables buildConfiguration=Release

# Delete pipeline
az pipelines delete --name "MyPipeline" --project "MyProject" --yes

# List pipeline runs
az pipelines runs list --project "MyProject" --pipeline-ids <pipeline-id>

# Show pipeline run
az pipelines runs show --id <run-id> --project "MyProject"

# Cancel pipeline run
az pipelines runs cancel --id <run-id> --project "MyProject"

# List pipeline definitions
az pipelines definition list --project "MyProject"

# Build (classic) commands
az pipelines build list --project "MyProject"
az pipelines build queue --definition-name "MyBuild" --project "MyProject"
az pipelines build show --id <build-id> --project "MyProject"
```

### Variable Groups

```bash
# Create variable group
az pipelines variable-group create --name "MyVars" --project "MyProject" --variables env=production region=eastus --authorize true

# List variable groups
az pipelines variable-group list --project "MyProject" --output table

# Show variable group
az pipelines variable-group show --group-id <id> --project "MyProject"

# Update variable group
az pipelines variable-group update --group-id <id> --project "MyProject" --variables newVar=newValue

# Delete variable group
az pipelines variable-group delete --group-id <id> --project "MyProject" --yes

# Add variable to group
az pipelines variable-group variable create --group-id <id> --name "apiKey" --value "secret-value" --secret true

# Update variable in group
az pipelines variable-group variable update --group-id <id> --name "apiKey" --value "new-value" --secret true

# Delete variable from group
az pipelines variable-group variable delete --group-id <id> --name "apiKey" --yes
```

### Service Connections

```bash
# Create Azure Resource Manager service connection (automatic)
az devops service-endpoint azurerm create --name "MyAzureConnection" --project "MyProject" --azure-rm-service-principal-id <app-id> --azure-rm-subscription-id <sub-id> --azure-rm-subscription-name <sub-name> --azure-rm-tenant-id <tenant-id>

# List service connections
az devops service-endpoint list --project "MyProject" --output table

# Show service connection
az devops service-endpoint show --id <connection-id> --project "MyProject"

# Delete service connection
az devops service-endpoint delete --id <connection-id> --project "MyProject" --yes

# Create GitHub service connection
az devops service-endpoint github create --name "MyGitHub" --project "MyProject" --github-url https://github.com --github-access-token <pat>
```

### Agent Pools

```bash
# List agent pools
az pipelines pool list --output table

# Show agent pool
az pipelines pool show --pool-id <id>

# List agents in pool
az pipelines agent list --pool-id <id> --output table

# Show agent details
az pipelines agent show --pool-id <id> --agent-id <agent-id>

# Create agent pool
az pipelines pool create --name "MyPool" --pool-type automation --auto-provision false

# Delete agent pool
az pipelines pool delete --pool-id <id> --yes

# Create agent queue
az pipelines queue create --name "MyQueue" --project "MyProject" --pool-id <id>
```

### Environments

```bash
# List environments
az pipelines environment list --project "MyProject" --output table

# Show environment
az pipelines environment show --environment-id <id> --project "MyProject"

# Create environment
az pipelines environment create --name "Production" --project "MyProject"

# Delete environment
az pipelines environment delete --environment-id <id> --project "MyProject" --yes
```

### Boards (Work Items)

```bash
# Create work item
az boards work-item create --title "New Bug" --type "Bug" --project "MyProject" --description "Bug description" --area "MyArea" --iteration "Sprint 1"

# Show work item
az boards work-item show --id <work-item-id> --project "MyProject"

# Update work item
az boards work-item update --id <work-item-id> --project "MyProject" --state "In Progress" --assigned-to <user-email>

# List work items (query)
az boards query --project "MyProject" --wiql "SELECT [System.Id], [System.Title], [System.State] FROM WorkItems WHERE [System.WorkItemType] = 'Bug'"

# Delete work item
az boards work-item delete --id <work-item-id> --project "MyProject" --yes

# List work item types
az boards work-item-type list --project "MyProject"

# List areas
az boards area project list --project "MyProject"

# Create area
az boards area project create --name "MyArea" --project "MyProject"

# List iterations
az boards iteration project list --project "MyProject"

# Create iteration
az boards iteration project create --name "Sprint 1" --project "MyProject" --start-date "2024-01-01" --finish-date "2024-01-14"

# List sprints
az boards sprint list --project "MyProject"

# Show sprint
az boards sprint show --id <sprint-id> --project "MyProject"
```

### Artifacts (Feeds & Packages)

```bash
# List feeds
az artifacts universal list --project "MyProject" --output table

# Create feed
az artifacts feed create --name "MyFeed" --project "MyProject"

# Show feed
az artifacts feed show --feed "MyFeed" --project "MyProject"

# Delete feed
az artifacts feed delete --feed "MyFeed" --project "MyProject" --yes

# Publish universal package
az artifacts universal publish --feed "MyFeed" --name "MyPackage" --version "1.0.0" --description "Package description" --path ./artifacts

# Download universal package
az artifacts universal download --feed "MyFeed" --name "MyPackage" --version "1.0.0" --path ./download

# List package versions
az artifacts package list --feed "MyFeed" --project "MyProject"
```

### Test Plans

```bash
# List test plans
az pipelines test-plan list --project "MyProject"

# Show test plan
az pipelines test-plan show --test-plan-id <id> --project "MyProject"

# Create test plan
az pipelines test-plan create --name "MyTestPlan" --project "MyProject"

# Delete test plan
az pipelines test-plan delete --test-plan-id <id> --project "MyProject" --yes
```

### Teams & Security

```bash
# List teams
az devops team list --project "MyProject" --output table

# Show team
az devops team show --team "MyTeam" --project "MyProject"

# Create team
az devops team create --name "MyTeam" --project "MyProject"

# Add member to team
az devops team member add --team "MyTeam" --project "MyProject" --member <user-id>

# List team members
az devops team member list --team "MyTeam" --project "MyProject"

# List security groups
az devops security group list --project "MyProject" --output table

# Create security group
az devops security group create --name "MyGroup" --project "MyProject" --description "Custom group"

# Add member to security group
az devops security group membership add --group-id <group-id> --member-id <user-id>

# List security namespaces
az devops security namespace list --output table
```

---

## 3. Pipeline Authoring

### Basic Pipeline Structure

```yaml
# azure-pipelines.yml
trigger:
  branches:
    include:
      - main
      - release/*
  paths:
    exclude:
      - README.md
      - docs/*

pr:
  branches:
    include:
      - main
  drafts: false

pool:
  vmImage: 'ubuntu-latest'

variables:
  buildConfiguration: 'Release'
  dotnetVersion: '8.0.x'

steps:
- task: UseDotNet@2
  inputs:
    packageType: 'sdk'
    version: $(dotnetVersion)

- script: dotnet build --configuration $(buildConfiguration)
  displayName: 'Build project'

- script: dotnet test --configuration $(buildConfiguration) --no-build --logger trx
  displayName: 'Run tests'

- task: PublishTestResults@2
  inputs:
    testResultsFiles: '**/*.trx'
    testRunTitle: 'Unit Tests'
```

### Multi-Stage Pipeline

```yaml
trigger:
  - main

stages:
- stage: Build
  displayName: 'Build Stage'
  jobs:
  - job: Build
    displayName: 'Build Job'
    pool:
      vmImage: 'ubuntu-latest'
    steps:
    - script: echo "Building..."
    - publish: $(Build.SourcesDirectory)/src
      artifact: sourceCode

- stage: Test
  displayName: 'Test Stage'
  dependsOn: Build
  jobs:
  - job: UnitTests
    displayName: 'Unit Tests'
    steps:
    - download: current
      artifact: sourceCode
    - script: echo "Running unit tests..."
    
  - job: IntegrationTests
    displayName: 'Integration Tests'
    dependsOn: UnitTests
    steps:
    - download: current
      artifact: sourceCode
    - script: echo "Running integration tests..."

- stage: Deploy
  displayName: 'Deploy Stage'
  dependsOn: Test
  condition: succeeded()
  jobs:
  - deployment: DeployWeb
    displayName: 'Deploy Web App'
    environment: 'Production'
    strategy:
      runOnce:
        deploy:
          steps:
          - script: echo "Deploying to Production..."
```

### Pipeline Templates

**Template file (templates/build.yml):**
```yaml
parameters:
- name: buildConfiguration
  type: string
  default: 'Release'
- name: projects
  type: string
  default: '**/*.csproj'
- name: dotnetVersion
  type: string
  default: '8.0.x'

steps:
- task: UseDotNet@2
  inputs:
    packageType: 'sdk'
    version: ${{ parameters.dotnetVersion }}
  displayName: 'Install .NET SDK'

- task: DotNetCoreCLI@2
  inputs:
    command: 'build'
    projects: ${{ parameters.projects }}
    arguments: '--configuration ${{ parameters.buildConfiguration }}'
  displayName: 'Build Projects'

- task: DotNetCoreCLI@2
  inputs:
    command: 'test'
    projects: ${{ parameters.projects }}
    arguments: '--configuration ${{ parameters.buildConfiguration }} --no-build'
  displayName: 'Run Tests'
```

**Using the template:**
```yaml
# azure-pipelines.yml
trigger:
  - main

stages:
- stage: Build
  jobs:
  - job: BuildAPI
    steps:
    - template: templates/build.yml
      parameters:
        buildConfiguration: 'Release'
        projects: 'src/API/*.csproj'
        dotnetVersion: '8.0.x'

  - job: BuildWorker
    steps:
    - template: templates/build.yml
      parameters:
        buildConfiguration: 'Release'
        projects: 'src/Worker/*.csproj'
        dotnetVersion: '8.0.x'
```

### Conditional Logic

```yaml
variables:
  ${{ if eq(variables['Build.SourceBranch'], 'refs/heads/main') }}:
    environment: 'Production'
  ${{ if ne(variables['Build.SourceBranch'], 'refs/heads/main') }}:
    environment: 'Development'

steps:
- ${{ if eq(variables['Build.SourceBranch'], 'refs/heads/main') }}:
  - script: echo "Deploying to Production"
    displayName: 'Production Deploy'

- ${{ if ne(variables['Build.SourceBranch'], 'refs/heads/main') }}:
  - script: echo "Deploying to Development"
    displayName: 'Development Deploy'

# Using conditions on steps
- script: echo "This runs only on main"
  condition: eq(variables['Build.SourceBranch'], 'refs/heads/main')

# Using stage conditions
- stage: Deploy
  condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/main'))
```

### Matrix Strategy

```yaml
strategy:
  matrix:
    linux:
      imageName: 'ubuntu-latest'
      dotnetVersion: '8.0.x'
    windows:
      imageName: 'windows-latest'
      dotnetVersion: '8.0.x'
    mac:
      imageName: 'macos-latest'
      dotnetVersion: '8.0.x'
  maxParallel: 3

pool:
  vmImage: $(imageName)

steps:
- task: UseDotNet@2
  inputs:
    packageType: 'sdk'
    version: $(dotnetVersion)
```

### Deployment Jobs with Environments

```yaml
stages:
- stage: Deploy
  jobs:
  - deployment: DeployApp
    displayName: 'Deploy Application'
    environment: 
      name: 'Production'
      resourceType: VirtualMachine
      tags: web
    strategy:
      runOnce:
        deploy:
          steps:
          - script: echo "Deploying to Production"
          
  - deployment: DeployWithApprovals
    displayName: 'Deploy with Manual Approval'
    environment: 'Staging'
    strategy:
      runOnce:
        deploy:
          steps:
          - script: echo "Deploying to Staging"
```

### Blue-Green Deployment

```yaml
stages:
- stage: DeployBlue
  displayName: 'Deploy to Blue Environment'
  jobs:
  - deployment: DeployBlue
    environment: 'Production-Blue'
    strategy:
      runOnce:
        deploy:
          steps:
          - task: AzureWebApp@1
            inputs:
              azureSubscription: 'MyServiceConnection'
              appName: 'myapp-blue'
              package: $(Pipeline.Workspace)/drop/*.zip

- stage: SwitchTraffic
  displayName: 'Switch Traffic to Blue'
  dependsOn: DeployBlue
  jobs:
  - deployment: SwitchTraffic
    environment: 'Production'
    strategy:
      runOnce:
        deploy:
          steps:
          - task: AzureAppServiceManage@0
            inputs:
              azureSubscription: 'MyServiceConnection'
              Action: 'Swap Slots'
              WebAppName: 'myapp'
              ResourceGroupName: 'myResourceGroup'
              SourceSlot: 'blue'
              TargetSlot: 'production'

- stage: DeployGreen
  displayName: 'Deploy to Green Environment'
  dependsOn: SwitchTraffic
  jobs:
  - deployment: DeployGreen
    environment: 'Production-Green'
    strategy:
      runOnce:
        deploy:
          steps:
          - task: AzureWebApp@1
            inputs:
              azureSubscription: 'MyServiceConnection'
              appName: 'myapp-green'
              package: $(Pipeline.Workspace)/drop/*.zip
```

### Canary Deployment

```yaml
stages:
- stage: Canary
  displayName: 'Canary Deployment (10%)'
  jobs:
  - deployment: Canary
    environment: 'Production'
    strategy:
      canary:
        increments: [10, 25, 50, 100]
        preDeploy:
          steps:
          - script: echo "Pre-deploy checks"
        deploy:
          steps:
          - task: KubernetesManifest@1
            inputs:
              action: 'deploy'
              kubernetesServiceConnection: 'aks-connection'
              namespace: 'production'
              manifests: 'k8s/deployment.yml'
              strategy: 'canary'
              percentage: 10
        postRouteTraffic:
          steps:
          - script: echo "Verify canary health"
          - task: AzureMonitor@1
            inputs:
              resourceGroupName: 'myResourceGroup'
              alertType: 'metric'
              action: 'check'
        on:
          failure:
            steps:
            - script: echo "Rollback triggered"
          success:
            steps:
            - script: echo "Canary successful"
```

### Container Jobs

```yaml
resources:
  containers:
  - container: build
    image: mcr.microsoft.com/dotnet/sdk:8.0
  - container: test
    image: mcr.microsoft.com/dotnet/sdk:8.0
    options: --hostname test-container

jobs:
- job: BuildInContainer
  container: build
  steps:
  - script: dotnet build
    displayName: 'Build in Container'

- job: TestInContainer
  container: test
  dependsOn: BuildInContainer
  steps:
  - script: dotnet test
    displayName: 'Test in Container'

# Custom container with service containers
- job: IntegrationTests
  container:
    image: mcr.microsoft.com/dotnet/sdk:8.0
  services:
    postgres:
      image: postgres:15
      env:
        POSTGRES_PASSWORD: $(postgresPassword)
      ports:
      - 5432:5432
  steps:
  - script: dotnet test --filter "Category=Integration"
    displayName: 'Run Integration Tests'
```

### Self-Hosted Agents

```yaml
# Use self-hosted agent pool
pool: 
  name: 'MySelfHostedPool'
  demands:
  - agent.os -equals Linux
  - npm

# Or with agent capabilities
pool:
  name: 'MySelfHostedPool'
  demands:
  - Agent.OS -equals Linux
  - Agent.Version -gtVersion 2.200.0

# Job-level pool override
jobs:
- job: Build
  pool: 'MySelfHostedPool'
  steps:
  - script: echo "Building on self-hosted agent"

- job: Deploy
  pool:
    vmImage: 'ubuntu-latest'
  steps:
  - script: echo "Deploying on Microsoft-hosted agent"
```

### Service Connections in Pipelines

```yaml
# Azure Resource Manager
- task: AzureWebApp@1
  inputs:
    azureSubscription: 'MyArmConnection'  # Service connection name
    appName: 'my-web-app'
    package: $(Pipeline.Workspace)/drop/*.zip

# Kubernetes
- task: KubernetesManifest@1
  inputs:
    kubernetesServiceConnection: 'MyAksConnection'
    action: 'deploy'
    namespace: 'default'
    manifests: 'k8s/*.yml'

# Docker Registry
- task: Docker@2
  inputs:
    containerRegistry: 'MyAcrConnection'  # Docker registry service connection
    repository: 'myapp'
    command: 'buildAndPush'
    Dockerfile: 'Dockerfile'
    tags: |
      $(Build.BuildId)
      latest

# GitHub
- task: GitHubRelease@1
  inputs:
    gitHubConnection: 'MyGitHubConnection'
    repositoryName: 'myorg/myrepo'
    action: 'create'
    tagSource: 'userSpecifiedTag'
    tag: 'v$(Build.BuildId)'
```

### Key Vault Integration

```yaml
# Azure Key Vault task
- task: AzureKeyVault@2
  inputs:
    azureSubscription: 'MyServiceConnection'
    KeyVaultName: 'my-keyvault'
    SecretsFilter: '*'
    RunAsPreJob: false

# Use secrets in subsequent tasks
- script: |
    echo "Database connection string: $(DatabaseConnectionString)"
  env:
    DB_CONNECTION: $(DatabaseConnectionString)

# Map secrets to variables
variables:
- group: 'MyVariableGroup'
- name: dbPassword
  value: $[variables.DatabasePassword]
```

---

## 4. Infrastructure as Code

### Bicep Templates

**main.bicep:**
```bicep
@description('Location for all resources')
param location string = resourceGroup().location

@description('Name of the storage account')
param storageAccountName string

@description('Storage account SKU')
param storageSku string = 'Standard_LRS'

@description('Tags to apply to resources')
param tags object = {
  environment: 'production'
  project: 'myapp'
}

resource storageAccount 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: storageAccountName
  location: location
  sku: {
    name: storageSku
  }
  kind: 'StorageV2'
  properties: {
    accessTier: 'Hot'
    minimumTlsVersion: 'TLS1_2'
    supportsHttpsTrafficOnly: true
  }
  tags: tags
}

resource appServicePlan 'Microsoft.Web/serverfarms@2023-01-01' = {
  name: '${storageAccountName}-plan'
  location: location
  sku: {
    name: 'P1v3'
    tier: 'PremiumV3'
    capacity: 1
  }
  properties: {
    reserved: false
  }
  tags: tags
}

resource webApp 'Microsoft.Web/sites@2023-01-01' = {
  name: '${storageAccountName}-app'
  location: location
  properties: {
    serverFarmId: appServicePlan.id
    siteConfig: {
      appSettings: [
        {
          name: 'StorageConnectionString'
          value: 'DefaultEndpointsProtocol=https;AccountName=${storageAccount.name};EndpointSuffix=core.windows.net'
        }
      ]
      httpsOnly: true
      minTlsVersion: '1.2'
    }
  }
  tags: tags
}

output storageAccountId string = storageAccount.id
output webAppUrl string = 'https://${webApp.defaultHostName}'
```

**Deploy Bicep with Azure CLI:**
```bash
# Validate template
az deployment group validate --resource-group myResourceGroup --template-file main.bicep --parameters storageAccountName=mystorage123

# What-if deployment (preview changes)
az deployment group what-if --resource-group myResourceGroup --template-file main.bicep --parameters storageAccountName=mystorage123

# Deploy
az deployment group create --resource-group myResourceGroup --template-file main.bicep --parameters storageAccountName=mystorage123

# Deploy with parameter file
az deployment group create --resource-group myResourceGroup --template-file main.bicep --parameters @parameters.json
```

**Bicep Pipeline:**
```yaml
trigger:
  - main

pool:
  vmImage: 'ubuntu-latest'

stages:
- stage: Validate
  jobs:
  - job: Validate
    steps:
    - task: AzureCLI@2
      inputs:
        azureSubscription: 'MyServiceConnection'
        scriptType: 'bash'
        scriptLocation: 'inlineScript'
        inlineScript: |
          az deployment group validate \
            --resource-group $(resourceGroup) \
            --template-file ./infrastructure/main.bicep \
            --parameters ./infrastructure/parameters.json

- stage: Deploy
  dependsOn: Validate
  jobs:
  - deployment: DeployInfrastructure
    environment: 'Production'
    strategy:
      runOnce:
        deploy:
          steps:
          - task: AzureCLI@2
            inputs:
              azureSubscription: 'MyServiceConnection'
              scriptType: 'bash'
              scriptLocation: 'inlineScript'
              inlineScript: |
                az deployment group create \
                  --resource-group $(resourceGroup) \
                  --template-file ./infrastructure/main.bicep \
                  --parameters ./infrastructure/parameters.json
```

### ARM Templates

```json
{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
  "contentVersion": "1.0.0.0",
  "parameters": {
    "storageAccountName": {
      "type": "string",
      "minLength": 3,
      "maxLength": 24,
      "metadata": {
        "description": "Name of the storage account"
      }
    },
    "location": {
      "type": "string",
      "defaultValue": "[resourceGroup().location]",
      "metadata": {
        "description": "Location for all resources"
      }
    },
    "storageSku": {
      "type": "string",
      "defaultValue": "Standard_LRS",
      "allowedValues": ["Standard_LRS", "Standard_GRS", "Premium_LRS"],
      "metadata": {
        "description": "Storage account SKU"
      }
    }
  },
  "variables": {
    "storageApiVersion": "2023-05-01"
  },
  "resources": [
    {
      "type": "Microsoft.Storage/storageAccounts",
      "apiVersion": "[variables('storageApiVersion')]",
      "name": "[parameters('storageAccountName')]",
      "location": "[parameters('location')]",
      "sku": {
        "name": "[parameters('storageSku')]"
      },
      "kind": "StorageV2",
      "properties": {
        "accessTier": "Hot",
        "minimumTlsVersion": "TLS1_2"
      }
    }
  ],
  "outputs": {
    "storageAccountId": {
      "type": "string",
      "value": "[resourceId('Microsoft.Storage/storageAccounts', parameters('storageAccountName'))]"
    }
  }
}
```

### Terraform with Azure

**main.tf:**
```hcl
provider "azurerm" {
  features {}
  subscription_id = var.subscription_id
  tenant_id       = var.tenant_id
}

resource "azurerm_resource_group" "main" {
  name     = "${var.prefix}-rg"
  location = var.location
  tags     = var.tags
}

resource "azurerm_storage_account" "main" {
  name                     = "${var.prefix}storage"
  resource_group_name      = azurerm_resource_group.main.name
  location                 = azurerm_resource_group.main.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  min_tls_version          = "TLS1_2"

  tags = var.tags
}

resource "azurerm_app_service_plan" "main" {
  name                = "${var.prefix}-plan"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  sku {
    tier = "PremiumV3"
    size = "P1v3"
  }
  tags = var.tags
}

resource "azurerm_linux_web_app" "main" {
  name                = "${var.prefix}-app"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  service_plan_id     = azurerm_app_service_plan.main.id

  site_config {
    always_on = true
    application_stack {
      docker_image     = "${var.acr_name}.azurecr.io/${var.image_name}"
      docker_image_tag = var.image_tag
    }
  }

  app_settings = {
    "WEBSITES_ENABLE_APP_SERVICE_STORAGE" = "false"
    "DOCKER_REGISTRY_SERVER_URL"          = "https://${var.acr_name}.azurecr.io"
    "DOCKER_REGISTRY_SERVER_USERNAME"     = var.acr_username
    "DOCKER_REGISTRY_SERVER_PASSWORD"     = var.acr_password
  }

  tags = var.tags
}

output "web_app_url" {
  value = azurerm_linux_web_app.main.default_hostname
}
```

**Terraform Pipeline with Remote State:**
```yaml
trigger:
  - main

variables:
  terraformVersion: '1.6.0'
  storageAccount: 'tfstate'
  container: 'tfstate'
  stateKey: 'terraform.tfstate'

stages:
- stage: TerraformPlan
  displayName: 'Terraform Plan'
  jobs:
  - job: Plan
    steps:
    - task: TerraformInstaller@0
      inputs:
        terraformVersion: $(terraformVersion)
    
    - task: TerraformTaskV4@4
      displayName: 'Terraform Init'
      inputs:
        provider: 'azurerm'
        command: 'init'
        backendServiceArm: 'MyServiceConnection'
        backendAzureRmResourceGroupName: 'terraform-state-rg'
        backendAzureRmStorageAccountName: $(storageAccount)
        backendAzureRmContainerName: $(container)
        backendAzureRmKey: $(stateKey)
    
    - task: TerraformTaskV4@4
      displayName: 'Terraform Plan'
      inputs:
        provider: 'azurerm'
        command: 'plan'
        commandOptions: '-out=tfplan -var-file="$(Build.SourcesDirectory)/terraform/variables/$(environment).tfvars"'
        environmentServiceNameAzureRM: 'MyServiceConnection'

- stage: TerraformApply
  displayName: 'Terraform Apply'
  dependsOn: TerraformPlan
  condition: succeeded()
  jobs:
  - deployment: Apply
    environment: 'Production'
    strategy:
      runOnce:
        deploy:
          steps:
          - task: TerraformInstaller@0
            inputs:
              terraformVersion: $(terraformVersion)
          
          - task: TerraformTaskV4@4
            displayName: 'Terraform Init'
            inputs:
              provider: 'azurerm'
              command: 'init'
              backendServiceArm: 'MyServiceConnection'
              backendAzureRmResourceGroupName: 'terraform-state-rg'
              backendAzureRmStorageAccountName: $(storageAccount)
              backendAzureRmContainerName: $(container)
              backendAzureRmKey: $(stateKey)
          
          - task: TerraformTaskV4@4
            displayName: 'Terraform Apply'
            inputs:
              provider: 'azurerm'
              command: 'apply'
              commandOptions: '-auto-approve -var-file="$(Build.SourcesDirectory)/terraform/variables/$(environment).tfvars"'
              environmentServiceNameAzureRM: 'MyServiceConnection'
```

---

## 5. Best Practices

### Branch Policies

```bash
# Configure comprehensive branch policies
# 1. Minimum reviewers
az repos policy branch create \
  --project "MyProject" \
  --repository-id <repo-id> \
  --branch main \
  --policy-type "Minimum number of reviewers" \
  --settings '{
    "minimumApproverCount": 2,
    "creatorVoteCounts": false,
    "allowDownvotes": false,
    "resetOnSourcePush": true
  }'

# 2. Build validation
az repos policy build create \
  --project "MyProject" \
  --repository-id <repo-id> \
  --branch main \
  --build-definition-id <definition-id> \
  --display-name "Build Validation" \
  --enabled true \
  --manual-queue-only false \
  --queue-on-source-update-only true \
  --valid-duration 720

# 3. Required reviewers for specific paths
az repos policy required-reviewer create \
  --project "MyProject" \
  --repository-id <repo-id> \
  --branch main \
  --enabled true \
  --blocking true \
  --settings '{
    "requiredReviewerIds": ["<security-group-id>"],
    "message": "Security team review required for infrastructure changes",
    "scope": [{"path": "/infrastructure/*", "repositoryId": null}]
  }'

# 4. Work item linking
az repos policy work-item-linking create \
  --project "MyProject" \
  --repository-id <repo-id> \
  --branch main \
  --enabled true \
  --blocking true

# 5. Comment resolution
az repos policy comment-required create \
  --project "MyProject" \
  --repository-id <repo-id> \
  --branch main \
  --enabled true \
  --blocking true
```

### Security Scanning Integration

```yaml
# SonarCloud integration
- task: SonarCloudPrepare@1
  inputs:
    SonarCloud: 'SonarCloud'
    organization: 'myorg'
    scannerMode: 'MSBuild'
    projectKey: 'my-project'
    projectName: 'My Project'
    extraProperties: |
      sonar.exclusions=**/bin/**,**/obj/**
      sonar.coverage.exclusions=**/Tests/**

# Run analysis
- task: SonarCloudAnalyze@1

# Publish results
- task: SonarCloudPublish@1
  inputs:
    pollingTimeoutSec: '300'

# OWASP Dependency Check
- task: dependency-check-build-task@6
  inputs:
    projectName: 'My Project'
    scanPath: '$(Build.SourcesDirectory)'
    format: 'HTML'
    failOnCVSS: '7'

# Snyk security scan
- task: SnykSecurityScan@1
  inputs:
    serviceConnectionEndpoint: 'SnykConnection'
    testType: 'app'
    monitorWhen: 'always'
    failOnIssues: true

# Trivy container scan
- task: Docker@2
  inputs:
    command: 'build'
    dockerfile: 'Dockerfile'
    tags: 'scan-target:latest'

- script: |
    docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
      aquasec/trivy:latest image --exit-code 1 --severity HIGH,CRITICAL scan-target:latest
  displayName: 'Trivy Container Scan'
```

### Secret Management

```yaml
# Pipeline structure for secret management
variables:
- group: 'NonSecretVariables'
- group: 'SecretVariables'  # Key Vault linked variable group

stages:
- stage: Build
  jobs:
  - job: Build
    steps:
    - task: AzureKeyVault@2
      inputs:
        azureSubscription: 'MyServiceConnection'
        KeyVaultName: 'my-keyvault'
        SecretsFilter: 'DatabasePassword,ApiKey'
      name: GetSecrets

    - script: |
        echo "Using secrets..."
        # Never echo secrets directly
      env:
        DB_PASSWORD: $(DatabasePassword)
        API_KEY: $(ApiKey)

# Azure Key Vault linked variable group (created via CLI or UI)
# az pipelines variable-group create --name "SecretVariables" --project "MyProject" --authorize true --keyvault "my-keyvault" --secrets "DatabasePassword,ApiKey"
```

### CI/CD Strategies

```yaml
# Feature branch workflow
trigger:
  branches:
    include:
      - main
      - release/*
  paths:
    exclude:
      - docs/*
      - README.md

pr:
  branches:
    include:
      - main
  paths:
    include:
      - src/*

# Semantic versioning pipeline
variables:
  major: 1
  minor: $[counter(variables['major'], 0)]
  patch: $[counter(format('{0}.{1}', variables['major'], variables['minor']), 0)]
  version: $(major).$(minor).$(patch)

stages:
- stage: Build
  jobs:
  - job: Build
    steps:
    - script: |
        echo "##vso[build.updatebuildnumber]$(version)"
    - script: dotnet build -p:Version=$(version)
```

### AKS Deployment Pipeline

```yaml
trigger:
  - main

resources:
  repositories:
  - repository: templates
    type: git
    name: 'Pipelines/Templates'

variables:
  imageRepository: 'myapp'
  dockerfilePath: 'Dockerfile'
  tag: '$(Build.BuildId)'
  k8sNamespace: 'default'

stages:
- stage: Build
  displayName: 'Build and Push'
  jobs:
  - job: Build
    displayName: 'Build Docker Image'
    pool:
      vmImage: 'ubuntu-latest'
    steps:
    - task: Docker@2
      displayName: 'Build and Push to ACR'
      inputs:
        containerRegistry: 'MyAcrConnection'
        repository: $(imageRepository)
        command: 'buildAndPush'
        Dockerfile: $(dockerfilePath)
        tags: |
          $(tag)
          latest

- stage: Deploy
  displayName: 'Deploy to AKS'
  dependsOn: Build
  condition: succeeded()
  jobs:
  - deployment: Deploy
    displayName: 'Deploy to AKS'
    environment: 'Production.myakscluster'
    strategy:
      runOnce:
        deploy:
          steps:
          - task: KubernetesManifest@1
            displayName: 'Create namespace'
            inputs:
              action: 'createSecrets'
              kubernetesServiceConnection: 'MyAksConnection'
              namespace: $(k8sNamespace)
              secretType: 'dockerRegistry'
              secretName: 'acr-secret'
              dockerRegistryEndpoint: 'MyAcrConnection'

          - task: KubernetesManifest@1
            displayName: 'Bake and Deploy'
            inputs:
              action: 'deploy'
              kubernetesServiceConnection: 'MyAksConnection'
              namespace: $(k8sNamespace)
              manifests: |
                $(Pipeline.Workspace)/manifests/deployment.yml
                $(Pipeline.Workspace)/manifests/service.yml
                $(Pipeline.Workspace)/manifests/ingress.yml
              containers: 'myacr.azurecr.io/$(imageRepository):$(tag)'

          - task: KubernetesManifest@1
            displayName: 'Verify Deployment'
            inputs:
              action: 'deploy'
              kubernetesServiceConnection: 'MyAksConnection'
              namespace: $(k8sNamespace)
              manifests: |
                $(Pipeline.Workspace)/manifests/deployment.yml
              rolloutStatusTimeout: '300s'
```

---

## 6. Common Workflows

### Create New Project with Full CI/CD

```bash
#!/bin/bash
# Setup complete Azure DevOps project

ORG="https://dev.azure.com/myorg"
PROJECT="MyNewProject"
REPO="MyApp"
SERVICE_CONNECTION="Azure-Connection"

# Create project
az devops project create \
  --name "$PROJECT" \
  --organization "$ORG" \
  --visibility private \
  --source-control git \
  --process Agile

# Create repository
az repos create \
  --name "$REPO" \
  --project "$PROJECT" \
  --organization "$ORG"

# Create variable groups
az pipelines variable-group create \
  --name "SharedVariables" \
  --project "$PROJECT" \
  --organization "$ORG" \
  --variables environment=development region=eastus \
  --authorize true

# Create service connection
az devops service-endpoint azurerm create \
  --name "$SERVICE_CONNECTION" \
  --project "$PROJECT" \
  --organization "$ORG" \
  --azure-rm-service-principal-id $SP_ID \
  --azure-rm-subscription-id $SUB_ID \
  --azure-rm-subscription-name $SUB_NAME \
  --azure-rm-tenant-id $TENANT_ID

# Create build pipeline
az pipelines create \
  --name "CI-Pipeline" \
  --project "$PROJECT" \
  --organization "$ORG" \
  --repository "$REPO" \
  --repository-type tfsgit \
  --branch main \
  --yml-path azure-pipelines.yml

# Setup branch policies
REPO_ID=$(az repos show --repository "$REPO" --project "$PROJECT" --query id -o tsv)

az repos policy branch create \
  --project "$PROJECT" \
  --repository-id "$REPO_ID" \
  --branch main \
  --policy-type "Minimum number of reviewers" \
  --settings '{"minimumApproverCount": 2, "creatorVoteCounts": false}'
```

### GitHub Integration

```yaml
# Pipeline triggered by GitHub
resources:
  repositories:
  - repository: mygithub
    type: github
    name: myorg/myrepo
    endpoint: 'GitHubConnection'  # GitHub service connection
    ref: main

trigger: none  # Disable CI trigger, use resource trigger

stages:
- stage: Build
  jobs:
  - job: Build
    steps:
    - checkout: mygithub
    - script: |
        echo "Building from GitHub repo"
```

### Docker/ACR Workflow

```yaml
# Complete Docker workflow
variables:
  imageName: 'myapp'
  acrName: 'myacr'
  acrLoginServer: 'myacr.azurecr.io'

stages:
- stage: Build
  jobs:
  - job: BuildImage
    pool:
      vmImage: 'ubuntu-latest'
    steps:
    - task: Docker@2
      displayName: 'Login to ACR'
      inputs:
        command: login
        containerRegistry: 'MyAcrConnection'

    - task: Docker@2
      displayName: 'Build Image'
      inputs:
        repository: $(imageName)
        command: build
        Dockerfile: Dockerfile
        tags: |
          $(Build.BuildId)
          latest
        arguments: '--build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ')'

    - task: Docker@2
      displayName: 'Push Image'
      inputs:
        command: push
        repository: $(imageName)
        containerRegistry: 'MyAcrConnection'
        tags: |
          $(Build.BuildId)
          latest

    - task: Docker@2
      displayName: 'Run Trivy Scan'
      inputs:
        command: build
        repository: $(imageName)
        tags: 'scan'
        Dockerfile: Dockerfile
      enabled: false

    - script: |
        docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
          aquasec/trivy image --exit-code 1 --severity HIGH,CRITICAL \
          $(acrLoginServer)/$(imageName):$(Build.BuildId)
      displayName: 'Security Scan'
```

---

## 7. Troubleshooting

### Pipeline Failures

```yaml
# Debug pipeline issues
steps:
- script: |
    echo "Build ID: $(Build.BuildId)"
    echo "Build Number: $(Build.BuildNumber)"
    echo "Source Branch: $(Build.SourceBranch)"
    echo "Source Version: $(Build.SourceVersion)"
    env | sort
  displayName: 'Debug Environment Variables'

- script: |
    ls -la $(Build.SourcesDirectory)
    find $(Build.SourcesDirectory) -type f -name "*.yml" | head -20
  displayName: 'Debug Source Directory'

# Enable system.debug for detailed logging
variables:
  system.debug: true
```

### Common Error Solutions

| Error | Solution |
|-------|----------|
| `No hosted parallelism has been purchased` | Request free parallelism or purchase agents |
| `The term 'az' is not recognized` | Install Azure CLI in pipeline: `UsePythonVersion@0` then `pip install azure-cli` |
| `Service connection not found` | Verify exact name match, check permissions |
| `Unable to find secret` | Check Key Vault permissions, verify secret name |
| `Docker build failed` | Check Dockerfile syntax, verify base image availability |
| `Kubernetes deployment timeout` | Increase `rolloutStatusTimeout`, check pod logs |
| `Permission denied` | Verify service principal has required RBAC roles |

### Diagnostic Commands

```bash
# Check service principal permissions
az role assignment list --assignee <app-id> --output table

# Test service connection
az devops service-endpoint show --id <connection-id> --project "MyProject"

# Check pipeline permissions
az pipelines show --name "MyPipeline" --project "MyProject" --query "permissions"

# View agent capabilities
az pipelines agent show --pool-id <pool-id> --agent-id <agent-id>

# Check recent failures
az pipelines runs list --project "MyProject" --result failed --top 10
```

---

## 8. References

### Official Documentation
- [Azure DevOps Documentation](https://learn.microsoft.com/en-us/azure/devops/)
- [Azure CLI Reference](https://learn.microsoft.com/en-us/cli/azure/)
- [Azure DevOps CLI](https://learn.microsoft.com/en-us/azure/devops/cli/)
- [YAML Schema Reference](https://learn.microsoft.com/en-us/azure/devops/pipelines/yaml-schema/)
- [Bicep Documentation](https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/)
- [Terraform Azure Provider](https://registry.terraform.io/providers/hashicorp/azurerm/)

### Task References
- [Azure Pipelines Tasks](https://learn.microsoft.com/en-us/azure/devops/pipelines/tasks/)
- [Marketplace Extensions](https://marketplace.visualstudio.com/search?term=devops&target=AzureDevOps&category=All%20categories)

### Best Practices
- [Azure DevOps Best Practices](https://learn.microsoft.com/en-us/azure/devops/boards/best-practices-github)
- [Security Best Practices](https://learn.microsoft.com/en-us/azure/devops/organizations/security/security-best-practices)
- [Pipeline Security](https://learn.microsoft.com/en-us/azure/devops/pipelines/security/secure-pipelines)

### Tools
- [Azure DevOps Demo Generator](https://azuredevopsdemogenerator.azurewebsites.net/)
- [YAML Pipeline Designer](https://azuredevopsdemogenerator.azurewebsites.net/)
- [Bicep Playground](https://bicepdemo.z22.web.core.windows.net/)
