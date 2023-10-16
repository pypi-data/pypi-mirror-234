class Joint:
    lower_limit: int
    upper_limit: int
    speed: int
    servo_Id: int
    id: int
    
    def __init__(self, lower_limit: int, upper_limit: int, speed: int, id: int) -> None:
        self.lower_limit = lower_limit
        self.upper_limit = upper_limit
        self.speed = speed
        self.id = id
