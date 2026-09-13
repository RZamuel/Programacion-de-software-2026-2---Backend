from datetime import date

from src.database.connection import get_session

from src.entities.miembro import Miembro
from src.entities.entrenador import Entrenador
from src.entities.membresia import Membresia
from src.entities.clase import Clase
from src.entities.inscripcion import Inscripcion
from src.entities.pago import Pago
from src.entities.reserva_clase import ReservaClase
from src.entities.rutina import Rutina


def poblar_base_de_datos() -> None:
    """Inserta datos iniciales en todas las tablas."""

    session = get_session()

    try:
        print("Iniciando Seeders...")

        # ==================================================
        # VALIDACIÓN: Evitar duplicados
        # ==================================================
        if session.query(Miembro).first():
            print(
                "⚠️ La base de datos ya tiene datos. "
                "Seed omitido para evitar duplicados."
            )
            return

        print("✓ Base de datos limpia. Insertando datos...")

        # ==================================================
        # 1. MIEMBROS
        # ==================================================
        miembro_1 = Miembro(
            nombre="Carlos",
            apellido="Pérez",
            email="carlos.perez@email.com",
            telefono="3001234567",
            fecha_registro=date(2026, 8, 1),
        )

        miembro_2 = Miembro(
            nombre="Ana",
            apellido="Gómez",
            email="ana.gomez@email.com",
            telefono="3115554433",
            fecha_registro=date(2026, 8, 10),
        )

        miembro_3 = Miembro(
            nombre="Luis",
            apellido="Martínez",
            email="luis.martinez@email.com",
            telefono="3157778899",
            fecha_registro=date(2026, 8, 15),
        )

        session.add_all([miembro_1, miembro_2, miembro_3])
        session.commit()

        print("✓ Miembros creados (3)")

        # ==================================================
        # 2. ENTRENADORES
        # ==================================================
        entrenador_1 = Entrenador(
            nombre="Laura",
            apellido="Martínez",
            especialidad="Musculación",
            telefono="3109876543",
            salario=2500000.0,
        )

        entrenador_2 = Entrenador(
            nombre="Juan",
            apellido="Rodríguez",
            especialidad="Cardio",
            telefono="3204567890",
            salario=2800000.0,
        )

        session.add_all([entrenador_1, entrenador_2])
        session.commit()

        print("✓ Entrenadores creados (2)")

        # ==================================================
        # 3. MEMBRESÍAS
        # ==================================================
        membresia_1 = Membresia(
            tipo="Mensual Básica",
            precio=80000.0,
            duracion_dias=30,
        )

        membresia_2 = Membresia(
            tipo="Trimestral Premium",
            precio=220000.0,
            duracion_dias=90,
        )

        membresia_3 = Membresia(
            tipo="Anual Total",
            precio=800000.0,
            duracion_dias=365,
        )

        session.add_all([membresia_1, membresia_2, membresia_3])
        session.commit()

        print("✓ Membresías creadas (3)")

        # ==================================================
        # 4. CLASES
        # ==================================================
        clase_1 = Clase(
            id_entrenador=entrenador_1.id_entrenador,
            nombre="Entrenamiento de Fuerza",
            dia_semana="Lunes",
            hora="18:00",
            capacidad_maxima=20,
        )

        clase_2 = Clase(
            id_entrenador=entrenador_2.id_entrenador,
            nombre="Cardio Intensivo",
            dia_semana="Miércoles",
            hora="19:00",
            capacidad_maxima=15,
        )

        clase_3 = Clase(
            id_entrenador=entrenador_1.id_entrenador,
            nombre="Musculación",
            dia_semana="Viernes",
            hora="17:00",
            capacidad_maxima=15,
        )

        session.add_all([clase_1, clase_2, clase_3])
        session.commit()

        print("✓ Clases creadas (3)")

        # ==================================================
        # 5. INSCRIPCIONES
        # ==================================================
        inscripcion_1 = Inscripcion(
            id_miembro=miembro_1.id_miembro,
            id_membresia=membresia_2.id_membresia,
            fecha_inicio=date(2026, 9, 1),
            fecha_fin=date(2026, 11, 30),
            estado="activa",
        )

        inscripcion_2 = Inscripcion(
            id_miembro=miembro_2.id_miembro,
            id_membresia=membresia_1.id_membresia,
            fecha_inicio=date(2026, 9, 1),
            fecha_fin=date(2026, 9, 30),
            estado="activa",
        )

        inscripcion_3 = Inscripcion(
            id_miembro=miembro_3.id_miembro,
            id_membresia=membresia_3.id_membresia,
            fecha_inicio=date(2026, 9, 1),
            fecha_fin=date(2027, 8, 31),
            estado="activa",
        )

        session.add_all([inscripcion_1, inscripcion_2, inscripcion_3])
        session.commit()

        print("✓ Inscripciones creadas (3)")

        # ==================================================
        # 6. PAGOS
        # ==================================================
        pago_1 = Pago(
            id_miembro=miembro_1.id_miembro,
            monto=220000.0,
            fecha_pago=date(2026, 9, 1),
            metodo_pago="Tarjeta",
            concepto="Membresía Trimestral Premium",
        )

        pago_2 = Pago(
            id_miembro=miembro_2.id_miembro,
            monto=80000.0,
            fecha_pago=date(2026, 9, 1),
            metodo_pago="Efectivo",
            concepto="Membresía Mensual Básica",
        )

        pago_3 = Pago(
            id_miembro=miembro_3.id_miembro,
            monto=800000.0,
            fecha_pago=date(2026, 9, 1),
            metodo_pago="PSE",
            concepto="Membresía Anual Total",
        )

        session.add_all([pago_1, pago_2, pago_3])
        session.commit()

        print("✓ Pagos creados (3)")

        # ==================================================
        # 7. RESERVAS DE CLASE
        # ==================================================
        reserva_1 = ReservaClase(
            id_miembro=miembro_1.id_miembro,
            id_clase=clase_1.id_clase,
            fecha_reserva=date(2026, 9, 5),
            estado="confirmada",
        )

        reserva_2 = ReservaClase(
            id_miembro=miembro_2.id_miembro,
            id_clase=clase_2.id_clase,
            fecha_reserva=date(2026, 9, 7),
            estado="confirmada",
        )

        reserva_3 = ReservaClase(
            id_miembro=miembro_3.id_miembro,
            id_clase=clase_1.id_clase,
            fecha_reserva=date(2026, 9, 5),
            estado="confirmada",
        )

        reserva_4 = ReservaClase(
            id_miembro=miembro_1.id_miembro,
            id_clase=clase_3.id_clase,
            fecha_reserva=date(2026, 9, 10),
            estado="confirmada",
        )

        session.add_all([reserva_1, reserva_2, reserva_3, reserva_4])
        session.commit()

        print("✓ Reservas creadas (4)")

        # ==================================================
        # 8. RUTINAS
        # ==================================================
        rutina_1 = Rutina(
            id_miembro=miembro_1.id_miembro,
            id_entrenador=entrenador_1.id_entrenador,
            nombre="Hipertrofia",
            descripcion="Rutina enfocada en ganar masa muscular.",
            fecha_creacion=date(2026, 9, 2),
        )

        rutina_2 = Rutina(
            id_miembro=miembro_2.id_miembro,
            id_entrenador=entrenador_2.id_entrenador,
            nombre="Cardio y resistencia",
            descripcion="Rutina enfocada en mejorar resistencia cardiovascular.",
            fecha_creacion=date(2026, 9, 3),
        )

        rutina_3 = Rutina(
            id_miembro=miembro_3.id_miembro,
            id_entrenador=entrenador_1.id_entrenador,
            nombre="Fuerza general",
            descripcion="Rutina enfocada en desarrollar fuerza general.",
            fecha_creacion=date(2026, 9, 4),
        )

        session.add_all([rutina_1, rutina_2, rutina_3])
        session.commit()

        print("✓ Rutinas creadas (3)")

        # ==================================================
        # FINAL
        # ==================================================
        print("\n========================================")
        print("✅ SEED EJECUTADO CORRECTAMENTE")
        print("========================================")
        print("Total de registros insertados: 24")
        print("========================================\n")

    except Exception as e:
        session.rollback()
        print(f"\n✗ Error al ejecutar el seed: {e}")
        print("Se ha revertido la última transacción.")

    finally:
        session.close()


if __name__ == "__main__":
    poblar_base_de_datos()
