class Event: 

  def __init__(self, type, start_date, end_date, start_time, end_time): 
    self.type = type
    self.start_date = start_date
    self.end_date = end_date
    self.start_time = start_time
    self.end_time = end_time

  def GetType(self)
    return self.type

  
