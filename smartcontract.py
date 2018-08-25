from hive.txio import get_asset_attachments
from hive.titles import *
from boa.interop.Neo.Runtime import Log, GetTrigger, CheckWitness
from boa.interop.Neo.Action import RegisterAction
from boa.interop.Neo.TriggerType import Application, Verification
from boa.interop.Neo.Storage import GetContext, Get, Put, Delete
from boa.builtins import concat

# -------------------------------------------
# TOKEN SETTINGS
# -------------------------------------------

OWNER = b'#\xba\'\x03\xc52c\xe8\xd6\xe5"\xdc2 39\xdc\xd8\xee\xe9'
# Script hash of the contract owner

TITLES = ['registerTitle','giveTitle','increaseTitleAmount']

# -------------------------------------------
# Events
# -------------------------------------------

context = GetContext()

def Main(operation, args):
    """
    This is the main entry point for the Smart Contract

    :param operation: the operation to be performed ( eg `balanceOf`, `transfer`, etc)
    :type operation: str
    :param args: a list of arguments ( which may be empty, but not absent )
    :type args: list
    :return: indicating the successful execution of the smart contract
    :rtype: bool
    """

    # The trigger determines whether this smart contract is being
    # run in 'verification' mode or 'application'

    trigger = GetTrigger()

    # 'Verification' mode is used when trying to spend assets ( eg NEO, Gas)
    # on behalf of this contract's address
    if trigger == Verification():

        # if the script that sent this is the owner
        # we allow the spend
        is_owner = CheckWitness(OWNER)

        if is_owner:

            return True

        return False

    # 'Application' mode is the main body of the smart contract
    elif trigger == Application():
        for op in NEP5_METHODS:
            if operation == op:
                return handle_titles(ctx, operation, args)

        if operation == 'deploy':
            deploy()

        result = 'unknown operation'

        return result

    return False


def deploy():
    if not CheckWitness(OWNER):
        print("Must be owner to deploy")
        return False

    if not Get(context, 'initialized'):
        # do deploy logic
        Put(context, 'initalized', 1)
        return True
    return False

