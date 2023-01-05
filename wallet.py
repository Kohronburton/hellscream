from dex.dexmanager import DEXManager
from erc20_worker import ERC20_Worker
import json
from network.provider import random_local_provider
import os
from web3 import Web3

ANYSWAP_BRIDGE_FANTOM = {'0x4b3B4120d4D7975455d8C2894228789c91a247F8': {'name': 'Anyswap: Bridge Fantom'}}
ANYSWAP_BRIDGE_POLYGON = {'0x171a9377C5013bb06Bca8CfE22B9C007f2C319F1': {'name': 'Anyswap: Bridge Polygon'}}

BINANCE_HOT_WALLET = {'0x631fc1ea2270e98fbd9d92658ece0f5a269aa161': {'name': 'Binance Hot Wallet'}}
PANCAKE_SWAP_STAKING = {'0x73feaa1eE314F8c655E354234017bE2193C9E24E': {'name': 'Pancake Swap - Main Staking Contract'}}
MDEX_ROUTER = {'0x7DAe51BD3E3376B8c7c4900E9107f12Be3AF1bA8': {'name': 'MDEX Router'}}
AUTOFARM_V2 = {'0x0895196562C7868C5Be92459FaE7f877ED450452': {'name': 'AutoFarm V2'}}
BOG_STAKING = {'0xc3ab35d3075430f52D2636d08D4f29bD39a18B65': {'name': 'BOG Staking'}}
PHOENIX_NEBULA = {'0x173C3C5BfB4c7B46eF5cC392EF502C454BCabC4F': {'name': 'PhoenixNebula'}}
BSC_TOKEN_HUB = {'0x0000000000000000000000000000000000001004': {'name': 'BSC: Token Hub'}}


class Wallet:

    @staticmethod
    def address():
        return os.environ.get('PUBLIC_KEY')

    @staticmethod
    def private_key():
        return os.environ.get('PRIVATE_KEY')

    @staticmethod
    def approve_if_needed(wallet_address, contract_address, router_address, amount, w3_provider=None):
        if w3_provider is None:
            w3_provider = random_local_provider()

        erc20abi = json.load(open('abi/erc20.abi'))
        bep_20 = w3_provider.eth.contract(address=contract_address, abi=erc20abi)
        approved_amount = bep_20.functions.allowance(wallet_address, router_address).call()
        if approved_amount >= amount:
            return True
        try:
            tx = bep_20.functions.approve(router_address, 2**256-1).buildTransaction({
                'from': wallet_address,
                'value': 0,
                'gasPrice': int(20e9),
                'gas': 1500000,
                "nonce": w3_provider.eth.getTransactionCount(wallet_address),
                })
            signed_tx = w3_provider.eth.account.sign_transaction(tx, private_key=Wallet.private_key())
            txhash = w3_provider.eth.sendRawTransaction(signed_tx.rawTransaction)
            print('Approving... ', txhash.hex())
            w3_provider.eth.waitForTransactionReceipt(txhash.hex(), timeout=600)  # 10 minutes
        except Exception as e:
            print('Approve Exception:', e)
            return False
        return True


if __name__ == '__main__':

    dm = DEXManager()
    erc = ERC20_Worker()
    tokens = erc.all_tokens()

    pending_wallets = [
        ('0x631fc1ea2270e98fbd9d92658ece0f5a269aa161', 4373), ('0x55d398326f99059ff775485246999027b3197955', 3292), ('0xe9e7cea3dedca5984780bafc599bd69add087d56', 1949), ('0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82', 557), ('0x10ed43c718714eb63d5aa57b78b54704e256024e', 515), ('0x54a936ffd2be2b3e307aad33bd79e612b9b7b88d', 217), ('0x3bb5f6285c312fc7e1877244103036ebbeda193d', 194), ('0x2170ed0880ac9a755fd29b2688956bd959f933f8', 153), ('0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c', 151), ('0x1d2f0da169ceb9fc7b3144628db156f3f6c60dbe', 135), ('0x3ee2200efb3400fabb9aacf31297cbdd1d435d47', 122), ('0x9c65ab58d8d978db963e63f2bfb7121627e3a739', 92), ('0x8595f9da7b868b1822194faed312235e43007b49', 88), ('0x2222227e22102fe3322098e4cbfe18cfebd57c95', 58), ('0x2859e4544c4bb03966803b044a93563bd2d0dd4d', 55), ('0x8ac76a51cc950d9822d68b83fe1ad97b32cd580d', 53), ('0x0000000000004946c0e9f43f4dee607b0ef1fa1c', 43), ('0x7acf49997e9598843cb9051389fa755969e551bb', 42), ('0x56b6fb708fc5732dec1afc8d8556423a2edccbd6', 40), ('0x7130d2a12b9bcbfae4f2634d864a1ee1ce3ead9c', 35), ('0xba2ae424d960c26247dd6c32edc70b295c744c43', 34), ('0x85eac5ac2f758618dfa09bdbe0cf174e7d574d5b', 28), ('0x5c25c7bc6ad513ce4f83c7a6a83229a7971c7844', 25), ('0xf82b6c89a1d3340733ea4f74f9d111b5d7127876', 21), ('0xb86abcb37c3a4b64f74f59301aff131a1becc787', 20), ('0x48a5a1a69ed94775355a61410e8c2f8ee814905e', 20), ('0x9f589e3eabe42ebc94a44727b3f3531c0c877809', 19), ('0x8fbb18afd47ba2251dff9d6556352275c453bbf6', 19), ('0x516ffd7d1e0ca40b1879935b2de87cb20fc1124b', 16), ('0x5c29d86e685aede928a1fb838702939e67eb178e', 16), ('0x7e624fa0e1c4abfd309cc15719b7e2580887f570', 15), ('0xaef0d72a118ce24fee3cd1d43d383897d05b4e99', 15), ('0xdaf74304d685b6f40e1e8610d84aa137bf20b5cf', 15), ('0x1f9f6a696c6fd109cd3956f45dc709d2b3902163', 14), ('0x7083609fce4d1d8dc0c979aab8c869ea2c873402', 13), ('0x11111112542d85b3ef69ae05771c2dccff4faa26', 12), ('0x05ff2b0db69458a0750badebc4f9e13add608c7f', 11), ('0xdaaebc5fb20f59c0b87a1f6eafd885335ad061c2', 10), ('0x1af3f329e8be154074d8769d1ffa4ee058b1dbc3', 9), ('0x8ff795a6f4d97e7887c79bea79aba5cc76444adf', 9), ('0x16939ef78684453bfdfb47825f8a5f714f12623a', 9), ('0xcf6bb5389c92bdda8a3747ddb454cb7a64626c63', 9), ('0x3ae4222d06dacba3618526359a25bee8aecdbd92', 8), ('0xbbe054e0133e912367ac364b1cdb08451d4feb76', 8), ('0xe3dd11ff84b5bf2805638d6a5f13723e32d5d46c', 8), ('0xe02df9e3e622debdd69fb838bb799e3f168902c5', 7), ('0xcc42724c6683b7e57334c4e856f4c9965ed682bd', 7), ('0xb59490ab09a0f526cc7305822ac65f2ab12f9723', 7), ('0x0000000000000000000000000000000000002000', 6), ('0xd6c3ab79fb514b69bb5de2db10b3dd61d9f552ce', 6), ('0xa80240eb5d7e05d3f250cf000eec0891d00b51cc', 6), ('0xca0a9df6a8cad800046c1ddc5755810718b65c44', 6), ('0x8519ea49c997f50ceffa444d240fb655e89248aa', 6), ('0x8d4daba34c92e581f928fca40e018382f7a0282a', 6), ('0x86e7417b5c613c084ac52e82fea7547ef8478bfe', 6), ('0x96dd399f9c3afda1f194182f71600f1b65946501', 5), ('0x78650b139471520656b9e7aa7a5e9276814a38e9', 5), ('0x4b3b4120d4d7975455d8c2894228789c91a247f8', 5), ('0xd41fdb03ba84762dd66a0af1a6c8540ff1ba5dfb', 5), ('0x9a319b959e33369c5eaa494a770117ee3e585318', 5), ('0xaf0000d4b3390000cea10023bb1b5c6c7cf8fc4d', 4), ('0xa7f552078dcc247c2684336020c03648500c6d9f', 4), ('0xe9f6de652222024e217f81c873c4e6e76dec0996', 4), ('0x6bff4fb161347ad7de4a625ae5aa3a1ca7077819', 4), ('0x9678e42cebeb63f23197d726b29b1cb20d0064e5', 4), ('0x39bea96e13453ed52a734b6aceed4c41f57b2271', 4), ('0x8257d16767050a6acee7f150c7bc86e2b3e47b6a', 4), ('0x7969dc3c6e925bccbea9f7fc466a63c74f0115b8', 3), ('0x47bead2563dcbf3bf2c9407fea4dc236faba485a', 3), ('0xca3f508b8e4dd382ee878a314789373d80a5190a', 3), ('0x250632378e573c6be1ac2f97fcdf00515d0aa91b', 3), ('0x058451c62b96c594ad984370eda8b6fd7197bbd4', 3), ('0xe4ca1f75eca6214393fce1c1b316c237664eaa8e', 3), ('0x7c17c8bed8d14bacce824d020f994f4880d6ab3b', 3), ('0x7c9e73d4c71dae564d41f78d56439bb4ba87592f', 3), ('0x6b8220898d01676705bbc118805d29bc0db0fa3c', 3), ('0xf88ac94f7f3fb4547bd16598d549fa1df0a22126', 3), ('0x0000000000000000000000000000000000001003', 2), ('0x8578eb576e126f67913a8bc0622e0a22eba0989a', 2), ('0x2af45a200ce862c3a0acdec17e5c637f41c5e0af', 2), ('0x762539b45a1dcce3d36d080f74d1aed37844b878', 2), ('0xad6caeb32cd2c308980a548bd0bc5aa4306c6c18', 2), ('0x51ba0b044d96c3abfca52b64d733603ccc4f0d4d', 2), ('0x0952ddffde60786497c7ced1f49b4a14cf527f76', 2), ('0xa527a61703d82139f8a06bc30097cc9caa2df5a6', 2), ('0xf78d2e7936f5fe18308a3b2951a93b6c4a41f5e2', 2), ('0x73feaa1ee314f8c655e354234017be2193c9e24e', 2), ('0x5acc84a3e955bdd76467d3348077d003f00ffb97', 2), ('0x7934df2b0364400725c44e71fa679be66172ac96', 2), ('0x61e36fc4340823a0236e287f95eb4542c0e73a81', 2), ('0xdbc1a13490deef9c3c12b44fe77b503c1b061739', 2), ('0x530f1a56063a27c6c19b047c977d2860c0168400', 2), ('0xd7562e691336a4d273deffe9b8ea69253abf71c1', 2), ('0x063ba25ac8ee03b2cf2d171b70127a5145d95b9e', 2), ('0x699850dfda34e84bfd6db9d5ec7bf4c09887f9e8', 2), ('0x7d86b9ecdfaa0b46f560e2b092771ea71e44bbed', 2), ('0x7dae51bd3e3376b8c7c4900e9107f12be3af1ba8', 1), ('0x3806aae953a3a873d02595f76c7698a57d4c7a57', 1), ('0xf62723f8b7bf9962d9577f099e7bb1bdf9715610', 1), ('0xd555c120509741032d1993cd227f23668b363469', 1), ('0x5c8d727b265dbafaba67e050f2f739caeeb4a6f9', 1), ('0x46d502fac9aea7c5bc7b13c8ec9d02378c33d36f', 1), ('0x27b6031e9cbb9a383acf2f7d7168ba052ccaecfb', 1), ('0x9cd0daac9d1caa9e937fc5bb4e1c0e058d9b6f94', 1), ('0x89c95071a7d955bd96485e82c57dc326b2d7cb72', 1), ('0xf5542a5d4c1fcdf8aa1b64303ac26dbeb59bf4d0', 1), ('0xd3bc1b39dfaa4788a6bf38142a05d776bfd82ace', 1), ('0xe486a69e432fdc29622bf00315f6b34c99b45e80', 1), ('0x7c13e5ad5376377af22d1d7c588e3780189db504', 1), ('0x790641a07865e570116b8f3c6c3482b9cac67b6d', 1), ('0x0895196562c7868c5be92459fae7f877ed450452', 1), ('0xa9a438b8b2e41b3bf322dba139af9490dc226953', 1), ('0xee8feaee52ce378ba356a5772bba29d08af25cdb', 1), ('0xf0dcf19a9eff191b046c562cf3a5cb00fde853d6', 1), ('0xe5c0c004abf5585dcacf95893c5866cf59f59b9c', 1), ('0xcca790ff9680930f44c6ae163c120555d38effa1', 1), ('0x3e532b4266a779de401297336d8de6dd099745a9', 1), ('0xad162ede177e26eb31b149a7dbc1546fcd508078', 1), ('0x3999565294ca158d3d7cde9c74c86be928317ea0', 1), ('0x0d6b56327bf69657462c4648ff3059a2f9383be9', 1), ('0x50f627128ac71c5416fcb95482f2eb47c9f2f171', 1), ('0x857b222fc79e1cbbf8ca5f78cb133d1b7cf34bbd', 1), ('0xe9d1d2a27458378dd6c6f0b2c390807aed2217ca', 1), ('0xfc3069296a691250ffdf21fe51340fdd415a76ed', 1), ('0x13a72f3363776b64a7b03257dd55d41fe95ed962', 1), ('0x126a02306d37c418d198b4449e66220821144e0c', 1), ('0x78d443d733ca32d108d906275bd04507dd119bae', 1), ('0x656730bf39023ef5a55aade2b285ede84bd0892a', 1), ('0x36e4ef865aec21a7bfd969b4f2e9f807842c102d', 1), ('0x683c6e225162eef977ab05a6c9dc93cf95da0396', 1), ('0x319bf3bb8ab93658074be595c4aa55cd60380af7', 1), ('0x96058f8c3e16576d9bd68766f3836d9a33158f89', 1), ('0x291083c8aedfc3cd0384494e1fcdcf2067d28d3e', 1), ('0x8effbee6964a9396d209cf7109a4066e87010e9b', 1), ('0x01eaedd1bc5f8198d174532aa13ba150653e0e11', 1), ('0x1f546ad641b56b86fd9dceac473d1c7a357276b7', 1), ('0x34dbe8e5faefabf5018c16822e4d86f02d57ec27', 1), ('0x0fe07dbd07ba4c1075c1db97806ba3c5b113cee0', 1), ('0xc3ab35d3075430f52d2636d08d4f29bd39a18b65', 1), ('0x1610bc33319e9398de5f57b33a5b184c806ad217', 1), ('0xd487fbe16fd7ac53a9dbe287d05795246bf14daa', 1), ('0x5c17b2ed709ccdf381f599dee3cdec6e20aa4c6a', 1), ('0xf40c1f421ee02a550afdd8712ef34dce97eec6f2', 1), ('0x5164b689ebecf0f5186969d410919092620c1f1f', 1), ('0x728c5bac3c3e370e372fc4671f9ef6916b814d8b', 1), ('0x595ce6006dcae4239b536f4fecb8751328ce5725', 1), ('0x5840ca6063025f50ff0d029135226728520b9e75', 1), ('0x57ef4e6680b3f6ff3c76559aebed594be457e76a', 1), ('0xbe84c954bbc37e3e62a7420cf395979a2b86d129', 1), ('0xbd01e8c1a67f53706bcab9bc96635cd3fbf3db79', 1), ('0xdfaa0e08e357db0153927c7eabb492d1f60ac730', 1), ('0xf307910a4c7bbc79691fd374889b36d8531b08e3', 1), ('0x46a35829d0a45f5221f211efd7de8591de2527ce', 1), ('0x7ff607c572f02ed79c0de4d92541982f76c25dca', 1), ('0x20ef20c996a1f34473e6f9f5176e21369fc20575', 1), ('0x81712fa99a0d9c3412b2f97636befcc83da2c0ac', 1), ('0x325995779738e2b78eca1a72dd1b763390a73e84', 1), ('0x96d529314765e49245a2a5a63a01dcd59f547be1', 1), ('0xaee234825dc4687fae606485c1ebd06336052bcc', 1), ('0xc070c8ae94977f78d04553d33449def944f24254', 1), ('0x00e7daf0e5fd1f5331c92d09e3c825a8e4fc6515', 1), ('0x4a37a2d3ec44f0fd7ddcf7c2d90749ddeefb6101', 1), ('0x08fc9ba2cac74742177e0afc3dc8aed6961c24e7', 1), ('0x0eef8931ec9de2619ca4b8c39840cf943323f54c', 1), ('0x08bba42794b1511e24831dc26877f81f5fdc20b3', 1), ('0x1494f9dfd48c4621ea8a925ac46b0ae0fac3d593', 1), ('0x93b328c301efb5182f5975b55f661527ed3ce3e6', 1), ('0x5136d1d7e4b80b6091b5f4ffae71ff820141351d', 1), ('0x821d0a40ae9cf0bdd7477244b05cf0371817681a', 1), ('0xb4a36843b9e9f4b4d078a7e279b7eb0bdb7d845f', 1), ('0x43c934a845205f0b514417d757d7235b8f53f1b9', 1), ('0xcdfd45f965de9932367833ca7187e4c9c43a2380', 1), ('0xe365d0172a39f83660282debb6ab7dfae7beda3e', 1), ('0x4d49da5e815133713fb029f37cf2deb35d4edac5', 1), ('0xc409ec8a33f31437ed753c82eed3c5f16d6d7e22', 1), ('0x9dceb1d92f7e0361d0766f3d98482424df857654', 1), ('0x55240890ab00a5fe4f12f77ae376923d574c8bba', 1), ('0x8cd6e29d3686d24d3c2018cee54621ea0f89313b', 1), ('0xfd80ec1450c4ea9241ce18a1b90f5cd3c65dd521', 1), ('0xbaf4f119b2956932d997b531de5436b9b998e27e', 1), ('0xc9168f358de91908ba2449625281b18a64fd26f8', 1), ('0xff96ce2cc0d20da0250a63bdca2b568f52a5bc71', 1), ('0xfeab3b2b9eba8b82e3f3d3d7b525b94a6de71c8b', 1), ('0x5b07b8df127276216ed6f2c6d8a181388cf5b794', 1), ('0xcd035c0c9f68392b88ddc127f7aad39d5f39cee6', 1), ('0x935a544bf5816e3a7c13db2efe3009ffda0acda2', 1), ('0x3074b9dea4d4729934846d3af65147b65cdd5d55', 1), ('0x64cc7ed01fa6b6d3e587e9c89da04ddbebe07580', 1), ('0xc18f998f173bd5a3b061d8e63798a490fa3d9235', 1), ('0xe84a0bd65f4d7135666f3c082d9dbaaba76e6ca7', 1), ('0xfb5833f486679f3e3df0c93c33e6d21fc312913a', 1), ('0x4b0f1812e5df2a09796481ff14017e6005508003', 1), ('0x171a9377c5013bb06bca8cfe22b9c007f2c319f1', 1), ('0x173c3c5bfb4c7b46ef5cc392ef502c454bcabc4f', 1), ('0x56979af35ddbce14f5dbba1571cafb9a35d48401', 1), ('0x74cfd109898fe125737e8081d2a8df4f318305cc', 1), ('0x085f5c396f419040b0687eb885fe9973fc23cf8a', 1), ('0x3f648151f5d591718327aa27d2ee25edf1b435d8', 1), ('0xeec29f49b8eeb8722e93cca549a4e8ec8bf12779', 1), ('0xee2368efc03583c80541e2e19d36a58962be3a0e', 1), ('0x1796ae0b0fa4862485106a0de9b654efe301d0b2', 1), ('0xd0842b8a83e3ffd988f589ad778c5cf4e142f20b', 1), ('0x0000000000000000000000000000000000001004', 1), ('0x326733c35fb9426358ba9d40f7416fcefb0283da', 1), ('0x4338665cbb7b2485a8855a139b75d5e34ab0db94', 1), ('0x0b771e34526886d9fff8e764cf557d1cb5943c89', 1), ('0x325e343f1de602396e256b67efd1f61c3a6b38bd', 1), ('0xf8a0bf9cf54bb92f17374d9e9a321e6a111a51bd', 1), ('0xf661e99c8d4ec92eb462e8dcbf24a221fd467f35', 1), ('0x49bbb345c432b9b66b407f1525a81a84f4509b8b', 1), ('0xcb3aad0ff6d0da972d1252fb2b369d7bb04b19b8', 1), ('0xcf5cb782633f527395d106a4388889e23ea13ddd', 1), ('0x1e8b5abcba7905055bf07a687bb19b694be16dc8', 1), ('0x7159b835cbeb8d01136d6cc321018b60ccec4b30', 1), ('0x33adbf5f1ec364a4ea3a5ca8f310b597b8afdee3', 1), ('0x07af67b392b7a202fad8e0fbc64c34f33102165b', 1), ('0x9287f5ad55d7ee8eae90b865718eb9a7cf3fb71a', 1), ('0xc8ce49372246c2637cf77bdd4f9198835f433dcb', 1), ('0xd116e286b039634f4863481abadb1871b4e0c2cd', 1), ('0xac51066d7bec65dc4589368da368b212745d63e8', 1), ('0x3fdc66b30f5134c381cf45b0e7c604acc65b8ec9', 1), ('0xacfc95585d80ab62f67a14c566c1b7a49fe91167', 1), ('0x346b08feeca0765e51147ce1aa16ede3da27568f', 1), ('0x15289a830d7caaaf4c3ecf556b8c39e89924f626', 1), ('0xfede52617df2b876aca9d58af2e46eb119cf63f1', 1)
    ]

    for address, trans_qry in pending_wallets:

        address = Web3.toChecksumAddress(address)

        if address in tokens.keys():
            print(address, tokens[address]['name'])
        elif dm.dex_by_address(address) is not None:
            dex = dm.dex_by_address(address)
            print(trans_qry, dex.__class__)
        else:
            print(trans_qry, address)
