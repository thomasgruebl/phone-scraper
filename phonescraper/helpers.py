import argparse
import base64
import logging
import os
import smtplib
import socket
import textwrap
from email.mime.text import MIMEText


def ping(dest: str):
    """Check if site is reachable"""
    global reachable
    domain = dest.split('/')[0]

    try:
        reachable = os.system("ping -c 1 " + domain)
    except:
        print("Ping error: ")
    finally:
        if reachable == 0:
            return True
        else:
            return False


def print_to_file(phone_list: list):
    """Print phone numbers to output file"""
    try:
        with open('../phone_list_output.txt', 'w') as f:
            for line in phone_list:
                f.writelines(line + '\n')
    except:
        logging.exception("Writing to output file failed.")
    logging.debug("Printed phone numbers to output file.")


class Args:
    arg_dict = {}

    def __init__(self):
        self.parse_args()

    def parse_args(self):
        parser = argparse.ArgumentParser(prog='scraper.py',
                                         allow_abbrev=True,
                                         formatter_class=argparse.RawDescriptionHelpFormatter,
                                         description=textwrap.dedent(''' \
                                         phone-scraper.
                                         --------------------------------
                                         Anonymously scrapes onlinesim.ru for new usable phone numbers.
                                         '''))

        parser.add_argument('-e', '--email',
                            type=str,
                            default=argparse.SUPPRESS,
                            help='add your email address to receive a notification when a new phone number appears.')

        parser.add_argument('-m', '--maxage',
                            type=int,
                            default=argparse.SUPPRESS,
                            help='pulls only phone numbers that are younger than the specified maximum age value in minutes.')

        parser.add_argument('-r', '--repeat',
                            type=int,
                            default=argparse.SUPPRESS,
                            help='specify the repetition interval in minutes for fetching phone numbers.')

        try:
            args = parser.parse_args()
            self.arg_dict = vars(args)
        except argparse.ArgumentError:
            logging.exception('Argument Error.')
            print('Argument Error.')
        except AttributeError:
            logging.exception('Attribute Error.')
            raise AttributeError

        if 'email' not in list(self.arg_dict):
            return 1


class Email:
    __sender = ""
    receiver = ""
    __port = 587

    def __init__(self, receiver, phone_list):
        self.receiver = receiver
        self.phone_list = phone_list

    def establish_connection(self):
        self.__sender = 'python.phonescraper@gmx.de'
        msg = self.__draft_email()

        msg['From'] = self.__sender
        msg['To'] = self.receiver

        try:
            with smtplib.SMTP('smtp.gmx.com', self.__port) as connection:
                connection.ehlo()
                connection.starttls()
                connection.ehlo()
                s = base64.b64decode('XkNPekkybGUxNSZNRlNoNjZweEIK').decode('ascii')
                s = s.rstrip("\n")
                connection.login(self.__sender, s)
                self.__send_email(connection, msg)
        except socket.gaierror:
            logging.exception('Mail server unreachable.')
            raise socket.gaierror

    def __draft_email(self):
        tidy_phone_list = ""
        for num in self.phone_list:
            tidy_phone_list += num + '\n'
        subject = "Python Phonescraper Notification"
        body = f"\nSelect a number and check SMS codes on https://onlinesim.ru/en\n\nDon't forget to use TOR.\n\n" \
               f"The following phone numbers have been recently added:\n\n{tidy_phone_list}"
        message = f"{subject}\n\n{body}"
        msg = MIMEText(message)

        self.phone_list.clear()
        del tidy_phone_list

        return msg

    def __send_email(self, connection, msg):
        connection.sendmail(msg['From'], msg['To'], msg.as_string())
        print("Sent email")
        logging.debug(f"Email sent from {self.__sender} to {self.receiver}")
