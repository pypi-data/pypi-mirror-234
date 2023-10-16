from coincurve import PrivateKey as CoinCurvePrivateKey
from eth_utils import keccak

from atlantiscore.types.evm import EVMAddress

NUMBER_OF_BYTES_IN_ADDRESS = 20


class PrivateKey(CoinCurvePrivateKey):
    @property
    def public_address(self) -> EVMAddress:
        public_key = self.public_key.format(compressed=False)[1:]
        return EVMAddress(keccak(public_key)[-NUMBER_OF_BYTES_IN_ADDRESS:])
