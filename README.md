# Alexa Client

Python client for Amazon's Alexa Voice Service (AVS). Read about it on my [blog post](http://ewenchou.github.io/blog/2016/03/20/alexa-voice-service/).

For more information about AVS, visit [Amazon's Getting Started Guide](http://amzn.to/1Uui0QW)

## Installation

1. Clone this repository

  `git clone https://github.com/ewenchou/alexa-client.git`

2. Configure settings

  Set values for your Alexa Voice Service variables in `alexa_client/settings.py`

3. Install requirements

  `pip install -r requirements.txt`


4. Install alexa_client

  `python setup.py install`

## Tests

Some sample tests are available in the `test` directory. Once installed and configured, you can run them to check if everything is working.

* Test a single request: `python test/test_ask.py`

* Test multiple concurrent requests: `python test/test_multiple.py`
