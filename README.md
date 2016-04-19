# alexa-client

Python client for Amazon's Alexa Voice Service (AVS). Read about it on my [blog post](http://ewenchou.github.io/blog/2016/03/20/alexa-voice-service/).

For more information about AVS, visit [Amazon's Getting Started Guide](http://amzn.to/1Uui0QW)

## Installation

    python setup.py install

## Configuration

Copy the sample config file from `config/alexa_client.ini` to your home directory as `~/.alexa_client.ini`.

    cp config/alexa_client.ini ~/.alexa_client.ini

Edit the file and add your own Alexa Voice Service values to the `[avs]` section.

## Tests

Some sample tests are available in the `test` directory. Once installed and configured, you can run them to check if everything is working.

* Test a single request: `python test/test_ask.py`

* Test multiple concurrent requests: `python test/test_multiple.py`
