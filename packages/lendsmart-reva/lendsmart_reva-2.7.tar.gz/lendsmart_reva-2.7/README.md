Reva CLI
==========
![image](https://user-images.githubusercontent.com/1402479/200783457-550bf8bc-4bc8-4571-b995-829bc2f9b2b1.png)



The Reva CLI is used to manage Lendsmart deployment from the command line. 

[![PyPI](https://img.shields.io/pypi/v/lendsmart-reva.svg)](https://pypi.python.org/pypi/lendsmart-reva)
[![PyPI](https://img.shields.io/pypi/pyversions/lendsmart-reva.svg)](https://pypi.python.org/pypi/lendsmart-reva)

The primary intent is:

- mirror prod and QA
- make the deploys smooth with no manual intervention.


Overview
========

The goals of this project is to make deployments more flexible, and make the deployments faster.

Installation
============

```
pip install lendmart_reva
```

Configuration
=============

### Step 1: export

```

# Here the home is the root user home directory
export LENDSMART_REVA_HOME=$HOME (or)

# Here the home is the directory `/home/makesh`
export LENDSMART_REVA_HOME="/home/makesh"

# Here the ui home is the path to where the code of ui exists
export LENDSMART_REVA_UI_HOME='/home/makesh/ui'

# Here the ui home is the path to where the code of worklet exists
export LENDSMART_REVA_WORKLET_HOME="/home/makesh/worklet"

```

### Step 3: mkdir reva

```

cd $LENDSMART_REVA_HOME

mkdir $LENDSMART_REVA_HOME/reva

```

### Step 3: reva.conf 

Copy the conf file to location `$LENDSMART_REVA_HOME/reva/config.json`

```json
{
  "dev": {
    "api_root": "https://devapi.lendsmart.ai/api/v1",
    "application_graphql_endpoint": "https://devappgraphql.lendsmart.ai/v1/graphql",
    "application_graphql_auth_token": "",
    "lendsmart_access_token": "<dev-lendsmart-access-token>"
  },
  "prod": {
    "api_root": "https://apiprod.lendsmart.ai/api/v1",
    "application_graphql_endpoint": "https://devappgraphql.lendsmart.ai/v1/graphql",
    "application_graphql_auth_token": "",
    "lendsmart_access_token": "<prod-lendsmart-access-token>"
  }
}
```

💁 Please update the aut_token, namespace and lendsmart_access_token for the appropriate environments. This is purposefully left out for security reasons.


<!-- commands -->
# Command Topics

* [`reva namespaces`](docs/namespaces.md) - manage namespaces on Lendsmart
* [`reva workflows`](docs/workflow.md) - manage workflow configuration
* [`reva loanproducts`](docs/loanproducts.md) - manage loanproducts configuration
* [`reva sitesettings`](docs/sitesettings.md) - manage sitesettings configuration
* [`reva worklet`](docs/worklet.md) - manage worklet configuration



<!-- commandsstop -->

References
==========

> [CLI](https://github.com/ceph/ceph-deploy)
> [Configuration conf/reva.py](https://github.com/ceph/ceph-deploy/blob/a16316fc4dd364135b11226df42d9df65c0c60a2/ceph_deploy/conf/ceph.py)
