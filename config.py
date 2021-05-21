# Wrapper for the program configuration
class Config:
    def __init__(self, action, secret_image, k, directory):
        self.action = action
        self.secret_image = secret_image
        self.k = k
        self.directory = directory