from dataclasses import dataclass
from typing import Callable, List, Optional
from httpx import Client, URL
from etsy_apiv3.models.TokenModel import Token
from etsy_apiv3.exceptions.TokenExpiredError import TokenExpiredError
from etsy_apiv3.utils.RequestException import EtsyRequestException
from etsy_apiv3.utils.EtsyListRequestException import EtsyListRequestException
from etsy_apiv3.models import Me

AUTH_CONNECT_ENDPOINT = "https://www.etsy.com/oauth/connect"
TOKEN_ENDPOINT = "https://api.etsy.com/v3/public/oauth/token"


@dataclass
class APILimit:
    limit_per_second: Optional[int]
    remaining_this_second: Optional[int]
    limit_per_day: Optional[int]
    remaining_today: Optional[int]


class EtsyOauth2Session:
    
    def __init__(self, client_id: str, token: Optional[Token] = None, token_updater: Optional[Callable] = None, extra_token_updater_args: Optional[tuple] = None) -> 'EtsyOauth2Session':
        self.headers = {
            "x-api-key": client_id
        }
        self.token = token
        
        if self.token is not None:
            if token_updater is None:
                self.token_updater = self._token_updater
            else:
                self.token_updater = token_updater
                
            self.headers["Authorization"] = f"{token.token_type} {token.access_token}"
        self.client_id = client_id
        self.client = Client(timeout=30.0)
        self.limits = APILimit(
            limit_per_second=None,
            remaining_this_second=None,
            limit_per_day=None,
            remaining_today=None
        )
        
        self.__me = None
        self.extra_token_updater_args = extra_token_updater_args
        
    @property
    def me(self) -> Me:
        if self.__me is None:
            self.__me = Me(**self.request(f"users/me"))
        return self.__me
    
    def _token_updater(self, new_token: Token, *args):
        self.token = new_token
        return True
    
    def refresh_token(self):
        data = {
            "grant_type": "refresh_token",
            "client_id": self.client_id,
            "refresh_token": self.token.refresh_token
        }
        response = self.client.post(TOKEN_ENDPOINT, data=data)
        token = Token(**response.json())
        self.headers["Authorization"] = f"{token.token_type} {token.access_token}"
        
        if self.extra_token_updater_args is not None:
            
            self.token_updater(token, *self.extra_token_updater_args)
        else:
            self.token_updater(token)
        
        return True
    
    def request(self, endpoint: str, method: str ="GET", *args, **kwargs) -> dict:
        """ method
        Send Request to target endpoint by method

        Args:
            endpoint (str): Api Endpoint Url
            method (str, optional): HTTP Methods [GET, POST, PUT, DELETE, UPDATE]. Defaults to "GET".

        Raises:
            EtsyRequestException: EtsyRequestException(status_code, message)

        Returns:
            json: Json From Request Response
        """
        base_endpoint = "https://openapi.etsy.com/v3/application/"
        url = f"{base_endpoint}{endpoint}"
        
        headers = self.headers
        if kwargs.get("headers") is not None:
            headers.update(kwargs.get("headers"))
            kwargs.pop("headers")
        
        res = self.client.request(method, url, headers=headers, *args, **kwargs)
        res_json = res.json()
        
        if "X-Limit-Per-Day" in res.headers.keys():
            
            self.limits.limit_per_day = res.headers["X-Limit-Per-Day"]
            self.limits.limit_per_second = res.headers["X-Limit-Per-Second"]
            self.limits.remaining_this_second = res.headers["X-Remaining-This-Second"]
            self.limits.remaining_today = res.headers["X-Remaining-Today"]

        
        if res.status_code in [400, 404, 500]:
            
            if isinstance(res_json, list):
                raise EtsyListRequestException(res.status_code, errors=res_json)
            
            raise EtsyRequestException(res.status_code, res_json["error"])
        
        if res.status_code == 401:
            if res_json["error"] == "invalid_token":
                updated = self.refresh_token()
                if updated:
                    return self.request(endpoint, method, *args, **kwargs)
                else:
                    raise TokenExpiredError(
                        status_code=res.status_code,
                        message=res_json["error_description"],
                        error=res_json["error"]
                    )
            
            raise EtsyRequestException(res.status_code, res_json["error"])
        
        
        return res_json
            
        


class EtsyOauth2Helper:
    
    def authorize(self, client_id: str, redirect_uri: str, scopes: List[str], state: str = "superuser", code_challange: str = None) -> str:
        authorize_url = URL(AUTH_CONNECT_ENDPOINT, params={
            "response_type": "code",
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "scope": " ".join(scopes),
            "code_challenge": code_challange,
            "state": state,
            "code_challenge_method": "S256"
        })
        print(f"Go to the following URL: {authorize_url}")
        return f"{authorize_url.scheme}://{authorize_url.host}{authorize_url.path}?{authorize_url.query.decode('utf-8')}"
    
    def authenticate(self, auth_code: str, redirect_uri: str, client_id: str, code_verifier: str) -> EtsyOauth2Session:
        client = Client(http2=False)
        data = {
            "grant_type": "authorization_code",
            "code": auth_code,
            "redirect_uri": redirect_uri,
            "client_id": client_id,
            "code_verifier": code_verifier
        }
        response = client.post(TOKEN_ENDPOINT, data=data)
        token = response.json()
        return EtsyOauth2Session(client_id, token=Token(**token))
    
