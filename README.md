# 88 Chemin Splitwise Analyzer
An example Flask application to show the usage of Splitwise SDK

## Installation with Docker

Clone this repository

```bash
git clone https://github.com/88Chemin/splitwise-analyzer
cd splitwise-analyzer

```
## Register your application

Goto [Splitwise](https://secure.splitwise.com/oauth_clients) and register you application. Use the following -

- Homepage URL - http://localhost:5000 

- Callback URL - http://localhost:5000/authorize

Make note of Consumer Key and Consumer Secret

Create a config.py file in the root directory of the repo
```bash
touch config.py
vim config.py
```
The content of the file should be:
```text
consumer_key = 'Your Consumer Key'
consumer_secret = 'Your Secret Key'
```
Remember to replace 'Your Consumer Key' and 'Your Secret Key' with the consumer_key and the secret_key you obtained after registering your app on Splitwise.
## Run 
Execute the run script to build and run the container
```bash
./run splitwise_analyzer.sh
```
This will build the image and start the flask application which you can access in your browser at **0.0.0.0:5000**
Login to Splitwise and then head to **0.0.0.0:5000/analyze** to see the payment matrices.
## Installation 

This application is dependent on [Flask](http://flask.pocoo.org/) and [Splitwise](https://github.com/namaggarwal/splitwise) python packages. Install these python packages using the commands below:

```sh
git clone https://github.com/88Chemin/splitwise-analyzer
cd splitwise-analyzer
pip install -r requirements.txt
```

## Register your application

Goto [Splitwise](https://secure.splitwise.com/oauth_clients) and register you application. Use the following -

Homepage URL - http://localhost:5000 

Callback URL - http://localhost:5000/authorize

Make note of Consumer Key and Consumer Secret

## Set Configuraion

Open ```config.py``` and replace consumer_key and consumer_secret by the values you got after registering your application.
```text
consumer_key = 'Your Consumer Key'
consumer_secret = 'Your Secret Key'
```
## Run the application

Goto the cloned repository and type 

```python
python app.py
```

Goto http://localhost:5000/ on your browser.

## Contact
Contact naman (dot) aggarwal (at) yahoo (dot) com for any information.
Naman is the original author of Splitwise REST bindings for Python. Mayank built the analyzer on top of it.


