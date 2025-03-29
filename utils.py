def format_checkin(checkin):
    '''
    takes CheckIn as input and returns a formatted string with hours and minutes
    '''
    total_seconds = (checkin.timeOut - checkin.timeIn).seconds
    hours = total_seconds // (60*60)
    minutes = (total_seconds % (60 * 60)) // 60
    seconds = total_seconds % 60
    return f"{hours}h {minutes}m {seconds}s"
