class action:
    def __init__(self, route):
        self.path = ""
        route = route.strip("/")
        self.parts = route.split('/')
        pass
