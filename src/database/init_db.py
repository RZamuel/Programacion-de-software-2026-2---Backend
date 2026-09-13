from src.database.connection import Base, engine
from src.entities.miembro import Miembro
from src.entities.membresia import Membresia
from src.entities.inscripcion import Inscripcion
from src.entities.pago import Pago
from src.entities.entrenador import Entrenador
from src.entities.clase import Clase
from src.entities.reserva_clase import ReservaClase
from src.entities.rutina import Rutina

Base.metadata.create_all(bind=engine)
