class Package_ID_Counter: 
  def __init__(self):
      self.package_id = 0
  
  def add(self):
    self.package_id += 1
  
  def get(self):
    return self.package_id