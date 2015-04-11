#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import requests
import json
from posixpath import basename
from requests.auth import HTTPBasicAuth

log = logging.getLogger(__name__)

# make external modules less noisy
logging.getLogger('requests').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)


def urljoin(*args):
    """
    Joins given arguments into a url. Trailing but not leading slashes are
    stripped for each argument.
    """

    return "/".join([str(x).rstrip('/') for x in args])


class LsmsException(Exception):
    """
    Exception class to indicate that something with the lsms api is
    not correct.

    The following member variables are available
    e.status_code
    e.url
    e.method
    e.data
    """
    pass


class Lsms(object):
    """
    Class to handle api calls to the lsmsd interface
    """

    def __init__(self, base_url, username=None, password=None):
        """ Creates a Lsms object"""
        self.base_url = base_url
        auth = None
        if username and password:
            auth = HTTPBasicAuth(username, password)

        self.s = requests.Session()
        self.s.headers['Content-Type'] = 'application/json'
        self.s.auth = auth

    def set_credentials(self, username, password):
        """ Set the username and password for the current session"""
        auth = HTTPBasicAuth(username, password)
        self.s.auth = auth

    def __api_call(self, url, method="get", data=None, to_json=True,
                   text_check=None):
        """ Make a call to the lsmsd api"""
        # TODO: Ugly implementation => make cleaner (dict based approach???)
        s = getattr(self.s, method, "get")
        if data:
            data = json.dumps(data)
            r = s(url, data=data)
        else:
            r = s(url)

        if text_check:
            if r.status_code == 200 and r.text == text_check:
                if to_json:
                    return r.json()
                else:
                    return r.text
        else:
            if r.status_code == 200:
                if to_json:
                    return r.json()
                else:
                    return r.text

        e = LsmsException("Status code: %s\nURL: %s\nMethod: %s\nData: %s\n%s" % (
            r.status_code, url, method, data, r.text))
        e.status_code = r.status_code
        e.url = url
        e.method = method
        e.data = data
        raise e

    def select_all(self, thing):
        """ Fetch all things

        Args:
            thing: The type of thing (e.g. 'user', 'item', 'policy')

        Returns:
            A list of dicts containing the data from the things

        Raises:
            LsmsException: A error occured when calling the api
        """
        return self.__api_call(urljoin(self.base_url, thing))

    def select_thing(self, thing, _id):
        """ Fetch one thing

        Args:
            thing: The type of thing (e.g. 'user', 'item', 'policy')
            _id: The id/name of the thing

        Returns:
            A dict containing the data from a thing

        Raises:
            LsmsException: A error occured when calling the api
        """
        return self.__api_call(urljoin(self.base_url, thing, _id))

    def select_thing_log(self, thing, _id):
        """ Fetch the history from one thing

        Args:
            thing: The type of thing (e.g. 'user', 'item', 'policy')
            _id: The id/name of the thing

        Returns:
            A list containing the history from a thing

        Raises:
            LsmsException: A error occured when calling the api
        """
        return self.__api_call(urljoin(self.base_url, thing, _id, "log"))

    def delete_thing(self, thing, _id):
        """ Delete a thing

        Args:
            thing: The type of thing (e.g. 'user', 'item', 'policy')
            _id: The id/name of the thing

        Raises:
            LsmsException: A error occured when calling the api
        """
        self.__api_call(urljoin(self.base_url, thing, _id),
                        method="delete", to_json=False,
                        text_check="true")

    def create_thing(self, thing, data):
        """ Create a thing

        Args:
            thing: The type of thing (e.g. 'user', 'item', 'policy')
            data: A dict with the data for the thing

        Returns:
            A int with the id/name of the thing

        Raises:
            LsmsException: A error occured when calling the api
        """
        data = self.__api_call(urljoin(self.base_url, thing),
                               method="post", data=data,
                               to_json=True)
        return basename(data)

    def update_thing(self, thing, data):
        """ Update a thing

        Args:
            thing: The type of thing (e.g. 'user', 'item', 'policy')
            data: A dict with the new data for the thing

        Raises:
            LsmsException: A error occured when calling the api
        """
        self.__api_call(urljoin(self.base_url, thing),
                        method="put", data=data,
                        to_json=False, text_check="true")


def test(base_url):
    l = Lsms(base_url)

    try:
        payload = {'Name': "hans", 'EMail': "hans@example.com", 'Password': 'hans'}
        log.info(l.create_thing("user", payload))
    except LsmsException as e:
        if e.status_code != 401:
            log.info(e)
            return

    try:
        payload = {'Name': "bernd", 'EMail': "bernd@example.com", 'Password': 'bernd'}
        log.info(l.create_thing("user", payload))
    except LsmsException as e:
        if e.status_code != 401:
            log.info(e)
            return

    try:
        payload = {'Name': "franz", 'EMail': "franz@example.com", 'Password': 'franz'}
        log.info(l.create_thing("user", payload))
    except LsmsException as e:
        if e.status_code != 401:
            log.info(e)
            return

    try:
        payload = {'Name': "franz", 'EMail': "franz@example.com", 'Password': 'franz'}
        log.info(l.create_thing("user", payload))
    except LsmsException as e:
        if e.status_code != 401:
            log.info(e)
            return

    l.set_credentials("bernd", "bernd")

    payload = {'Id': 1,
               'name': 'Prusarotti',
               'Description': 'Prusa Mendel 3D-Drucker, der wegen seiner singenden Geräusche den Spitznamen "Prusarotti" (von Luciano Pavarotti, Opernsänger) bekommen hat.',
               'Contains': [],
               #'Owner': "",
               'Usage': "Description can be found in the [wiki](http://wiki.openlab-augsburg.de/openwiki:maschinen:prusarotti)",
               'Maintainer': "hans"}
    thing_id = l.create_thing("item", payload)
    log.info(thing_id)

    payload['Maintainer'] = "bernd"
    payload['Owner'] = "franz"
    payload['Id'] = int(thing_id)
    log.info(l.update_thing("item", payload))

    log.info(l.select_thing_log("item", payload['Id']))

    items = l.select_all("item")
    for item in items:
        l.delete_thing("item", item['Id'])

    users = l.select_all("user")
    for user in users:
        l.set_credentials(user['Name'], user['Name'])
        l.delete_thing("user", user['Name'])

if __name__ == '__main__':
    import signal

    base_url = "http://localhost:8080/"

    logging.basicConfig(level=logging.DEBUG)
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    #import cProfile
    #stats_file = "stats.prof"
    #cProfile.run("test()", stats_file)

    test(base_url)

    print("done")
