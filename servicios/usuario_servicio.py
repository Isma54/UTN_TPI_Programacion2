from entidades.usuario import Usuario
from enums.enumerados import Rol
from excepciones.food_store_error import EntidadNoEncontradaError,DuplicadoError,CredencialesInvalidasError,OperacionNoPermitidaError,DatoInvalidoError

class UsuarioServicio:
    def __init__(self)->None:
        self.__usuarios : list[Usuario] = []

    def _validar_admin(self,usuario_sesion: Usuario|None) -> None:
        if usuario_sesion is not None:
            if not isinstance(usuario_sesion,Usuario) and (usuario_sesion.eliminado or usuario_sesion.rol != Rol.ADMIN):
                raise OperacionNoPermitidaError("Solo un administrador puede realizar esta operacion")
        else:
            raise OperacionNoPermitidaError("Solo un administrador puede realizar esta operacion")        

    def listar(self,usuario_sesion: Usuario)->list[Usuario]:
        self._validar_admin(usuario_sesion)
        return [u for u in self.__usuarios if not u.eliminado]

    def buscar_por_id(self,id_usuario:int)->Usuario:
        for u in self.__usuarios:
            if id_usuario == u.id and not u.eliminado:
                return u
        raise EntidadNoEncontradaError(f"No se encontro el usuario con id: {id_usuario}")

    def crear_administrador_inicial(self,nombre:str,apellido:str,mail:str,celular:str,contrasenia:str)->Usuario:
        if self.__usuarios:
            raise OperacionNoPermitidaError("El administrador inicial ya fue creado")
        administrador = Usuario(nombre,apellido,mail,celular,contrasenia,Rol.ADMIN)
        self.__usuarios.append(administrador)
        return administrador
    
    def crear_usuario(self,nombre:str,apellido:str,mail:str,celular:str,contrasenia:str,rol:Rol,usuario_sesion : Usuario|None = None)->Usuario:
        self._validar_admin(usuario_sesion)
        if not isinstance(mail,str):
            raise DatoInvalidoError("El mail debe ser una cadena de texto")
        mail_limpio = mail.strip().lower()
        for u in self.__usuarios:
            if mail_limpio == u.mail:
                raise DuplicadoError("El mail ingresado ya se encuentra registrado")
        usuario= Usuario(nombre,apellido,mail_limpio,celular,contrasenia,rol)
        self.__usuarios.append(usuario)
        return usuario

    def autenticar(self,mail:str,contrasenia:str)->Usuario:
        if not isinstance(mail,str) or not isinstance(contrasenia,str):
            raise CredencialesInvalidasError("Mail o contraseña incorrectos")
        mail_limpio = mail.strip().lower()
        for u in self.__usuarios:
            if mail_limpio == u.mail:
                if u.verificar_contrasenia(contrasenia):
                    return u
        raise CredencialesInvalidasError("Mail o contraseña incorrectos")

    def editar(self,id_usuario:int,nombre:str=None,apellido:str=None,mail:str=None,celular:str=None,contrasenia:str=None,rol:Rol=None,usuario_sesion: Usuario|None = None)->Usuario:
        self._validar_admin(usuario_sesion)
        usuario = self.buscar_por_id(id_usuario)
        if id_usuario == usuario_sesion.id and rol is not None and rol != Rol.ADMIN:
            raise OperacionNoPermitidaError("Un administrador no puede quitarse el rol ADMIN mientras tiene su sesion iniciada")            
        if mail is not None:
            if not isinstance(mail,str):
                raise DatoInvalidoError("El mail debe ser una cadena de texto")
            mail_limpio= mail.strip().lower()
            for u in self.__usuarios:
                if id_usuario != u.id and mail_limpio == u.mail:
                    raise DuplicadoError("El mail ya pertenece a otro usuario")
            usuario.mail = mail_limpio
        if nombre is not None:
            usuario.nombre = nombre
        if apellido is not None:
            usuario.apellido = apellido
        if celular is not None:
            usuario.celular = celular
        if contrasenia is not None:
            usuario.actualizar_contrasenia(contrasenia)
        if rol is not None:
            usuario.rol = rol
        return usuario

    def eliminar(self,id_usuario:int,usuario_sesion:Usuario)->None:
        self._validar_admin(usuario_sesion)
        usuario = self.buscar_por_id(id_usuario)
        if usuario.id == usuario_sesion.id:
            raise OperacionNoPermitidaError("Un administrador no puede eliminarse a si mismo mientras tiene su sesion iniciada")
        usuario.eliminar()