from tortoise.models import Model
from tortoise.expressions import Q
from tortoise import fields


from fastapi import HTTPException, status
from passlib.context import CryptContext
from typing_extensions import Self
from typing import Tuple, Union
from datetime import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Users(Model):
    id = fields.UUIDField(pk=True)
    first_name = fields.CharField(max_length=50)
    last_name = fields.CharField(max_length=50)
    email = fields.CharField(max_length=50)
    username = fields.CharField(max_length=50)
    hashed_password = fields.CharField(max_length=100)
    # False if not validate email or if deactivate email
    # True if active
    
    active = fields.BooleanField(default=False)
    deactivate_date_start = fields.DateField(null=True)
    deactivate_date_end = fields.DateField(null=True)
        
    
    @staticmethod
    def verify_password(plain_password, hashed_password) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def get_password_hash(password) -> str:
        return pwd_context.hash(password)
    
    @classmethod
    async def register_new_user(
        cls, 
        first_name: str, 
        last_name: str, 
        email: str, 
        username: str, 
        password: str, 
        *args,
        **kwargs
    ) -> Tuple[Union[str, Self], bool]:
        """Valitate if email and user not exists and create

        Args:
            first_name (str): first name
            last_name (str): last name
            email (str): email
            username (str): username
            password (str): password

        Returns:
            Tuple[Union[str, Self], bool]: User or detail and bool 
        """
        user = locals()
        del user['cls']
        del user['args']
        del user['kwargs']
        
        user_exist = await cls.filter(email=email).first()
        if user_exist:
            return 'email already used', False
        
        user_exist = await cls.filter(username=username).first()
        if user_exist:
            return 'username already used', False
        
        user['hashed_password'] = cls.get_password_hash(password=user.pop('password'))
        
        return await cls.create(**user), True
    
    @classmethod
    async def get_authenticated_user(cls, username: str) -> Union[None, Self]:
        """Verify if has user by username or email and return it.

        Args:
            password (str): password
            username (str): email or username

        Returns:
            Union[None, Self]: None or object Users
        """
        user = await cls.filter(
            Q(email=username) | Q(username=username)).first()
        
        if not user:
            return None
        return user
    
    @classmethod
    async def get_user(cls, id: str) -> Self:
        """
        Return user by id

        Args:
            id (uuid4): id type uuid4

        Returns:
            Self: object Users
        """
        user = await cls.filter(id=id).first()
        if not user:
            return None
        return user
    
    @classmethod
    async def update_by_id(cls, id: str, **kwargs) -> bool:
        
        user = await cls.filter(id=id).first()
        for key, value in kwargs.items():
            
            # validations 
            # infos can not by repeat
            if key in ['email', 'username']:
                filter_user = await cls.filter(**{key:value}).first() 
                if filter_user:
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail=f'{key} {value} already in use'
                    )
                
            setattr(user, key, value)
            if not getattr(user, key) == value:
                return False
            
        await user.save()
        return True
    
    @classmethod
    async def deactivate_user(cls, id: str):
        user = await cls.filter(id=id).first()
        
        if not user:
            return False
        
        user.active = False
        user.deactivate_date_start = datetime.now().date()
        
        user.save()
        
        return True