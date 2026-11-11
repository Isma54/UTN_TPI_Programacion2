from entidades.base import Base
from enums.enumerados import Rol
from excepciones.food_store_error import DatoInvalidoError

class Usuario(Base):
    def __init__(self,nombre:str,apellido:str,mail:str,celular:str,contrasenia:str,rol:Rol)->None:
        super().__init__()
        self.nombre = nombre
        self.apellido = apellido
        self.mail = mail
        self.celular = celular
        self.actualizar_contrasenia(contrasenia)
        self.rol = rol

    @property
    def nombre(self)->str:
        return self.__nombre
    @property
    def apellido(self)->str:
        return self.__apellido
    @property
    def mail(self)->str:
        return self.__mail
    @property
    def celular(self)->str:
        return self.__celular
    @property
    def rol(self)->Rol:
        return self.__rol

    @nombre.setter
    def nombre(self,nombre:str)->None:
        if not isinstance(nombre,str):
            raise DatoInvalidoError("El nombre del usuario debe ser de una cadena de texto")
        if nombre.strip() == "":
            raise DatoInvalidoError("El nombre del usuario no puede quedar vacio")
        self.__nombre = nombre.strip()

    @apellido.setter
    def apellido(self,apellido:str)->None:
        if not isinstance(apellido,str):
            raise DatoInvalidoError("El apellido del usuario debe ser una cadena de texto")
        if apellido.strip() == "":
            raise DatoInvalidoError("El apellido del usuario no puede quedar vacio")
        self.__apellido = apellido.strip()

    @mail.setter
    def mail(self,mail:str)->None:
        if not isinstance(mail,str):
            raise DatoInvalidoError("El mail del usuario debe ser una cadena de texto")
        if mail.strip() == "":
            raise DatoInvalidoError("El mail no puede quedar vacio")
        if "@" not in mail or "." not in mail:
            raise DatoInvalidoError("El mail ingresado no tiene un formato valido")
        self.__mail = mail.strip().lower()

    @celular.setter
    def celular(self,celular:str)->None:
        if not isinstance(celular,str):
            raise DatoInvalidoError("El celular del usuario debe ser una cadena de texto")
        if celular.strip() == "":
            raise DatoInvalidoError("EL celular del usuario no puede quedar vacio")
        self.__celular = celular.strip()

    @rol.setter
    def rol(self,rol:Rol)->None:
        if not isinstance(rol,Rol):
            raise DatoInvalidoError("El rol del usuario debe ser instancia de la clase Rol")
        self.__rol = rol

    def verificar_contrasenia(self,contrasenia:str)->bool:
        if contrasenia == self.__contrasenia:
            return True
        return False

    def actualizar_contrasenia(self,contrasenia:str)->None:
        if not isinstance(contrasenia,str) or not contrasenia or len(contrasenia.strip()) < 3:
            raise DatoInvalidoError("La contrasenia es muy corta o tiene un formato incorrecto")
        self.__contrasenia = contrasenia.strip()
        
    def __str__(self)->str:
        return f"ID: {self.id} | {self.nombre} {self.apellido} | {self.mail} | {self.rol.name}"