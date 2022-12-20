import web3
import constants as c # From constants.py file

# To solve a weird error
# https://stackoverflow.com/questions/70812529/the-field-extradata-is-97-bytes-but-should-be-32-it-is-quite-likely-that-you-a
from web3.middleware import geth_poa_middleware


class SendBot():
    """A bot that sends a token to an address periodically."""
    
    def __init__(self,
                 address, # Address of the wallet the SendBot is using
                 private_key, # Private Key of the wallet the SendBot is using
                 network, # Which blockchain we're using
                 token, # Which token we are sending
                 recipient_address, # The address we are sending the token to
                 last_sent_date # The date of the last time the bot sent the token
                 ):
        self.address = address
        self.private_key = private_key
        self.network = network
        self.token = token[network]

        # To solve the weird error mentioned above
        self.w3 = web3.Web3(web3.HTTPProvider(c.RPC[network]))
        self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        
    def send(self):
        """Send token"""
        pass