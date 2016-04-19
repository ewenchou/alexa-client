"""This tests the `ask_multiple()` method which loads three pre-generated
audio files in the `tests` directory and sends them to AVS in parallel.
"""
from alexa_client import AlexaClient
import os

TESTS_PATH = os.path.dirname(os.path.realpath(__file__))


def main():
    alexa = AlexaClient()
    inputs = []
    for i in range(1, 4):
        inputs.append((
            '{}/{}.wav'.format(TESTS_PATH, i),
            '/tmp/test_multiple_{}.mp3'.format(i)
        ))
    results = alexa.ask_multiple(inputs)
    print "Responses are saved to: "
    for r in results:
        print r


if __name__ == '__main__':
    main()
