from database.connection import Base, engine
from entities.miembro import Miembro
from entities.membresia import Membresia
from entities.inscripcion import Inscripcion
from entities.pago import Pago
from entities.entrenador import Entrenador
from entities.clase import Clase
from entities.reserva_clase import ReservaClase
from entities.rutina import Rutina

Base.metadata.create_all(bind=engine)
