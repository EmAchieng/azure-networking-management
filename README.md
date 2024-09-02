# Azure Networking Management

## Overview

Using Python to provide a modularized management of Azure network. It simplifies tasks such as creating Virtual Networks (VNets), deploying Virtual Machines (VMs), managing Network Security Groups (NSGs), and more.

## Modularity

### Architecture
- **Azure VNet Module:** Handles Virtual Network (VNet) creation and management..
- **Azure VM Module:** Manages Virtual Machine (VM) deployment and configuration.
- **Azure NSG Module:** Facilitates Network Security Group (NSG) creation and rules management.
- **Azure Subnet Module:** Supports subnet creation and configuration within VNets.
- **Azure Virtual Network Gateway (VNG) Module:** Provides functionality for managing virtual network gateways for secure network connections.
- **Azure Route Table Module: ** Manages route tables and associations with subnets for network traffic routing.
- **Azure Scale Set Module:** Facilitates creation and management of Virtual Machine Scale Sets for scalable VM deployment.

### Benefits of Modularity

1. **Code Organization:** Each module encapsulates logic specific to its Azure resource, enhancing code organization and readability.

2. **Reusability:** Modules can be reused across projects or within the same project for different infrastructure components, promoting code reusability.

3. **Scalability:** Easily add new modules for additional AWS resources or modify existing ones without impacting other parts of the SDK.

### Prerequisites

Before installing the SDK, ensure:
- Python 3.9+ is installed on your system.
- AWS credentials are configured:
  - Either through environment variables (AZURE_CLIENT_ID, AZURE_SECRET, and AZURE_SUBSCRIPTION_ID),
  - Or using Azure CLI configuration (az login).
    
# Pip
### Installation Guide 
   ```bash
   python3 -m venv path/to/venv
source path/to/venv/bin/activate
python3 -m pip install -r requirements.txt
   ```
### Running the module files
  ```bash
   python3 modules/main.py
```
### Testing 
   ```bash
   python3 pip install pytest
   pytest test/

   ```

# Docker
### Installation Guide 
  ```bash
docker build -t azure-image .
```

### Running 
  ```bash
   docker run -p 4000:80 azure-image
```

### Testing 
   ```bash
   docker build -t azure-test-image .
   docker run azure-test-image
   ```

# Poetry
### Installation Guide 
 ```bash
   curl -sSL https://install.python-poetry.org | python3 -
```

  ```bash
poetry init
```
  ```bash
poetry install
```
### Running 
  ```bash
   poetry run python modules/main.py
```

### Testing 
   ```bash
   poetry add --dev pytest
   poetry run pytest
   ```
   
