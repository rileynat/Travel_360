
class City: 
  """Creates a city object."""

  def __init__(self, name, country): 
    self.name = name 
    self.country = country
    self.region = ''
    self.state = ''
    self.events = []
    self.climate = None
    self.activities = []
    self.days = []
    self.photo = None

  def AddEvent(self, event): 
    self.events += event

  def AddActivity(self, activity): 
    self.activities += activity

  def GetName(self): 
    return self.name

  def GetRegion(self): 
    return self.region

  def GetEvents(self): 
    return self.events

  def GetActivities(self): 
    return self.activities

  def GetClimate(self): 
    return self.climate

  def SetPhoto(self, photo_url): 
    self.photo = photo_url
