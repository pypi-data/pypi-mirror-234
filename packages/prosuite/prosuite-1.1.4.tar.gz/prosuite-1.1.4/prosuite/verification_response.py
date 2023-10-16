class VerificationResponse:
    """
    This class represents a VerificationResponse Message.

    :param message: the actual message
    :param message_level: message level -> see class MessageLevel
    :param service_call_status: service status -> see class ServiceStatus

    The str() method is overridden to return all properties from the VerificationResponse when 
    a VerificationResponse object is printed using pythons print() method. 

    """

    def __init__(self, service_call_status: str, message: str, message_level: str):
        #:
        self.message: str = message
        #:
        self.service_call_status = ServiceStatus.status_0
        #:
        self.message_level = MessageLevel.level_40000
        self._set_service_call_status(service_call_status)
        self._set_message_level(message_level)

    def __str__(self):
        return f'service_call_status: {self.service_call_status}\t message_level: {self.message_level} \t ' \
               f'message: {self.message}'

    def _set_service_call_status(self, service_call_status: str):
        if service_call_status == 0:
            self.service_call_status = ServiceStatus.status_0
        if service_call_status == 1:
            self.service_call_status = ServiceStatus.status_1
        if service_call_status == 2:
            self.service_call_status = ServiceStatus.status_2
        if service_call_status == 3:
            self.service_call_status = ServiceStatus.status_3
        if service_call_status == 4:
            self.service_call_status = ServiceStatus.status_4

    def _set_message_level(self, message_level: str):
        if message_level == 110000:
            self.message_level = MessageLevel.level_110000
        if message_level == 70000:
            self.message_level = MessageLevel.level_70000
        if message_level == 60000:
            self.message_level = MessageLevel.level_60000
        if message_level == 40000:
            self.message_level = MessageLevel.level_40000
        if message_level == 30000:
            self.message_level = MessageLevel.level_30000
        if message_level == 10000:
            self.message_level = MessageLevel.level_10000


class ServiceStatus:
    status_0 = 'Undefined'
    status_1 = 'Running'
    status_2 = 'Cancelled'
    status_3 = 'Finished'
    status_4 = 'Failed'


class MessageLevel:
    level_110000 = 'Fatal'
    level_70000 = 'Error'
    level_60000 = 'Warn'
    level_40000 = "Info"
    level_30000 = 'Debug'
    level_10000 = 'Verbose'
