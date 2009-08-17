# Copyright 2009 Google Inc. All Rights Reserved.

"""Mocks for namebench.py, does not send any actual DNS requests."""

__author__ = 'tstromberg@google.com (Thomas Stromberg)'

import dns.message
import dns.rrset
import namebench


class MockNameBench(namebench.NameBench):
  """Neutered NameBench, does make any DNS queries."""

  def LoadDomainsList(self, unused_filename):
    return ['slashdot.org', 'google.com', 'x.gov']

  def BuiltInNameServerDetails(self):
    return {'192.168.1.1': 'Test', '192.168.1.2': 'Test 2'}

  def InternalNameServers(self):
    return ['10.0.0.1']

  def TimedDNSRequest(self, nameserver, type_string, record_string):
    """Call the real method, but manipulate the returned duration."""
    response = super(MockNameBench, self).TimedDNSRequest(
        nameserver, type_string, record_string
    )[0]
    if nameserver == '192.168.1.2':
      return (response, 22.5)
    else:
      return (response, 9.0)

  def DNSQuery(self, request, nameserver):
    # This server is down
    if str(nameserver) == '192.168.1.1':
      return None
    message = dns.message.Message()

    # Only positive requests from here.
    if 'INTERNIC.NET.' in str(request) or 'google.com.' in str(request):
      message.answer = [dns.rrset.RRset(None, None, None)]
    return message

  def DisplayBanner(self):
    pass