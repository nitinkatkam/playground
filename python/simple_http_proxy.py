#!/bin/python

#
# Author: Nitin Reddy
# Created: November 17, 2018
# Description: Simple HTTP proxy
#

from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from _thread import start_new_thread  # Fun fact - underscore prefix indicates implementation-specific module


# Listener port number
port = 8080


# Entry point. Listens and accepts incoming connections from client and hands off to a separate thread
def main():
    conn_queue = 3
    bufsize = 2048
    s = socket(AF_INET, SOCK_STREAM)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind( ('', port) )  # Default IP
    s.listen(conn_queue)
    while 1:
        conn, addr = s.accept()
        data = conn.recv(bufsize)
        start_new_thread(request_handler, (conn, data, addr) )


# Handles a client's request
def request_handler(conn, data, addr):
    first_line = data.decode("iso-8859-1").split('\n')[0]
    (hostname, port) = get_requested_hostname_and_port(first_line)
    proxy_request(hostname, port, conn, data, addr)


# Gets the hostname and port from the first request line
def get_requested_hostname_and_port(first_line):
    first_line_tokens = first_line.split()
    verb = first_line_tokens[0]
    url_or_host = first_line_tokens[1]

    if verb == 'CONNECT':
        # CONNECT is generally used with HTTPS, but just in case...
        host_with_port = url_or_host  # CONNECT requests don't have a URI scheme
    elif verb == 'GET' or verb == 'HEAD' or verb == 'POST' or verb == 'PUT' or verb == 'PATCH' or verb == 'DELETE':
        # HTTP verbs are followed by a URL when making a proxy request
        tempstr = url_or_host[(url_or_host.find('://')+3):]  # Strip the URI scheme
        host_with_port = tempstr[:tempstr.find('/')]

    # Separate the port no. if it exists
    port_sep_pos = host_with_port.find(':')
    if port_sep_pos==-1:
        port = 80
        hostname = host_with_port
    else:
        port = int(host_with_port[port_sep_pos+1:])
        hostname = host_with_port[:port_sep_pos]

    log_txt = 'Fetch request for: ' + hostname
    print(log_txt)

    return (hostname, port)


# Send the request to the destination server and relay the response to the client
def proxy_request(webserver, port, conn, data, addr):
    bufsize = 2048
    s = socket(AF_INET, SOCK_STREAM)
    s.connect( (webserver, port) )
    s.send(data)  # TODO Strip the first line if it is a CONNECT HTTP tunnel request

    try:
        while 1:
            reply = s.recv(bufsize)
            if len(reply) > 0:
                conn.send(reply)
            else:
                break
    except Exception as ex:
        pass

    s.close()
    conn.close()


# Invoke the entry point
if __name__ == '__main__':
    main()
