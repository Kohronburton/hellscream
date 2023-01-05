#
#  https://docs.cream.finance/v/binance-smart-chain/lending/lending-contract-address
#  https://docs.cream.finance/flash-loans#step-by-step-guide
#

import json
from network.provider import random_local_provider
from web3 import Web3


class CreamTokenBase:

    def __init__(self):
        self.addr_tkn = {}

    def _sanitize_addresses(self, addr_tkn):
        for add, tkn in addr_tkn.items():
            add = Web3.toChecksumAddress(add)
            self.addr_tkn[add] = tkn


class CREAMLending(CreamTokenBase):

    def __init__(self):
        super(CREAMLending, self).__init__()
        addr_tkn = {
            Web3.toChecksumAddress('0x1ffe17b99b439be0afc831239ddecda2a790ff3a'): {'name': 'crBNB', 'flashloan': False},
            Web3.toChecksumAddress('0x15CC701370cb8ADA2a2B6f4226eC5CF6AA93bC67'): {'name': 'crWBNB', 'flashloan': True},
            Web3.toChecksumAddress('0x2bc4eb013ddee29d37920938b96d353171289b7c'): {'name': 'crBUSD', 'flashloan': True},
            Web3.toChecksumAddress('0x11883Cdea6bAb720092791cc89affa54428Ce069'): {'name': 'crBTCB', 'flashloan': True},
            Web3.toChecksumAddress('0xAa46e2c21B7763a73DB48e9b318899253E66e20C'): {'name': 'crXRP', 'flashloan': True},
            Web3.toChecksumAddress('0xCb87Cee8c77CdFD310fb3C58ff72e688d46f90b1'): {'name': 'crBCH', 'flashloan': True},
            Web3.toChecksumAddress('0xb31f5d117541825D6692c10e4357008EDF3E2BCD'): {'name': 'crETH', 'flashloan': True},
            Web3.toChecksumAddress('0x8cc7E2a6de999758499658bB702143FD025E09B2'): {'name': 'crLTC', 'flashloan': True},
            Web3.toChecksumAddress('0xEF6d459FE81C3Ed53d292c936b2df5a8084975De'): {'name': 'crUSDT', 'flashloan': True},
            Web3.toChecksumAddress('0x3942936782d788ce69155F776A51A5F1C9dd9B22'): {'name': 'crLINK', 'flashloan': True},
            Web3.toChecksumAddress('0x53D88d2ffDBE71E81D95b08AE0cA49D0C4A8515f'): {'name': 'crDOT', 'flashloan': True},
            Web3.toChecksumAddress('0x81C15D3E956e55e77E1f3F257f0A65Bd2725fC55'): {'name': 'crADA', 'flashloan': True},
            Web3.toChecksumAddress('0x426D6D53187be3288fe37f214e3F6901D8145b62'): {'name': 'crCREAM', 'flashloan': False},
            Web3.toChecksumAddress('0x738f3810b3dA0F3e6dC8C689D0d72f3b4992c43b'): {'name': 'crBAND', 'flashloan': True},
            Web3.toChecksumAddress('0x19eE64850862cFd234e20c0db4edA286f12ec907'): {'name': 'crEOS', 'flashloan': True},
            Web3.toChecksumAddress('0x9095e8d707E40982aFFce41C61c10895157A1B22'): {'name': 'crDAI', 'flashloan': True},
            Web3.toChecksumAddress('0xE692714717a89E4F2ab89dd17d8DDdD7bb52De8e'): {'name': 'crXTZ', 'flashloan': True},
            Web3.toChecksumAddress('0x1aF8c1C3AD36A041cb6678feD86B1E095004fd16'): {'name': 'crFIL', 'flashloan': True},
            Web3.toChecksumAddress('0xEA466cd2583A0290b9E7b987a769a7Eb468FB0A5'): {'name': 'crYFI', 'flashloan': True},
            Web3.toChecksumAddress('0x3B0Be453a4008EBc2eDd457e7Bd355f1C5469d68'): {'name': 'crUNI', 'flashloan': True},
            Web3.toChecksumAddress('0x0E9d900C884964dC4B26db96Ba113825B1a09Baa'): {'name': 'crATOM', 'flashloan': True},
            Web3.toChecksumAddress('0xD83C88DB3A6cA4a32FFf1603b0f7DDce01F5f727'): {'name': 'crUSDC', 'flashloan': True},
            Web3.toChecksumAddress('0x264Bc4Ea2F45cF6331AD6C3aC8d7257Cf487FcbC'): {'name': 'crALPHA', 'flashloan': True},
            Web3.toChecksumAddress('0x2d3bfaDF9BC94E3Ab796029A030e863F1898aA06'): {'name': 'crTWT', 'flashloan': True},
            Web3.toChecksumAddress('0xbf9b95b78bc42f6cf53ff2a0ce19d607cfe1ff82'): {'name': 'crCAKE', 'flashloan': True},
            Web3.toChecksumAddress('0x4ebdef163ff08ac1d56a89bafefd6c01cc28a48f'): {'name': 'crXVS', 'flashloan': True},
            Web3.toChecksumAddress('0x4cB7F1f4aD7a6b53802589Af3B90612C1674Fec4'): {'name': 'crBAT', 'flashloan': True},
            Web3.toChecksumAddress('0x84902bd5ccef97648Bf69C5096729A9367043bEb'): {'name': 'crVAI', 'flashloan': True},
            Web3.toChecksumAddress('0xF77DF34F4Bf632Fb5CA928592a73a29A42BCf0B1'): {'name': 'crAUTO', 'flashloan': True},
            Web3.toChecksumAddress('0x7F746A80506a4cafA39938f7C08Ad59cFa6dE418'): {'name': 'crRENBTC', 'flashloan': True},
            Web3.toChecksumAddress('0xbE7E1d74AcAE787355169bC61A8729b2040fCe6b'): {'name': 'crRENZEC', 'flashloan': True},
            Web3.toChecksumAddress('0xDCf60E349a5AAeeEcdd2fb6772931FBF3486eD1C'): {'name': 'crBETH', 'flashloan': True},
            Web3.toChecksumAddress('0xc17C8C5b8bB9456c624f8534FdE6cBda2451488C'): {'name': 'crIOTX', 'flashloan': True},
            Web3.toChecksumAddress('0xa8D75A0D17D2f4F2f4673975Ab8470269D019c96'): {'name': 'crSXP', 'flashloan': True},
            Web3.toChecksumAddress('0x9B53e7D5e3F6Cc8694840eD6C9f7fee79e7Bcee5'): {'name': 'crSUSHI', 'flashloan': True}
        }
        self._sanitize_addresses(addr_tkn)
        self.w3 = random_local_provider()

    def max_flashloan_liquidity(self, underlying_asset_address):

        cream_fl_addr = CREAMLending.token_fl_mapping(underlying_asset_address)
        erc20abi = json.load(open('abi/erc20.abi'))

        bep20Token = self.w3.eth.contract(address=underlying_asset_address, abi=erc20abi)
        amount = bep20Token.functions.balanceOf(cream_fl_addr).call()

        return amount

    @staticmethod
    def token_fl_mapping(underlying_asset_address=None):

        #    BEP20 to CREAM Flashloan mapping
        #    BEP20 ADDRESS                                # CREAM FLASHLOAN CONTRACT

        mp = {
            Web3.toChecksumAddress('0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c'): Web3.toChecksumAddress('0x15CC701370cb8ADA2a2B6f4226eC5CF6AA93bC67'),  # WBNB
            Web3.toChecksumAddress('0xe9e7cea3dedca5984780bafc599bd69add087d56'): Web3.toChecksumAddress('0x2bc4eb013ddee29d37920938b96d353171289b7c'),  # BUSD
            Web3.toChecksumAddress('0x7130d2a12b9bcbfae4f2634d864a1ee1ce3ead9c'): Web3.toChecksumAddress('0x11883Cdea6bAb720092791cc89affa54428Ce069'),  # BTCB
            Web3.toChecksumAddress('0x1d2f0da169ceb9fc7b3144628db156f3f6c60dbe'): Web3.toChecksumAddress('0xAa46e2c21B7763a73DB48e9b318899253E66e20C'),  # XRP
            Web3.toChecksumAddress('0x8ff795a6f4d97e7887c79bea79aba5cc76444adf'): Web3.toChecksumAddress('0xCb87Cee8c77CdFD310fb3C58ff72e688d46f90b1'),  # BCH
            Web3.toChecksumAddress('0x2170ed0880ac9a755fd29b2688956bd959f933f8'): Web3.toChecksumAddress('0xb31f5d117541825D6692c10e4357008EDF3E2BCD'),  # ETH
            Web3.toChecksumAddress('0x4338665cbb7b2485a8855a139b75d5e34ab0db94'): Web3.toChecksumAddress('0x8cc7E2a6de999758499658bB702143FD025E09B2'),  # LTC
            Web3.toChecksumAddress('0x55d398326f99059ff775485246999027b3197955'): Web3.toChecksumAddress('0xEF6d459FE81C3Ed53d292c936b2df5a8084975De'),  # USDT
            Web3.toChecksumAddress('0xf8a0bf9cf54bb92f17374d9e9a321e6a111a51bd'): Web3.toChecksumAddress('0x3942936782d788ce69155F776A51A5F1C9dd9B22'),  # LINK
            Web3.toChecksumAddress('0x7083609fce4d1d8dc0c979aab8c869ea2c873402'): Web3.toChecksumAddress('0x53D88d2ffDBE71E81D95b08AE0cA49D0C4A8515f'),  # DOT
            Web3.toChecksumAddress('0x3ee2200efb3400fabb9aacf31297cbdd1d435d47'): Web3.toChecksumAddress('0x81C15D3E956e55e77E1f3F257f0A65Bd2725fC55'),  # ADA
            Web3.toChecksumAddress('0xd4cb328a82bdf5f03eb737f37fa6b370aef3e888'): Web3.toChecksumAddress('0x426D6D53187be3288fe37f214e3F6901D8145b62'),  # CREAM
            Web3.toChecksumAddress('0xad6caeb32cd2c308980a548bd0bc5aa4306c6c18'): Web3.toChecksumAddress('0x738f3810b3dA0F3e6dC8C689D0d72f3b4992c43b'),  # BAND
            Web3.toChecksumAddress('0x56b6fb708fc5732dec1afc8d8556423a2edccbd6'): Web3.toChecksumAddress('0x19eE64850862cFd234e20c0db4edA286f12ec907'),  # EOS
            Web3.toChecksumAddress('0x1af3f329e8be154074d8769d1ffa4ee058b1dbc3'): Web3.toChecksumAddress('0x9095e8d707E40982aFFce41C61c10895157A1B22'),  # DAI
            Web3.toChecksumAddress('0x16939ef78684453bfdfb47825f8a5f714f12623a'): Web3.toChecksumAddress('0xE692714717a89E4F2ab89dd17d8DDdD7bb52De8e'),  # XTZ
            Web3.toChecksumAddress('0x0d8ce2a99bb6e3b7db580ed848240e4a0f9ae153'): Web3.toChecksumAddress('0x1aF8c1C3AD36A041cb6678feD86B1E095004fd16'),  # FIL
            Web3.toChecksumAddress('0x88f1a5ae2a3bf98aeaf342d26b30a79438c9142e'): Web3.toChecksumAddress('0xEA466cd2583A0290b9E7b987a769a7Eb468FB0A5'),  # YFI
            Web3.toChecksumAddress('0xbf5140a22578168fd562dccf235e5d43a02ce9b1'): Web3.toChecksumAddress('0x3B0Be453a4008EBc2eDd457e7Bd355f1C5469d68'),  # UNI
            Web3.toChecksumAddress('0x0eb3a705fc54725037cc9e008bdede697f62f335'): Web3.toChecksumAddress('0x0E9d900C884964dC4B26db96Ba113825B1a09Baa'),  # ATOM
            Web3.toChecksumAddress('0x8ac76a51cc950d9822d68b83fe1ad97b32cd580d'): Web3.toChecksumAddress('0xD83C88DB3A6cA4a32FFf1603b0f7DDce01F5f727'),  # USDC
            Web3.toChecksumAddress('0xa1faa113cbe53436df28ff0aee54275c13b40975'): Web3.toChecksumAddress('0x264Bc4Ea2F45cF6331AD6C3aC8d7257Cf487FcbC'),  # ALPHA
            Web3.toChecksumAddress('0x4b0f1812e5df2a09796481ff14017e6005508003'): Web3.toChecksumAddress('0x2d3bfaDF9BC94E3Ab796029A030e863F1898aA06'),  # TWT
            Web3.toChecksumAddress('0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82'): Web3.toChecksumAddress('0xbf9b95b78bc42f6cf53ff2a0ce19d607cfe1ff82'),  # CAKE
            Web3.toChecksumAddress('0xcf6bb5389c92bdda8a3747ddb454cb7a64626c63'): Web3.toChecksumAddress('0x4ebdef163ff08ac1d56a89bafefd6c01cc28a48f'),  # XVS
            Web3.toChecksumAddress('0x101d82428437127bf1608f699cd651e6abf9766e'): Web3.toChecksumAddress('0x4cB7F1f4aD7a6b53802589Af3B90612C1674Fec4'),  # BAT
            Web3.toChecksumAddress('0x4bd17003473389a42daf6a0a729f6fdb328bbbd7'): Web3.toChecksumAddress('0x84902bd5ccef97648Bf69C5096729A9367043bEb'),  # VAI
            Web3.toChecksumAddress('0xa184088a740c695e156f91f5cc086a06bb78b827'): Web3.toChecksumAddress('0xF77DF34F4Bf632Fb5CA928592a73a29A42BCf0B1'),  # AUTO
            Web3.toChecksumAddress('0xfce146bf3146100cfe5db4129cf6c82b0ef4ad8c'): Web3.toChecksumAddress('0x7F746A80506a4cafA39938f7C08Ad59cFa6dE418'),  # RENBTC
            Web3.toChecksumAddress('0x695fd30af473f2960e81dc9ba7cb67679d35edb7'): Web3.toChecksumAddress('0xbE7E1d74AcAE787355169bC61A8729b2040fCe6b'),  # RENZEC
            Web3.toChecksumAddress('0x250632378e573c6be1ac2f97fcdf00515d0aa91b'): Web3.toChecksumAddress('0xDCf60E349a5AAeeEcdd2fb6772931FBF3486eD1C'),  # BETH
            Web3.toChecksumAddress('0x9678e42cebeb63f23197d726b29b1cb20d0064e5'): Web3.toChecksumAddress('0xc17C8C5b8bB9456c624f8534FdE6cBda2451488C'),  # IOTX
            Web3.toChecksumAddress('0x47bead2563dcbf3bf2c9407fea4dc236faba485a'): Web3.toChecksumAddress('0xa8D75A0D17D2f4F2f4673975Ab8470269D019c96'),  # SXP
            Web3.toChecksumAddress('0x947950bcc74888a40ffa2593c5798f11fc9124c4'): Web3.toChecksumAddress('0x9B53e7D5e3F6Cc8694840eD6C9f7fee79e7Bcee5'),  # SUSHI
        }

        if underlying_asset_address is None:
            return mp
        else:
            if underlying_asset_address not in mp.keys():
                return None
            else:
                return mp[underlying_asset_address]
