from datetime import datetime


class Annotation():
    """ Annotation of the properties
    """

    def __init__(self, value, date=None, active=True):
        self.active = active
        self.value = value
        self.date = date
        if self.date is None:
            self.date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

