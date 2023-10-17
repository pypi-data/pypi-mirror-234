import logging

import math
import socket
from threading import RLock

from lxdbapi import errors, versions
import ssl
import time

try:
    import httplib
except ImportError:
    import http.client as httplib

__all__ = ['HttpAvaticaConnection', 'TcpAvaticaConnection', 'NetAvaticaConnection']

logger = logging.getLogger(__name__)

class NetAvaticaConnection(object):
    def close(self):
        raise NotImplementedError('Extend NetAvaticaConnection')

    def request(self, body=None):
        raise NotImplementedError('Extend NetAvaticaConnection')

    def checkSerialization(self):
        raise NotImplementedError('Extend NetAvaticaConnection')


class TcpAvaticaConnection(NetAvaticaConnection):

    def __init__(self, url, secure, max_retries):
        self._close_lock = RLock()
        self.url = url
        self.secure =secure
        """Opens a HTTP connection to the RPC server."""
        self.max_retries = max_retries if max_retries is not None else 3
        self._opened = False
        self._connect()

    def __del__(self):
        self._close()

    def __exit__(self):
        self._close()

    def _connect(self):
        if not self.secure:
            logger.debug("Using TCP")
            logger.debug("Opening connection to %s:%s", self.url.hostname, self.url.port)
            self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            self.tcp_socket.connect((self.url.hostname, self.url.port))
            self.tcpConn = self.tcp_socket
            self._opened = True
        else:
            logger.debug("Using TCP with SSL")
            logger.debug("Opening connection to %s:%s", self.url.hostname, self.url.port)
            self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            self.tcpConn = ssl.wrap_socket(self.tcp_socket, ssl_version=ssl.PROTOCOL_TLSv1)
            self.tcpConn.connect((self.url.hostname, self.url.port))
            self._opened = True

    def _close(self):
        with self._close_lock:
            if self._opened:
                self._opened = False
                self.tcpConn.close()

    def close(self):
        self._close()

    def request(self, body=None):
        req_sz = len(body)
        # build message Body size, tag(always 0), body
        tag = 0
        msg = bytearray()
        msg.extend(req_sz.to_bytes(4, 'little'))
        msg.extend(tag.to_bytes(4, 'little'))
        msg.extend(body)
        self.tcpConn.sendall(msg)
        hdr = self.tcpConn.recv(8)
        resp_sz = int.from_bytes(hdr[:4], 'little')
        tag = int.from_bytes(hdr[4:], 'little')
        if 0 > resp_sz:
            logger.warning("negative msg size (sz {}) tag:{}".format(resp_sz, tag))
            raise IOError('IO Error on RPC request on {}. Got negative size [{}]'.format(self.url, resp_sz))
        if 0 == resp_sz:
            return None
        response = bytearray()
        pending = resp_sz
        offset = 0
        while pending > 0:
            partial = self.tcpConn.recv(resp_sz)
            l = len(partial)
            offset += l
            pending -= l
            response.extend(partial)
        return response

    def checkSerialization(self):
        raise NotImplementedError('Extend NetAvaticaConnection')


class HttpAvaticaConnection(NetAvaticaConnection):

    def __init__(self, url, secure, max_retries):
        self.url = url
        self.secure =secure
        """Opens a HTTP connection to the RPC server."""
        self.max_retries = max_retries if max_retries is not None else 3
        self._connect()

    def _connect(self):
        if not self.secure:
            logger.debug("Using HTTP")
            logger.debug("Opening connection to %s:%s", self.url.hostname, self.url.port)
            try:
                self.httpConn = httplib.HTTPConnection(self.url.hostname, self.url.port)
                self.httpConn.connect()
                self.cookies = {}
                # self.checkSerialization()
            except (httplib.HTTPException, socket.error) as e:
                raise errors.InterfaceError('Unable to connect to the specified service', e)
        else:
            logger.debug("Using HTTPS")
            logger.debug("Opening connection to %s:%s", self.url.hostname, self.url.port)
            try:
                purpose = ssl.Purpose.SERVER_AUTH
                context = ssl.create_default_context(purpose)
                self.httpConn = httplib.HTTPSConnection(self.url.hostname, self.url.port,
                                                        context=context)
                self.httpConn.connect()
                self.cookies = {}
                # self.checkSerialization()
            except (httplib.HTTPException, socket.error) as e:
                raise errors.InterfaceError('Unable to connect to the specified service', e)

    def close(self):
        """Closes the HTTP connection to the RPC server."""
        logger.debug("Closing connection to %s:%s", self.url.hostname, self.url.port)
        try:
            self.httpConn.close()
        except httplib.HTTPException:
            logger.warning("Error while closing connection", exc_info=True)

    def request(self, body=None):
        method = 'POST'
        headers = {'content-type': 'application/x-google-protobuf'}
        # add cookies if any
        if self.cookies is not None and self.cookies.get('hap-cookie') is not None:
            headers['Cookie'] = self.cookies.get('hap-cookie')
        retry_count = self.max_retries
        while True:
            logger.debug("%s %s %r %r", method, self.url.path, body, headers)
            try:
                self.httpConn.request(method, self.url.path, body=body, headers=headers)
                response = self.httpConn.getresponse()
            except (httplib.HTTPException, ssl.SSLError, BrokenPipeError) as e:
                if retry_count > 0:
                    logger.debug("Error at HTTP connection level... Trying to reconnect to {}".format(self.url))
                    delay = math.exp(-retry_count)
                    logger.debug("HTTP protocol error, will retry in %s seconds...", delay, exc_info=True)
                    self.close()
                    try:
                        self._connect()
                    except BaseException as th:
                        logger.debug("Retry failed on {}: {}".format(self.url, th))
                        raise th
                    logger.debug("Successfully reconnected HTTP connection, Continuing...")
                    time.sleep(delay)
                    retry_count -= 1
                    continue
                raise errors.InterfaceError('RPC request failed on {}'.format(self.url), cause=e)
            else:
                if response.status == httplib.SERVICE_UNAVAILABLE:
                    if retry_count > 0:
                        delay = math.exp(-retry_count)
                        logger.debug("Service unavailable, will retry in %s seconds...", delay, exc_info=True)
                        time.sleep(delay)
                        retry_count -= 1
                        continue
                # save cookie if using hap
                if response.headers.get('set-cookie') is not None:
                    self.cookies['hap-cookie'] = response.headers.get('set-cookie')
                    logger.debug("Setting cookie: {}:{}".format('hap-cookie', response.headers.get('set-cookie')))
                return response.read()

    def checkSerialization(self):
        retry_count = self.max_retries
        while True:
            logger.debug("OPTIONS %s", self.url.path)
            try:
                self.httpConn.request('OPTIONS', '')
                response = self.httpConn.getresponse()
                response_body = response.read()
                serialization = str(response_body).split(';')

                # Compare the minimum server version against client version
                index = [idx for idx, s in enumerate(serialization) if 'minimumVersion' in s]
                if index:
                    minimumVersions = serialization[index[0]].split("=")[1].split(".")
                    if int(minimumVersions[0]) > int(versions.MAJOR_VERSION) or \
                            (int(minimumVersions[0]) == int(versions.MAJOR_VERSION) and int(minimumVersions[1]) > int(
                                versions.MINOR_VERSION)):
                        raise errors.SerializationError(
                            "Client version '{}.{}' is not allowed to connect. Minimum allowed version is '{}.{}'".format(
                                versions.MAJOR_VERSION, versions.MINOR_VERSION, minimumVersions[0], minimumVersions[1]))

            except IndexError as e:
                raise errors.InterfaceError('Avatica server did not respond correctly. Please check endpoint.', cause=e)
            except httplib.HTTPException as e:
                if retry_count > 0:
                    retry_count -= 1
                    delay = math.exp(-retry_count)
                    logger.debug("HTTP protocol error, will retry in %s seconds...", delay, exc_info=True)
                    self.close()
                    self._connect()
                    time.sleep(delay)
                    continue
                raise errors.InterfaceError('Max retries for attempting to connect and check serialization wasted',
                                            cause=e)
            else:
                if response.status == httplib.SERVICE_UNAVAILABLE:
                    if retry_count > 0:
                        delay = math.exp(-retry_count)
                        logger.debug("Service unavailable, will retry in %s seconds...", delay, exc_info=True)
                        time.sleep(delay)
                        retry_count -= 1
                        continue
                return response
