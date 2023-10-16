import os

class Paytring:
    """
    Intialisation of Key and Secret 
    """
    def __init__(self) -> None:
        
        self.key = os.getenv('key')
        self.secret = os.getenv('secret')
        if not self.key or not self.secret:
            raise Exception('SDK key and secret must be provided.')
        
    