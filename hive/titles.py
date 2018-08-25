from hive.txio import get_asset_attachments
from boa.interop.Neo.Runtime import CheckWitness, Notify
from boa.interop.Neo.Action import RegisterAction
from boa.interop.Neo.Storage import *
from boa.builtins import concat

def handle_titles(ctx, operation, args):
    if operation == 'registerTitle':
        if len(args) == 2:
            t_owner = args[0]
            orig_title = args[1]
            register = DoRegisterTitle(t_owner, orig_title)
            return register
        return False
    
    elif operation == 'giveTitle':
        if len(args) == 3:
            t_owner = args[0]
            t_receiver = args[1]
            orig_title = args[2]
            give = DoGiveTitle(t_owner, t_receiver, orig_title)
            return give
        return False

    elif operation == 'increaseTitleAmount':
        if len(args) == 3:
            t_owner = args[0]
            orig_title = args[1]
            amount = args[2]
            increase = DoIncreaseTitleAmount(t_owner, orig_title, amount)
            return increase
        return False

"""
Original Smart Contract
"""

def DoRegisterTitle(t_owner, orig_title):
    """
    Method to register a title

    :param t_owner: owner of token
    :param orig_title: original title name
    :return: bool
    """
    owner_is_sender = CheckWitness(t_owner)

    if not owner_is_sender:
        Log("Incorrect permission")
        return False

    context = GetContext()

    # ここで，返金処理を入れる必要がある．
    # とりあえず，省く

    ## 称号が存在しないかチェック
    if Get(context, t_owner + orig_title + b'name'):
        # 存在したら，エラー
        return False
    else:
        # 存在しない場合，称号を登録する
        Put(context, t_owner + orig_title + b'name', orig_title)
        Put(context, t_owner + orig_title + b'amount', 100) # 支払われたGas(NEO)に対応した量にする

    return True


def DoGiveTitle(t_owner, t_receiver, orig_title):
    """
    Method to register a title

    :param t_owner: owner of token
    :param t_receiver: receiver of token
    :param orig_title: original title name
    :return: bool
    """
    owner_is_sender = CheckWitness(t_owner)

    if not owner_is_sender:
        Log("Incorrect permission")
        return False

    context = GetContext()

    # すでに称号を持っていないかチェック
    if Get(context, t_receiver + orig_title + b'name'):
        # すでに持っていたら
        return False
    else:
        # 持っていなかったら
        current_balance = Get(context, t_owner + orig_title + b'amount')
        Put(context, t_owner + orig_title + b'amount', current_balance - 1)
        Put(context, t_receiver + orig_title + b'name', orig_title)

    return True

def DoIncreaseTitleAmount(t_owner, orig_title, amount):
    """
    Method to register a title

    :param t_owner: owner of token
    :param orig_title: original title name
    :param amount: amount of title
    :return: bool
    """
    owner_is_sender = CheckWitness(t_owner)

    if not owner_is_sender:
        Log("Incorrect permission")
        return False

    context = GetContext()

    ## 称号が存在するかチェック
    if Get(context, t_owner + orig_title + b'name'):
        # 存在したら，増やす
        current_balance = Get(context, t_owner + orig_title + b'amount')
        Put(context, t_owner + orig_title + b'amount', current_balance - 100)   # 支払われたGas(Neo)に対応した量を増やす
    else:
        # 存在しない場合，エラー
        return False

    return True