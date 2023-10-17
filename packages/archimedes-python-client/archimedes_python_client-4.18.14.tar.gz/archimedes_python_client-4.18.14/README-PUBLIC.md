# archimedes-python-client

`archimedes` is the python sdk for accessing Optimeering data. This document outlines the setup of 
environment, authentication and general usage of the python client to fetch RK within day data using python.

## Setting up the environment

We will be using [venv](https://docs.python.org/3/library/venv.html) to manage the virtual environment in this example.

### Creating a virtual environment.

```bash
python3 -m venv .venv
```

This will create a directory named `.venv` where all the dependencies will be installed.

### Activating the virtual environment

```bash
source ./.venv/bin/activate # linux/macOS
.venv\Scripts\activate.bat # Windows cmd
.\.venv\Scripts\Activate.ps1 # Windows PowerShell
```

### Installing`archimedes-python-client`

```bash
python3 -m pip install archimedes-python-client
```

## Authentication

**For local development:**

For local development, the python client can use user authentication. The users are can be authenticated using the 
archimedes command line tool `arcl`.

```bash
python3 -m pip install arcl

arcl auth login # then, follow the instructions to login with your Microsoft account
```

Once the user is logged in, the archimedes login information will be stored in your `~/.archimedes` directory and all 
the scripts and applications running as the same user are able to authenticate to the API automatically when using the 
`archimedes-python-client`.

**For deployed applications:**

The python client uses the following fields in environment variable for authentication of the client.

1. `AZURE_AD_TENANT_ID`  **Provided by Optimeering AS**
2. `AZURE_AD_APP_ID` **Provided by Optimeering AS**
3. `AZURE_AD_APP_CLIENT_CREDENTIAL` **Provided by Optimeering AS**
4. `USE_APP_AUTHENTICATION` **Set to True**

As long as these variables have been set up as environment variables, any python script that invokes methods in 
`archimedes` will automatically use the values in the environment variables for authentication.

## Example Code

Below is a code sample that invokes an `archimedes` method.

```python
#import os
import archimedes

# The following environment variables are only needed for deployed applications.
# These would ideally be set in the app runtime environment and not necessarily in 
# python code
# os.environ["AZURE_AD_TENANT_ID"] = "***azure_ad_tenant_id***"
# os.environ["AZURE_AD_APP_ID"] = "***azure_ad_client_id***"
# os.environ["AZURE_AD_APP_CLIENT_CREDENTIAL"] = "***secret***"
# os.environ["USE_APP_AUTHENTICATION"] = "true"

data = archimedes.rk_within_day.directions(
    start="2023-01-01 00:00:00+0000",
    price_area="NO1",
    end="2023-01-01 01:00:00+0000",
    ref_dt="2022-12-31 23:00:00+0000"
)
print(data)
```

The sample code prints the RK within day directions probability for provided constraints to the console.
