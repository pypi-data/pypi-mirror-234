from socket          import socket, AF_INET, SOCK_DGRAM
from dnslib          import *
from teamhack_db.sql import select_hostname_recordtype

# Function to handle DNS queries and return a response
def handle_dns_query(conn, data, upstream_server, upstream_port):
    request = DNSRecord.parse(data)

    reply = DNSRecord(DNSHeader(id=request.header.id, qr=1, aa=1, ra=1), q=request.q)

    qname = str(request.q.qname)
    qtype = request.q.qtype
    #if   qtype == QTYPE.NS: qt = 'NS'
    #elif qtype == QTYPE.A:  qt = 'A'
    #else:
    #  a = request.send(upstream_server, upstream_port, tcp=False, timeout=10)
    #  request.add_answer(a)
    #  return request.pack()

    print(f'A qname: {qname}, qtype: {qtype}')
    res = select_hostname_recordtype(conn, qname, qtype)
    print(f'B res {type(res)}: {res}')
    assert isinstance(res, list)
    if not res:
      a = request.send(upstream_server, upstream_port, tcp=False, timeout=10)
      return a
    res = res[0]
    print(f'C res {type(res)}: {res}')
    assert isinstance(res, tuple)
    if not res:
      a = request.send(upstream_server, upstream_port, tcp=False, timeout=10)
      return a

    res = res[3]
    print(f'D res {type(res)}: {res}')
    assert isinstance(res, str)
    if not res:
      a = request.send(upstream_server, upstream_port, tcp=False, timeout=10)
      return a
    #res = res[3]
    #if not res:
    #  a = request.send(upstream_server, upstream_port, tcp=False, timeout=10)
    #  return a
    print(f'E qname: {qname}, qtype: {qtype}, res: {res}')

    #if qname in dns_records and qtype in dns_records[qname]:
    #if res:
    if qtype == QTYPE.NS: reply.add_answer(RR(rname=qname, rtype=qtype, rdata=NS(res)))
    else:                 reply.add_answer(RR(rname=qname, rtype=qtype, rdata=A(res)))
    #else:
    #    # TODO
    #    #reply.add_answer(RR(rname=qname, rtype=qtype, rdata=A('0.0.0.0')))
    #    #q = DNSRecord(q=DNSQuestion(qname))
    #    a = reply.send(upstream_server, upstream_port, tcp=False, timeout=10)
    #    reply.add_answer(a)

    return reply.pack()

# Function to start the DNS server and listen for requests
def start_server(conn, host='', port=53, upstream_server='8.8.8.8', upstream_port=53):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))

    print(f'DNS server listening on port {port}... \n \n' )

    while True:
      try:
        data, address = server_socket.recvfrom(1024)
        response = handle_dns_query(conn, data, upstream_server, upstream_port)
        server_socket.sendto(response, address)
      except: pass

