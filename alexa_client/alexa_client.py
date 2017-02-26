"""
Python client class for interacting with Amazon Alexa Voice Service (AVS).
"""
import settings
import requests
import json
import uuid
import os
import re
from requests_futures.sessions import FuturesSession


class AlexaClient(object):
    def __init__(self, token=None, client_id=settings.CLIENT_ID,
            client_secret=settings.CLIENT_SECRET,
            refresh_token=settings.REFRESH_TOKEN,
            temp_dir=settings.TEMP_DIR, *args, **kwargs):
        self._token = token
        self._client_id = client_id
        self._client_secret = client_secret
        self._refresh_token = refresh_token
        self.temp_dir = temp_dir
        os.system("mkdir -p {}".format(self.temp_dir))

    def get_token(self, refresh=False):
        """Returns AVS access token.

        If first call, will send a request to AVS to obtain the token
        and save it for future use.

        Args:
            refresh (bool): If set to True, will send a request to AVS
                            to refresh the token even if one's saved.

        Returns:
            AVS access token (str)
        """
        # Return saved token if one exists.
        if self._token and not refresh:
            return self._token
        # Prepare request payload
        payload = {
            "client_id" : self._client_id,
            "client_secret" : self._client_secret,
            "refresh_token" : self._refresh_token,
            "grant_type" : "refresh_token"
        }
        url = "https://api.amazon.com/auth/o2/token"
        res = requests.post(url, data=payload)
        res_json = json.loads(res.text)
        self._token = res_json['access_token']
        return self._token

    def get_request_params(self):
        """Returns AVS request parameters

        Returns a tuple of parameters needed for an AVS request.

        Returns:
            Tuple (url, headers, request_data) where,

               url (str): Request URL
               headers (dict): Request headers
               request_data (dict): Predefined request payload parameters
        """
        url = "https://access-alexa-na.amazon.com/v1"
        url += "/avs/speechrecognizer/recognize"
        headers = {'Authorization' : 'Bearer %s' % self.get_token()}
        request_data = {
            "messageHeader": {
                "deviceContext": [
                    {
                        "name": "playbackState",
                        "namespace": "AudioPlayer",
                        "payload": {
                            "streamId": "",
                            "offsetInMilliseconds": "0",
                            "playerActivity": "IDLE"
                        }
                    }
                ]
            },
            "messageBody": {
                "profile": "alexa-close-talk",
                "locale": "en-us",
                "format": "audio/L16; rate=16000; channels=1"
            }
        }
        return url, headers, request_data

    def save_response_audio(self, res, save_to=None):
        """Saves the audio from AVS response to a file

        Parses the AVS response object and saves the audio to a file.

        Args:
            res (requests.Response): Response object from request.
            save_to (str): Filename including path for saving the
                           audio. If `None` a random filename will
                           be used and saved in the temporary directory.

        Returns:
            Path (str) to where the audio file is saved.
        """
        if not save_to:
            save_to = "{}/{}.mp3".format(self.temp_dir, uuid.uuid4())
        with open(save_to, 'wb') as f:
            if res.status_code == requests.codes.ok:
                for v in res.headers['content-type'].split(";"):
                    if re.match('.*boundary.*', v):
                        boundary =  v.split("=")[1]
                response_data = res.content.split(boundary)
                audio = None
                for d in response_data:
                    if (len(d) >= 1024):
                        audio = d.split('\r\n\r\n')[1].rstrip('--')
                if audio is None:
                    raise RuntimeError("Failed to save response audio")
                f.write(audio)
                return save_to
            # Raise exception for the HTTP status code
            print "AVS returned error: Status: {}, Text: {}".format(
                res.status_code, res.text)
            res.raise_for_status()

    def ask(self, audio_file, save_to=None):
        """
        Send a command to Alexa

        Sends a single command to AVS.

        Args:
            audio_file (str): File path to the command audio file.
            save_to (str): File path to save the audio response (mp3).

        Returns:
            File path for the response audio file (str).
        """
        with open(audio_file) as in_f:
            url, headers, request_data = self.get_request_params()
            files = [
                (
                    'file',
                    (
                        'request', json.dumps(request_data),
                        'application/json; charset=UTF-8',
                    )
                ),
                ('file', ('audio', in_f, 'audio/L16; rate=16000; channels=1'))
            ]
            res = requests.post(url, headers=headers, files=files)
            # Check for HTTP 403
            if res.status_code == 403:
                # Try to refresh auth token
                self.get_token(refresh=True)
                # Refresh headers
                url, headers, request_data = self.get_request_params()
                # Resend request
                res = requests.post(url, headers=headers, files=files)
            return self.save_response_audio(res, save_to)

    def ask_multiple(self, input_list):
        """Sends multiple requests to AVS concurrently.

        Args:
            input_list (list): A list of input audio filenames to send
                               to AVS. The list elements can also be a
                               tuple, (in_filename, out_filename) to
                               specify where to save the response audio.
                               Otherwise the responses will be saved to
                               the temporary directory.

        Returns:
            List of paths where the responses were saved.
        """
        session = FuturesSession(max_workers=len(input_list))
        # Keep a list of file handlers to close. The input file handlers
        # need to be kept open while requests_futures is sending the
        # requests concurrently in the background.
        files_to_close = []
        # List of saved files to return
        saved_filenames = []
        # List of future tuples, (future, output_filename)
        futures = []

        try:
            # Refresh token to prevent HTTP 403
            self.get_token(refresh=True)
            for inp in input_list:
                # Check if input is a tuple
                if isinstance(inp, tuple):
                    name_in = inp[0]
                    name_out = inp[1]
                else:
                    name_in = inp
                    name_out = None

                # Open the input file
                in_f = open(name_in)
                files_to_close.append(in_f)

                # Setup request parameters
                url, headers, request_data = self.get_request_params()
                files = [
                    (
                        'file',
                        (
                            'request', json.dumps(request_data),
                            'application/json; charset=UTF-8',
                        )
                    ),
                    (
                        'file',
                        ('audio', in_f, 'audio/L16; rate=16000; channels=1')
                    )
                ]

                # Use request_futures session to send the request
                future = session.post(url, headers=headers, files=files)
                futures.append((future, name_out))

            # Get the response from each future and save the audio
            for future, name_out in futures:
                res = future.result()
                save_to = self.save_response_audio(res, name_out)
                saved_filenames.append(save_to)
            return saved_filenames
        except Exception as e:
            print str(e)
        finally:
            # Close all file handlers
            for f in files_to_close:
                f.close()

    def clean(self):
        """
        Deletes all files and directories in the temporary directory.
        """
        os.system('rm -r {}/*'.format(self.temp_dir))
