# Dingman API Server

## Dependencies

| Dependency | Version |
|------------|---------|
| Python     | >= `3.7`|
| Dingman    |         |
## Setup

```bash
# Create a new Python3 virtual environment
python3 -m venv env
source env/bin/activate

# Upgrade pip & install requirements
pip3 install --upgrade pip
pip3 install -r requirements.txt

# Install gsssdk-python (i.e Dingman Python SDK)
pip3 install ./pkgs/dingman-0.0.4.tar.gz

# Alternatively, to fetch the latest version of the SDK:
# 1. Download https://sysrepo.byted.org/savanna/gsssdk-python
# 2. Run the install.sh to install Dingman SDK
```
    
## Run

```bash
./scripts/start.sh
```
> Ensure that Dingman gRPC server is already running at the specified port before starting the API server.

## Testing

We use pytest for testing

```bash
python3 -m pytest -s

# Generate code coverage
python3 -m pytest -s --cov=app --cov-report html
```