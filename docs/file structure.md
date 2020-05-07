/credentials
/docs
/lib
  Librería oficial de Cortex API
/emotiv
  Librería de conexión con el Emotiv Epoch+
/monads
  Librería de estructuras algebraicas
/classifiers
  Librería de clasificadores con una interfaz en común para un plug & play
/fif
  Librería de procesamiento de data en formato .fif
daemon.py
  Mantiene el estado del servidor, esto es, almacena el usuario conectado al servidor, el classificador usado y el tipo de equipo (emotiv epoch o mock)
server.py
  Mantiene las rutas usadas ara comunicarse con el sistema
db.py
  Mantiene la conexión con la base de datos y las queries necesarias para el servidor