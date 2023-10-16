import json
import pickle
import time
import requests
import platform
import traceback
import pandas as pd
from qtc.consts.enums import DataTransmissionProtocol
from qtc.ext.logging import set_logger
logger = set_logger()


def get_auth(username=None, password=None):
    if username is not None or password is not None:
        from requests_ntlm import HttpNtlmAuth
        auth = HttpNtlmAuth(username=username, password=password)
    else:
        if platform.system() == 'Windows':
            from requests_negotiate_sspi import HttpNegotiateAuth
            return HttpNegotiateAuth()
        else:
            from requests_kerberos import HTTPKerberosAuth, OPTIONAL
            return HTTPKerberosAuth(mutual_authentication=OPTIONAL)

    return auth


def _process_request(request_url, is_post, body=None,
                     username=None, password=None,
                     data_transmission_protocol='JSON'):
    # import time
    # start_time = time.time()

    with requests.Session() as session:
        session.auth = get_auth(username=username, password=password)

        if is_post:
            response = session.post(request_url, json=body, timeout=300)
        else:
            response = session.get(request_url, params=body, timeout=300)

        # print(f"Request roundtrip time={time.time()-start_time} @ request_url={request_url}")
        # start_time = time.time()

        if not response.ok:
            url_format = lambda x: x if len(x)<100 else x[0:100]+'...'
            logger.error(f'Failed with status code {response.status_code} for '
                         f'URL: {url_format(request_url)} with Body: {url_format(str(body))}')
            response.raise_for_status()
            return None

        if data_transmission_protocol is None:
            return response

        if isinstance(data_transmission_protocol, str):
            data_transmission_protocol = DataTransmissionProtocol.retrieve(data_transmission_protocol)

        if data_transmission_protocol==DataTransmissionProtocol.JSON:
            data = json.loads(response.content.decode('utf-8'))
            # print(f"JSON parsing time = {time.time()-start_time} @ request_url={request_url}")
        elif data_transmission_protocol==DataTransmissionProtocol.PICKLE:
            data = pickle.loads(response.content)
            # print(f"pickle.loads elapse time = {time.time()-start_time} @ request_url={request_url}")
        elif data_transmission_protocol==DataTransmissionProtocol.TXT:
            data = response.content.decode('utf-8')

    return data


def process_request(request_url, is_post, body=None,
                    username=None, password=None,
                    data_transmission_protocol='JSON',
                    max_retry=0, retry_interval=60):
    data = None
    n_try = 0
    while data is None:
        try:
            data = _process_request(request_url=request_url, is_post=is_post, body=body,
                                    username=username, password=password,
                                    data_transmission_protocol=data_transmission_protocol)
        except:
            traceback.print_exc()

        n_try += 1
        if n_try>max_retry:
            break

        logger.warn(f'Sleeping for {retry_interval} seconds before {n_try} retry ...')
        time.sleep(retry_interval)

    if data is None and max_retry>0:
        logger.error(f'Failed to get data after {max_retry} retries !')

    return data


def process_request_json2df(request_url, is_post, body=None,
                            username=None, password=None,
                            max_retry=0, retry_interval=60):
    data = process_request(request_url=request_url, is_post=is_post, body=body,
                           username=username, password=password,
                           data_transmission_protocol=DataTransmissionProtocol.JSON,
                           max_retry=max_retry, retry_interval=retry_interval)
    if data is None:
        return None

    try:
        data = pd.DataFrame.from_records(data['Data']['Records'],
                                         columns=data['Data']['Fields'])
    except:
        try:
            data = pd.DataFrame(data['Data'])
        except:
            try:
                data = pd.DataFrame(data)
            except:
                logger.error(f"Failed to parse JSON data to pd.DataFrame!\n{data}")

    return data
