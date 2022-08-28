from fastapi import (
    APIRouter, 
    HTTPException,
    status,
    Depends
)

from models.users import Users

from schemas.accounts import Account, AccountConfigs, AccountId

from utils.token_auth import user_auth_token

router = APIRouter()

@router.get('/configs', response_model=Account)
async def get_users_configs(account: Account = Depends(user_auth_token)):
    """
        Return config infos about specified account.
    """
    return account

@router.put('/update', response_model=Account)
async def update_users_configs(update_infos: AccountConfigs, account: AccountId = Depends(user_auth_token)):
    """
        Update infos of user account.
    """
    items = {}
    
    # implement logic filter to correct way to update infos in db
    # in this case only update in users db
    # filter infos that is not None
    for key, value in update_infos.dict().items():
        if value and key != 'deactivate':
            items[key] = value
            setattr(account, key, value)
    
    if not items:
        raise HTTPException(
            status_code=status.HTTP_426_UPGRADE_REQUIRED,
            detail='uprocessable update'
        )
    
    status_update = await Users.update_by_id(id=account.id, **items)
    
    if not status_update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='uprocessable update'
        )
    
    return account

@router.put('/deactivate')
async def deactivate_account(account: AccountId = Depends(user_auth_token)):
    """
        Validate and update account status active to false. 
        The account and user infos will be deleted by the robot after expired date of specified days.  
    """
    
    # validate if users has pendencies
    # if has first resolve the pendencies 
    # and after deactivate account
    
    return {}
    