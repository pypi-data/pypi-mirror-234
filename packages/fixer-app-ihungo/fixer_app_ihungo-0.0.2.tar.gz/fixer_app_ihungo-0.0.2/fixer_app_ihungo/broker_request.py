"""
estas clases permiten realizar acciones de autenticacion, registro,
modificación y consulta de servicios externos.
"""

import requests
import json
from abc import ABC,abstractmethod
from typing import List,Tuple,Dict,Union,Optional


class BaseServiceRequest(ABC):

    @abstractmethod
    def login(self,*args: Union[Optional[str],Dict[str,str]]):
        pass

    @abstractmethod    
    def get_headers(self,*args):
        pass

    @abstractmethod  
    def get(self,*args):
        pass 

    @abstractmethod      
    def post(self,*args):
        pass   

    @abstractmethod          
    def put(self,*args):
        pass   

    @abstractmethod      
    def delete(self,*args):
        pass      


class ServiceRequest(BaseServiceRequest):
    def login(self,url: Optional[str]=None,
              username: Optional[str]=None,
              password:Optional[str]=None,
              prefix_token: str="JWT",
              key_token: str="token",
              user_custom: Dict[str,str]={})-> Tuple[bool,str]:
        """
        este metodo se encargara de consumir los servicios de autenticacion, y obtener un token
        args:
            -url: endpoint para auntenticar el usuario
            -username: el username del usuario
            -password: la contraseña de usuario
            -prefix_token: prefijo necesario para armar el token que se usa para obtener el header
            -user_custom: diccionario que se utiliza como sustituto de 'username' y 'password', encasos especificos
                el login se realiza con 'correo' y no con 'username'. ej:
                {'correo':'correo@email.com','password':'password'}
        return:
            retorna una tupla en donde :
            - el primer argumento es un boolean que indique si el token fué valido o no.
            - el token valido que se obtine de la concatenacion del prefijo y key_token. 
        """
        data: Dict[str,str] = {'username': username,'password':password} if not user_custom else user_custom
        response: requests = requests.post(url, data=data)
        if response.status_code == 200:
            key_token = response.json()['token']            
            token_obtained: str = prefix_token + " " +key_token
            return True,token_obtained
        else:    
            token_obtained: str = prefix_token + " " +key_token
            return False,token_obtained 
      
    def get_headers(self,token):
        """
        este metodo se encarga de generar los headers, por defecto recibira como parametro el token y retornara un dicionario
        """
        header = {
            'Content-Type': 'application/json',
            "Authorization":token
        }
        return header
    
    def get(self,url,headers):
        """
        este metodo se encargara de realizar todas las solicitudes a servicios GET
        """
        response =requests.get(url=url,headers=headers)
        if response.status_code == 200:
           return response.json()
        
    def post(self, url,payload,files: Union[str,list],headers):
        """
         este metodo se encargara de realizar todas las solicitudes POST
        """
        response = requests.post(url=url,data=json.dumps(payload),files=files,headers=headers)
        if response.status_code == 201:            
            return response.json()
        else:
            respuesta = response.content.decode("utf-8")
            respuesta = json.loads(respuesta)
            return respuesta
    
    def put(self, url,payload,files,headers):
        """
         este metodo se encargara de realizar todas las solicitudes PUT
        """
        response = requests.put(url=url,data=json.dumps(payload),files=files,headers=headers)
        if response.status_code == 200:
            return response.json()

    def delete(self, url,headers):
        """
         este metodo se encargara de realizar todas las solicitudes DELETE
        """
        response =requests.delete(url=url,headers=headers)
        if response.status_code == 204:
           return "elemento eliminado"
        
class ServiceRequestSimpleJwt(ServiceRequest):

    def login(self,
              username: str=None,
              password: str=None,
              url: str=None,
              prefix_token: str="JWT",
              key_token: str="token",
              user_custom: dict ={}
            ):
        """
        este metodo se encargara de consumir los servicios de autenticacion, y obtener un token
        args:
            -url: endpoint para auntenticar el usuario
            -username: el username del usuario
            -password: la contraseña de usuario
            -prefix_token: prefijo necesario para armar el token que se usa para obtener el header
            -user_custom: diccionario que se utiliza como sustituto de 'username' y 'password', encasos especificos
                el login se realiza con 'correo' y no con 'username'. ej:
                {'correo':'correo@email.com','password':'password'}
        return:
            retorna una tupla en donde :
            - el primer argumento es un boolean que indique si el token fué valido o no.
            - el token valido que se obtine de la concatenacion del prefijo y key_token. 
        """
        data = {'username': username,'password':password} if not user_custom else user_custom
        response = requests.post(url, data=data)
        if response.status_code == 200:

            token_jwt = 'token' if 'token' in response.json() else 'access'
            refresh = 'refresh' if 'refresh' in response.json() else None
            key_token = response.json()[token_jwt]
            token_obtained: str = prefix_token + " " +key_token
            token_dict: Dict[str,str] = {"is_active":True,"access_token":token_obtained}
            if refresh:
                refresh_token = response.json()[refresh] 
                token_dict.update({"refresh_token":refresh_token})           
            return token_dict
        else:    
            token_obtained: str = prefix_token + " " +key_token
            refresh_token: str  = ''
            return {"is_active":False,"access_token":token_obtained,"refresh_token":refresh_token} 

    def get_refresh_token(self,url,refresh_token,prefix_token= "JWT"):

        data = {"refresh": refresh_token}
        response = requests.post(url, data=data)
        if response.status_code == 200:
            access_token = response.json()["access"]
            token_obtained = prefix_token + " " + access_token
            return token_obtained
        else:
            return "refresh token_invalido o en lista negra"
    