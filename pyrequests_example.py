import re
import json
import logging
import requests

# Setup your own config.py
from config import CONFIG


_logDir = '/tmp/'
_logFile = '%szenossApi.log' % _logDir
log = logging.getLogger("zen.PortalAPI")
format = logging.Formatter(
    '%(asctime)s %(name)s %(levelname)s: %(message)s'
    )
lh = logging.FileHandler(_logFile)
lh.setFormatter(format)
log.addHandler(lh)

_ZENOSS_INSTANCE = CONFIG['ZENOSS']['INSTANCE']
_ZENOSS_USERNAME = CONFIG['ZENOSS']['USERNAME']
_ZENOSS_PASSWORD = CONFIG['ZENOSS']['PASSWORD']
_ZENOSS_TIMEOUT = CONFIG['ZENOSS']['TIMEOUT']
_ZENOSS_DEBUG = CONFIG['ZENOSS']['DEBUG']

_ROUTERS = {
    'MessagingRouter': 'messaging',
    'EventsRouter': 'evconsole',
    'ProcessRouter': 'process',
    'ServiceRouter': 'service',
    'DeviceRouter': 'device',
    'NetworkRouter': 'network',
    'TemplateRouter': 'template',
    'DetailNavRouter': 'detailnav',
    'ReportRouter': 'report',
    'MibRouter': 'mib',
    'ZenPackRouter': 'zenpack',
    'SearchRouter': 'search',
    }


class ZenossAPI(object):
    def __init__(self, timeout=_ZENOSS_TIMEOUT, debug=_ZENOSS_DEBUG):
        """
        Initialize the API connection, log in, and store authentication cookie
        """
        self._session = requests.Session()
        self._session.auth = (_ZENOSS_USERNAME, _ZENOSS_PASSWORD)
        self._host = _ZENOSS_INSTANCE
        self._req_count = 0
        self.timeout = float(timeout)
        if debug:
            log.setLevel(logging.DEBUG)
        else:
            log.setLevel(logging.WARNING)

    def _router_request(self, router, method, data=[]):
        if router not in _ROUTERS:
            raise Exception('Router "' + router + '" not available.')

        req_data = json.dumps([dict(
            action=router,
            method=method,
            data=data,
            type='rpc',
            tid=self._req_count)]
            )

        uri = '{0}/zport/dmd/{1}_router'.format(
            self._host,
            _ROUTERS.get(router)
            )
        headers = {'Content-type': 'application/json; charset=utf-8'}
        try:
            response = self._session.post(
                uri,
                data=req_data,
                headers=headers,
                verify=False,
                timeout=self.timeout,
                )
            response.raise_for_status()
        except Exception as e:
            log.warning(str(e))
            return dict(success=False, msg=str(e))

        self._req_count += 1

        try:
            return json.loads(response.content)['result']
        except:
            return response.content

  def getDevices(self, deviceClass='/zport/dmd/Devices'):
        return self._router_request(
            'DeviceRouter',
            'getDevices',
            data=[{
                'uid': deviceClass,
                'params': {},
            }],
        )
