import enum

"""
wallets types enum 

@Author: Efrat Cohen
@Date: 02.2023
"""


class Wallet(enum.Enum):
    """
    the wallets names needs to be exactly the same as in the site.
    Pay attention to upper and lower case letters
    """
    metamask = 'MetaMask'
    coinbase = 'Coinbase'
    nami = "Nami"
