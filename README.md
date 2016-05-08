# alexa-client

Python client for Amazon's Alexa Voice Service (AVS). Read about it on my [blog post](http://ewenchou.github.io/blog/2016/03/20/alexa-voice-service/).

For more information about AVS, visit [Amazon's Getting Started Guide](http://amzn.to/1Uui0QW)

## Installation

    python setup.py install

## Configuration

A sample configuration file is available in `config/alexa_client.ini`. You need to set values for your Alexa Voice Service variables before you can use `alexa_client`.

Alexa client will look for the configuration file in the following paths:

* `config/alexa_client.ini` (i.e. local path where alexa_client is installed)

* `/opt/alexa-client/config/alexa_client.ini`

* `~/.alexa_client.ini`

## Tests

Some sample tests are available in the `test` directory. Once installed and configured, you can run them to check if everything is working.

* Test a single request: `python test/test_ask.py`

* Test multiple concurrent requests: `python test/test_multiple.py`
