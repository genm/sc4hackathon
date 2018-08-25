from hive.txio import get_asset_attachments
from boa.interop.Neo.Runtime import CheckWitness, Notify
from boa.interop.Neo.Action import RegisterAction
from boa.interop.Neo.Storage import *
from boa.builtins import concat

def handle_degrees(context, operation, args):
    if operation == 'registerDegree':
        if len(args) == 2:
            t_owner = args[0]
            orig_degree = args[1]
            register = DoRegisterDegree(t_owner, orig_degree)
            return register
        return False
    
    elif operation == 'giveDegree':
        if len(args) == 3:
            t_owner = args[0]
            t_receiver = args[1]
            orig_degree = args[2]
            give = DoGiveDegree(t_owner, t_receiver, orig_degree)
            return give
        return False

    elif operation == 'increaseDegreeAmount':
        if len(args) == 3:
            t_owner = args[0]
            orig_degree = args[1]
            amount = args[2]
            increase = DoIncreaseDegreeAmount(t_owner, orig_degree, amount)
            return increase
        return False

"""
Original Smart Contract
"""

def DoRegisterDegree(t_owner, orig_degree):
    """
    Method to register a degree

    :param t_owner: owner of token
    :param orig_degree: original degree name
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
    if Get(context, concat( t_owner , concat( orig_degree , b'name'))):
        # 存在したら，エラー
        return False
    else:
        # 存在しない場合，称号を登録する
        attachments = get_asset_attachments()
        print(attachments[3])
        if attachments[3] / 100000000 < 500:
            return False
        amount = get_amount_register(attachments[3] / 100000000 )

        Put(context, concat( t_owner , concat( orig_degree , b'name')), orig_degree)
        print( concat( orig_degree , b'name') )
        print( orig_degree )
        print( t_owner )
        print( concat( t_owner , concat( orig_degree , b'name' ) ) )
        Put(context, concat( t_owner , concat( orig_degree , b'amount')), amount)

    return True


def DoGiveDegree(t_owner, t_receiver, orig_degree):
    """
    Method to register a degree

    :param t_owner: owner of token
    :param t_receiver: receiver of token
    :param orig_degree: original degree name
    :return: bool
    """
    owner_is_sender = CheckWitness(t_owner)

    if not owner_is_sender:
        Log("Incorrect permission")
        return False

    context = GetContext()

    # すでに称号を持っていないかチェック
    if Get(context, concat(t_receiver , concat( orig_degree , b'name'))):
        # すでに持っていたら
        return False
    else:
        # 持っていなかったら
        current_balance = Get(context, concat( t_owner , concat(orig_degree , b'amount')))
        if current_balance == 0 :
            return False
        Put(context, concat(t_owner , concat( orig_degree , b'amount')), current_balance - 1)
        Put(context, concat(t_receiver , concat( orig_degree , b'name')), orig_degree)

    return True

def DoIncreaseDegreeAmount(t_owner, orig_degree, amount):
    """
    Method to register a degree

    :param t_owner: owner of token
    :param orig_degree: original degree name
    :param amount: amount of degree
    :return: bool
    """
    owner_is_sender = CheckWitness(t_owner)

    if not owner_is_sender:
        Log("Incorrect permission")
        return False

    context = GetContext()

    ## 称号が存在するかチェック
    if Get(context, concat( t_owner , concat( orig_degree , b'name'))):
        # 存在したら，増やす
        attachments = get_asset_attachments()
        if attachments[3] / 100000000 < 100 :
            return False
        amount = get_amount_increese(attachments[3] / 100000000)
        current_balance = Get(context, concat( t_owner , concat( orig_degree , b'amount')))
        Put(context, concat( t_owner , concat( orig_degree , b'amount')), current_balance + amount)
    else:
        # 存在しない場合，エラー
        return False

    return True

def get_amount_register( attachment ):
    return attachment * 10

def get_amount_increese(attachment):
    return attachment * 10

