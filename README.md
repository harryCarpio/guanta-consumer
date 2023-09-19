## Install & Run

```sh
pip3 install --user pipenv
# pip3 install --upgrade pipenv
pipenv --python python3

pip3 install --user -e .
pip3 install .
ocds-reader --help
pip3 uninstall ocds-reader
```
### Dependencies 
To install pipreqs:
```sh
pip3 install pipreqs
```
Generate requirents.txt
```sh
pipreqs .
```
Install dependencies
```sh
cd ocds_reader
pip3 install -r requirements.txt
```
### References
* [Building a Command Line Tool with Python](https://www.pluralsight.com/cloud-guru/labs/aws/building-a-command-line-tool-with-python?utm_source=google&utm_medium=paid-search&utm_campaign=cloud-transformation&utm_term=ssi-global-acg-aws-dsa&utm_content=free-trial&gclid=CjwKCAjw2K6lBhBXEiwA5RjtCSuOIxRyrWwtBzhBucPF7ia2kHXvp_-HJVLGc6Qu3_8bFr4fhAsaBRoC91cQAvD_BwE)
* [Requirements.txt vs Setup.py in Python: Managing Dependencies](https://levelup.gitconnected.com/requirements-txt-vs-setup-py-in-python-a0e70313f50b#:~:text=Setup.py%20is%20a%20more,and%20even%20complex%20dependency%20structures.)



## Docker

### Env setup
```sh
# Create data directory
mkdir -p ~/mongo/data

# Create log directory
sudo mkdir -p /var/log/mongodb
```

```sh
# Run
docker-compose up -d

# Check running
docker ps

# Chcek data container
docker volume ls

# Stop container
docker-compose stop

# Shutdown db and delete containers (remove)
docker-compose down
```