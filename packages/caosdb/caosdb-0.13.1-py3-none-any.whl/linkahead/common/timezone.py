class TimeZone():
    """
    TimeZone, e.g. CEST, Europe/Berlin, UTC+4.


    Attributes
    ----------
    zone_id : string
        ID of the time zone.
    offset : int
        Offset to UTC in seconds.
    display_name : string
        A human-friendly name of the time zone:
    """

    def __init__(self, zone_id, offset, display_name):
        self.zone_id = zone_id
        self.offset = offset
        self.display_name = display_name
