#!/usr/bin/env python
# coding:utf-8

# Copyright (C) 2018- by AnJia <anjia0532@gmail.com> and Aivars Kalvans <aivars.kalvans@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import re
import random
import base64
import logging
import requests

log = logging.getLogger('scrapy.proxies')

class Mode:
  RANDOMIZE_PROXY_EVERY_REQUESTS, RANDOMIZE_PROXY_ONCE, SET_CUSTOM_PROXY = range(3)

class RandomProxy(object):
  def __init__(self, settings):
    proxy_settings = settings.get('PROXY_SETTINGS',dict())
    self.chosen_proxy = ''
    
    self.mode = proxy_settings.get('mode',0)
    self.proxy_list = proxy_settings.get('list',list())
    self.use_real_ip = proxy_settings.get('use_real_when_empty',False)
    self.from_proxies_server = proxy_settings.get('from_proxies_server',False)
    self.custom_proxy = proxy_settings.get('custom_proxy','')

    lines = list()

    if (self.mode == Mode.RANDOMIZE_PROXY_EVERY_REQUESTS 
        or self.mode == Mode.RANDOMIZE_PROXY_ONCE):
      if not (self.proxy_list or isinstance(self.proxy_list, list)):
        raise KeyError('PROXY_LIST setting is missing')

      try:
        for i in self.proxy_list:
          if self.from_proxies_server:
            ips = requests.get(i).json()
            lines.extend(list("http://" + ip[0] + ":" + str(ip[1]) for ip in ips if ips))
          else:
            fin = open(i)
            lines.extend(fin.readlines())
            fin.close()
      except Exception as e:
        logging.exception(e)

    elif self.mode == Mode.SET_CUSTOM_PROXY and self.custom_proxy:
      lines = list(self.custom_proxy)
    else:
      raise KeyError('unknown Mode, RANDOMIZE_PROXY_EVERY_REQUESTS, RANDOMIZE_PROXY_ONCE, SET_CUSTOM_PROXY plz!')

    if not lines:
      if self.use_real_ip:
        return
      else:
        raise KeyError('PROXIES is empty')

    self.proxies = {}
    try:
      for line in lines:
        parts = re.match('(\\w+://)([^:]+?:[^@]+?@)?(.+)', line.strip())
        if not parts:
          continue

        # Cut trailing @
        if parts.group(2):
          user_pass = parts.group(2)[:-1]
        else:
          user_pass = ''

        self.proxies[parts.group(1) + parts.group(3)] = user_pass
    except Exception as e:
      logging.exception(e)

    if (self.mode == Mode.RANDOMIZE_PROXY_ONCE 
        or self.mode == Mode.SET_CUSTOM_PROXY):
      self.chosen_proxy = random.choice(list(self.proxies.keys()))

  @classmethod
  def from_crawler(cls, crawler):
    return cls(crawler.settings)

  def process_request(self, request, spider):
    # Don't overwrite with a random one (server-side state for IP)
    if 'proxy' in request.meta:
      if request.meta["exception"] is False:
        return
    request.meta["exception"] = False
    if len(self.proxies) == 0:
      if self.use_real_ip:
        return
      else:
        raise ValueError('All proxies are unusable, cannot proceed')

    if self.mode == Mode.RANDOMIZE_PROXY_EVERY_REQUESTS:
      proxy_address = random.choice(list(self.proxies.keys()))
    else:
      proxy_address = self.chosen_proxy

    proxy_user_pass = self.proxies[proxy_address]

    if proxy_address:
      request.meta['proxy'] = proxy_address

    if proxy_user_pass:
      basic_auth = 'Basic ' + base64.b64encode(proxy_user_pass.encode()).decode()
      request.headers['Proxy-Authorization'] = basic_auth

    log.debug('Using proxy <%s>, %d proxies left' % (proxy_address, len(self.proxies)))

  def process_exception(self, request, exception, spider):
    if 'proxy' not in request.meta:
      return
    if (self.mode == Mode.RANDOMIZE_PROXY_EVERY_REQUESTS 
        or self.mode == Mode.RANDOMIZE_PROXY_ONCE):
      proxy = request.meta['proxy']
      try:
        del self.proxies[proxy]
      except KeyError:
        pass
      request.meta["exception"] = True
      if self.mode == Mode.RANDOMIZE_PROXY_ONCE:
        self.chosen_proxy = random.choice(list(self.proxies.keys()))
      log.info('Removing failed proxy <%s>, %d proxies left' % (proxy, len(self.proxies)))