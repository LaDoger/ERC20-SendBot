import web3, json
import constants as c # From constants.py file

# To solve a weird error
# https://stackoverflow.com/questions/70812529/the-field-extradata-is-97-bytes-but-should-be-32-it-is-quite-likely-that-you-a
from web3.middleware import geth_poa_middleware

ERC20_ABI = json.loads("""[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"payable":true,"stateMutability":"payable","type":"fallback"},{"anonymous":false,"inputs":[{"indexed":true,"name":"owner","type":"address"},{"indexed":true,"name":"spender","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Transfer","type":"event"}]
""")

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
        self.token_contract = self.w3.eth.contract(
            address = self.token,
            abi=ERC20_ABI
        )
        self.recipient_address = recipient_address

    def send(self, amount):
        """Send token"""
        #TODO: set gas stuff, especially important on polygon
        contract_tx = self.token_contract.functions["transfer"](self.recipient_address, amount).buildTransaction(
            {
                "from": self.address,
                "nonce": self.w3.eth.get_transaction_count(self.address),
                "gasPrice": self.w3.eth.gas_price, #TODO: optimize because polygon is broken
            }
        )
        signed_contract_tx = self.w3.eth.account.sign_transaction(
            contract_tx, self.private_key
        )
        contract_txhash = self.w3.eth.send_raw_transaction(
            signed_contract_tx.rawTransaction
        )
        contract_txreceipt = self.w3.eth.wait_for_transaction_receipt(
            contract_txhash
        )
        #Assert for the status from contract_txreceipt
        print(contract_txreceipt)
        assert contract_txreceipt.status == 1
        print("call done")

