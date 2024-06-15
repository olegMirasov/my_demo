item = {'ID': '62',
'PORTAL_USER_ID': '1',
'PORTAL_NUMBER': 'REST_APP:6',
'PHONE_NUMBER': '4',
'CALL_ID': 'externalCall.fef7ab57e9f54b1ebe5769cdbee3377c.1718123051',
'EXTERNAL_CALL_ID': None,
'CALL_CATEGORY': 'external',
'CALL_DURATION': '4',
'CALL_START_DATE': '2023-08-18T00:00:00+03:00',
'CALL_RECORD_URL': None,
'CALL_VOTE': '0',
'COST': '0.0000',
'COST_CURRENCY': '',
'CALL_FAILED_CODE': '200',
'CALL_FAILED_REASON': '',
'CRM_ENTITY_TYPE': None,
'CRM_ENTITY_ID': None,
'CRM_ACTIVITY_ID': '0',
'REST_APP_ID': '6',
'REST_APP_NAME': 'is_demo',
'TRANSCRIPT_ID': None,
'TRANSCRIPT_PENDING': 'N',
'SESSION_ID': None,
'REDIAL_ATTEMPT': None,
'COMMENT': None,
'RECORD_DURATION': None,
'RECORD_FILE_ID': 144,
'CALL_TYPE': '1'}


class Call:
    def __init__(self, **kwargs):
        self.__dict__ = kwargs

    def get_time(self):
        return self.CALL_START_DATE

c = Call(**item)
print(c.get_time())