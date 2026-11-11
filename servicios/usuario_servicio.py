from entidades.usuario import Usuario
from enums.enumerados import Rol
from excepciones.food_store_error import EntidadNoEncontradaError,DuplicadoError,CredencialesInvalidasError,OperacionNoPermitidaError,DatoInvalidoError

class UsuarioServicio:
    def __init__(self)->None:
        self.__usuarios : list[Usuario] = []

    def listar(self)->list[Usuario]:
        return [u for u in self.__usuarios if not u.eliminado]

    def buscar_por_id(self,id_usuario:int)->Usuario:
        for u in self.__usuarios:
            if id_usuario == u.id and not u.eliminado:
                return u
        raise EntidadNoEncontradaError(f"No se encontro el usuario con id: {id_usuario}")

    def crear_usuario(self,nombre:str,apellido:str,mail:str,celular:str,contrasenia:str,rol:Rol)->Usuario:
        if not isinstance(mail,str):
            raise DatoInvalidoError("El mail debe ser una cadena de texto")
        mail_limpio = mail.strip().lower()
        for u in self.__usuarios:
            if mail_limpio == u.mail and not u.eliminado:
                raise DuplicadoError("El mail ingresado ya se encuentra registrado")
        usuario= Usuario(nombre,apellido,mail_limpio,celular,contrasenia,rol)
        self.__usuarios.append(usuario)
        return usuario

    def autenticar(self,mail:str,contrasenia:str)->Usuario:
        if not isinstance(mail,str) or not isinstance(contrasenia,str):
            raise CredencialesInvalidasError("Mail o contraseña incorrectos")
        mail_limpio = mail.strip().lower()
        for u in self.__usuarios:
            if mail_limpio == u.mail and not u.eliminado:
                if u.verificar_contrasenia(contrasenia):
                    return u
        raise CredencialesInvalidasError("Mail o contraseña incorrectos")

    def editar(self,id_usuario:int,nombre:str=None,apellido:str=None,mail:str=None,celular:str=None,contrasenia:str=None,rol:Rol=None)->Usuario:
        usuario = self.buscar_por_id(id_usuario)
        if nombre is not None and nombre.strip():
            usuario.nombre = nombre
        if apellido is not None and apellido.strip():
            usuario.apellido = apellido
        if mail is not None and mail.strip():
            mail_limpio = mail.strip().lower()
            for u in self.__usuarios:
                if id_usuario != u.id and mail_limpio == u.mail and not u.eliminado:
                    raise DuplicadoError("El mail ya pertecene a otro usuario")
            usuario.mail = mail_limpio
        if celular is not None and celular.strip():
            usuario.celular = celular
        if contrasenia is not None and contrasenia.strip():
            usuario.actualizar_contrasenia(contrasenia)
        if rol is not None:
            usuario.rol = rol
        return usuario

    def eliminar(self,id_usuario:int,id_usuario_sesion:int)->None:
        usuario = self.buscar_por_id(id_usuario)
        if usuario.id == id_usuario_sesion:
            raise OperacionNoPermitidaError("Un administrador no puede eliminarse a si mismo mientras tiene su sesion iniciada")
        usuario.eliminar()