import json
from algosdk.future import transaction
from algosdk import mnemonic, account
from algosdk.v2client import algod
from utils import submit_tx

# Example account, don't use it with real funds!

# ADDRESS: 4JCU2OFYPYWWRXS3ZVTDM7T5JZGSNAPG6CLY2YZY4UY6HZZFOLW2RD2UZM
_MNEMONIC = 'office talent clap guide enact bleak glance cage defy check blood cake large bind reflect spice stock veteran donor grit sauce dynamic royal abstract improve'

def get_client():
    algod_address = 'http://localhost:4001'
    algod_token = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
    return algod.AlgodClient(algod_token, algod_address)

def get_keys():
    pk = mnemonic.to_private_key(_MNEMONIC)
    return account.address_from_private_key(pk), pk

def create_asa_txn(client, sender_addr):
    asset_name = 'NFT Seminario Tecnico'

    nft_metadata = {
        'standard': 'arc69',
        'description': 'NFT Seminario Tecnico',
        'external_url': 'ipfs://QmRRPWG96cmgTn2qSzjwr2qvfNEuhunv6FNeMFGa9bx6mQ',
        'mime_type': 'image/png',
        'properties': {
            'Earring': 'Silver Hoop', 
            'Background': 'Orange', 
            'Fur': 'Robot',
            'Clothes': 'Striped Tee',
            'Mouth': 'Discomfort',
            'Eyes': 'X Eyes'
        }
    }

    txn = transaction.AssetCreateTxn(
        sender=sender_addr,
        total=1,
        decimals=0,
        default_frozen=False,
        manager=sender_addr,
        reserve=sender_addr,
        freeze=None,
        clawback=None,
        unit_name='PLT',
        asset_name=asset_name,
        url='ipfs://QmRRPWG96cmgTn2qSzjwr2qvfNEuhunv6FNeMFGa9bx6mQ',
        note=json.dumps(nft_metadata),
        metadata_hash='',
        sp=client.suggested_params(),
    )

    return txn

if __name__ == '__main__':
    
    client = get_client()
    address, pk = get_keys()

    print('Preparazione transazione per creazione asset')
    create_asset_txn = create_asa_txn(client, address)

    print('Firma transazione')
    signed_tx = create_asset_txn.sign(pk)

    print('Invio transazione')
    response = submit_tx(client, signed_tx)

    print(f'ID nuovo ASA: {response["asset-index"]}')

