from starlette import status
from starlette.responses import JSONResponse

from auth.auth_handler import AuthHandler
from dbs.mongodb import mongodb
from helpers.hashing import Hash
from helpers.key_generator import KeyGenerator
from helpers.response_handler import ResponseHandler
from models.key_token_model import KeyToken
from models.shop_model import Shop, ShopRole
from services.key_token_service import KeyTokenService


class ShopService:
    @staticmethod
    async def sign_up(request: Shop):
        request = request.model_dump()
        collection = mongodb[Shop.__collection_name__]

        existed_shop = collection.find_one({'email': request['email']})

        if existed_shop:
            content = {
                'message': 'Email is already registered',
                'code': 'EMAIL_IS_ALREADY_REGISTERED',
            }
            return JSONResponse(content=content, status_code=status.HTTP_400_BAD_REQUEST)

        hashed_password = await Hash.bcrypt(request['password'])
        roles = [ShopRole.SHOP]
        shop_data = {'name': request['name'], 'email': request['email'], 'password': hashed_password, 'roles': roles}
        new_shop = Shop(**shop_data)

        if new_shop:
            private_key, public_key = await KeyGenerator.generate_rsa_keypair()
            public_key_pem = await KeyGenerator.create_public_key_pem(public_key)

            key_token = await KeyTokenService.create_key_token(new_shop.id, public_key_pem)
            if not key_token.public_key:
                content = {
                    'message': 'Public key is null',
                    'code': 'PUBLIC_KEY_IS_NULL',
                }
                return JSONResponse(content=content, status_code=status.HTTP_400_BAD_REQUEST)

            payload = {
                'id': str(new_shop.id),
                'email': new_shop.email,
            }
            access_token, refresh_token = await AuthHandler.create_token_pair(payload=payload, public_key=public_key, private_key=private_key)

            new_shop_dict = new_shop.model_dump(by_alias=True)
            collection.insert_one(new_shop_dict)

            key_token_dict = key_token.model_dump(by_alias=True)
            collection = mongodb[KeyToken.__collection_name__]
            collection.insert_one(key_token_dict)

            content = {
                'message': 'Created successfully',
                'metadata': {
                    'shop': await ResponseHandler.response_data(obj=new_shop_dict, fields=('_id', 'name', 'email')),
                    'tokens': {
                        'access_token': access_token,
                        'refresh_token': refresh_token,
                    },
                },
            }
            return JSONResponse(content=content, status_code=status.HTTP_201_CREATED)

        content = {
            'message': 'Unable to create new shop',
            'code': 'UNABLE_TO_CREATE_NEW_SHOP',
        }
        return JSONResponse(content=content, status_code=status.HTTP_400_BAD_REQUEST)
