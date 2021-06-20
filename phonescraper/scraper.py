import asyncio
import json
import logging
import os
import time
from collections import defaultdict
from datetime import datetime

from requests.exceptions import ConnectionError
from requests.exceptions import Timeout
from requests.exceptions import TooManyRedirects
from termcolor import colored
from torpy.cell_socket import TorSocketConnectError
from torpy.circuit import CellTimeoutError
from torpy.circuit import CircuitExtendError
from torpy.http.requests import TorRequests

import helpers


class Phone:

    recent_list = list()

    def extract_phone_numbers(self, phone_list, max_age):
        """Extract the phone numbers and the dates they have been added"""
        numbers = defaultdict()
        for num in phone_list['numbers']:
            numbers[num['full_number']] = num['maxdate']

        numbers = dict(sorted(numbers.items(), key=lambda item: item[1]))

        print("Phone numbers printed to phone_list_output file.")
        print("\n\nSelect a number and check SMS codes on https://onlinesim.ru/en\nDon't forget to use TOR.\n")
        print(f"\nThe phone numbers that have most recently been added are:\n")
        cmp_time = datetime.now()
        out_list = list()
        for k, v in reversed(numbers.items()):
            v_time = datetime.strptime(v, '%Y-%m-%d %H:%M:%S')
            v = datetime.now() - datetime.strptime(v, '%Y-%m-%d %H:%M:%S')
            diff = cmp_time - v_time
            out_msg = f"{k} added {v} hours ago."
            out_list.append(out_msg)
            if diff.total_seconds() < max_age * 60:
                # within the last x minutes
                self.recent_list.append(out_msg)
                print(colored(out_msg, 'green'))
            else:
                print(out_msg)

        # returns list of phone numbers
        return out_list


def initialise():
    """load the domain names from sites.json"""
    this_dir = os.path.dirname(__file__)
    json_path = os.path.join(this_dir, 'sites.json')
    try:
        with open(json_path) as f:
            s = json.load(f)
    except UnboundLocalError or FileNotFoundError:
        logging.exception("Initialisation failed.")

    return s


async def request(s, max_age):
    """scrape the sites listed in sites.json using the TOR network (new IP for every cycle)"""
    try:
        with TorRequests() as tor_requests:
            print("Building TOR circuit")
            with tor_requests.get_session() as session:
                ip = session.get("http://httpbin.org/ip").json()
                print("IP Address used: ", ip['origin'])
                if s == 'onlinesim.ru' or s == 'onlinesim.io':
                    # api calls for onlinesim.io
                    phone_list = await get_free_phone_list(session)
                    phone_list = json.loads(phone_list)

                    phone = Phone()
                    out_list = phone.extract_phone_numbers(phone_list, max_age)
                    helpers.print_to_file(out_list)

                    message_list = await get_free_message_list(session, phone_list['numbers'][0]['full_number'])
                    message_list = json.loads(message_list)
                    # print(message_list)
                    if not 'data' in message_list['messages'] or len(message_list['messages']['data']) == 0:
                        logging.debug('GetFreeMessageList API call currently unavailable.')
                else:
                    # other site
                    r = session.get("https://" + s)
                    print(r.text)

    except (ConnectionError, Timeout, TimeoutError, CircuitExtendError, CellTimeoutError):
        if helpers.ping(s):
            print(f"Connection Error. {s} is not reachable. Please check your connection.")
            logging.exception(f"Connection Error. {s} is not reachable. Please check your connection.")
        else:
            print(f"Connection Error. {s} seems to be down. Skipping site...")
            logging.exception(f"Connection Error. {s} seems to be down. Skipping site...")
    except TorSocketConnectError:
        print("Network unreachable.")
        logging.exception("Network unreachable.")
    except TooManyRedirects:
        print("Too many redirects error.")
        logging.exception("Too many redirects error.")

    return out_list


async def get_free_phone_list(session):
    """Get the phone number and the phone number age with this API call"""
    data = session.get(
        "https://" +
        "onlinesim.io/" +
        "api/getFreePhoneList")

    return data.text


async def get_free_message_list(session, phone_number):
    """Get the message list for a certain phone number with this API call"""
    data = session.get(
        "https://" +
        "onlinesim.io/" +
        "api/getFreeMessageList?" +
        "cpage=1&phone=" +
        phone_number)

    return data.text


async def main():
    logging.basicConfig(filename='phonescraper.log',
                        filemode='w',
                        level=logging.DEBUG,
                        format='%(asctime)s - %(message)s',
                        datefmt='%d-%b-%y %H:%M:%S')
    logging.info('Started')
    args = helpers.Args()
    arg_dict = args.arg_dict
    sites = initialise()

    # repeat_flag
    if 'repeat' in list(arg_dict):
        repeat = arg_dict['repeat']
    else:
        # default is 10 minutes
        repeat = 10

    # max_age flag
    if 'maxage' in list(arg_dict):
        max_age = arg_dict['maxage']
    else:
        # default is 10 minutes
        max_age = 10

    while 1:
        coroutines = [request(sites[site], max_age) for site in sites]
        await asyncio.gather(*coroutines)
        phone_list = Phone.recent_list

        # send email if new phone number has been found within the last x minutes
        if 'email' in list(arg_dict) and len(phone_list) > 0:
            print("Email flag set.")
            email = helpers.Email(arg_dict['email'], phone_list)
            email.establish_connection()

        print(f"Repeating in {int(repeat)} minute(s)...\n\n")
        time.sleep(repeat * 60)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
