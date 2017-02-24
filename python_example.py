# Zenoss-4.x JSON API Example (python)
#
# To quickly explore, execute 'python -i api_example.py'
#
# >>> z = ZenossAPIExample()
# >>> events = z.get_events()
# etc.

import json
import urllib
import urllib2

ZENOSS_INSTANCE = 'http://localhost:8080'
ZENOSS_USERNAME = 'user1'
ZENOSS_PASSWORD = '1234'

ROUTERS = { 'MessagingRouter': 'messaging',
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
            'MaintenanceWindowRouter': 'maintwindow',
            }

class ZenossAPI():
    def __init__(self, debug=False):
        """
        Initialize the API connection, log in, and store authentication cookie
        """
        # Use the HTTPCookieProcessor as urllib2 does not save cookies by default
        self.urlOpener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
        if debug: self.urlOpener.add_handler(urllib2.HTTPHandler(debuglevel=1))
        self.reqCount = 1

        # Contruct POST params and submit login.
        loginParams = urllib.urlencode(dict(
                        __ac_name = ZENOSS_USERNAME,
                        __ac_password = ZENOSS_PASSWORD,
                        submitted = 'true',
                        came_from = ZENOSS_INSTANCE + '/zport/dmd'))
        self.urlOpener.open(ZENOSS_INSTANCE + '/zport/acl_users/cookieAuthHelper/login',
                            loginParams)

    def _router_request(self, router, method, data=[]):
        if router not in ROUTERS:
            raise Exception('Router "' + router + '" not available.')

        # Contruct a standard URL request for API calls
        req = urllib2.Request(ZENOSS_INSTANCE + '/zport/dmd/' +
                              ROUTERS[router] + '_router')

        # NOTE: Content-type MUST be set to 'application/json' for these requests
        req.add_header('Content-type', 'application/json; charset=utf-8')

        # Convert the request parameters into JSON
        reqData = json.dumps([dict(
                    action=router,
                    method=method,
                    data=data,
                    type='rpc',
                    tid=self.reqCount)])

        # Increment the request count ('tid'). More important if sending multiple
        # calls in a single request
        self.reqCount += 1

        # Submit the request and convert the returned JSON to objects
        return json.loads(self.urlOpener.open(req, reqData).read())

    def get_devices(self, deviceClass='/zport/dmd/Devices'):
        return self._router_request('DeviceRouter', 'getDevices',
                                    data=[{'uid': deviceClass,
                                           'params': {} }])['result']

    def get_boundtemplates(self, deviceid):
        return self._router_request('DeviceRouter', 'getBoundTemplates',
                                    data=[{'uid': deviceid}])['result']

    def get_info(self, cmp):
	data = dict(uid=cmp, keys=None)
        return self._router_request('DeviceRouter', 'getInfo',
                                    data=[{ 'uid': cmp,
                                            'keys': None },
                                         ])['result']

    def get_components(self, uid):
	data = dict(uid=uid, meta_type=None, keys=None, start=0, dir='ASC')
#	data = dict(uid=deviceid)
        return self._router_request('DeviceRouter', 'getComponents', [data])['result']

#    def get_components(self, uid, meta_type=None, keys=None, start=0, sort='titleOrId', dir='ASC', name=None):
#        data = dict(uid=uid)
#        return self._router_request('DeviceRouter', 'getComponents', [data])['result']

    def get_templates(self, id):
        data = dict(id=id)
        return self._router_request('DeviceRouter', 'getTemplates', [data])['result']

    def get_local_templates(self, query, uid):
        data = dict(uid=uid, query=query)
        return self._router_request('DeviceRouter', 'getLocalTemplates', [data])['result']

    def get_thresholds(self, uid, query=''):
        data = dict(uid=uid)
        return self._router_request('TemplateRouter', 'getThresholds', [data])['result']
