# JWT contiene tres partes separados por partes y se utiliza para transmitir información de forma segura entre dos partes. Estas partes son:
# 1. Header: Contiene información sobre el tipo de token y el algoritmo de firma utilizado.
# 2. Payload: Contiene las declaraciones (claims) que representan la información que se desea transmitir. Estas declaraciones pueden ser sobre el usuario, permisos, etc.
# 3. Signature: Es la firma digital que se genera utilizando el header, el payload y una clave secreta. Esta firma se utiliza para verificar la integridad del token y asegurar que no ha sido modificado.
# JWT se utiliza comúnmente para autenticación y autorización en aplicaciones web. El servidor genera un token JWT después de que el usuario se autentica correctamente y lo envía al cliente. El cliente luego incluye este token en las solicitudes subsecuentes para acceder a recursos protegidos en el servidor. El servidor puede verificar la firma del token para asegurarse de que es válido y no ha sido alterado, y luego puede extraer la información del payload para determinar los permisos del usuario.

import jwt
import datetime
SECRET_KEY = "9b7eea038ce5473ff247bcd3a5832e918f9f25e807b9a1e2b2c132e1a83625e8"

payload: dict= {
    "username": "Jorge Petterson",
    "Role": "user",
    "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=2)
}

#Crear ell JWT 
#En el algoritmo el mas comun a utilizar es el HS256, que es un algoritmo de firma simétrica que utiliza una clave secreta para generar la firma del token. Esto significa que tanto el emisor como el receptor del token deben conocer la misma clave secreta para poder verificar la autenticidad del token.
token = jwt.encode(payload, SECRET_KEY,algorithm="HS256")
print("JWT:", token)

#Verificar/decodificar el JWT 
try:
    decoded = jwt.decode(token,SECRET_KEY, algorithms=["HS256"])
    print("Decoded JWT:", decoded)
except jwt.ExpiredSignatureError:
    print("Token has expired")
except jwt.InvalidTokenError:
    print("Invalid token")   

#Verificar rol del usuario
try:
    decoded = jwt.decode(token,SECRET_KEY, algorithms=["HS256"])
    if decoded.get("Role")=="Admin":
        print("User has admin access")
    else:
        print("User does not have admin access")
except jwt.ExpiredSignatureError:
    print("Token has expired")    