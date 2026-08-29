import re
from datetime import datetime
from src.entities.miembro import Miembro
from src.entities.membresia import Membresia
from src.entities.inscripcion import Inscripcion
from src.entities.pago import Pago
from src.entities.entrenador import Entrenador
from src.entities.clase import Clase
from src.entities.reserva_clase import ReservaClase
from src.entities.rutina import Rutina

from src.crud import crud_miembro
from src.crud import crud_membresia
from src.crud import crud_inscripcion
from src.crud import crud_pago
from src.crud import crud_entrenador
from src.crud import crud_clase
from src.crud import crud_reserva_clase
from src.crud import crud_rutina


def titulo(texto: str) -> None:
    """Muestra un título de sección."""
    print("\n" + "=" * 60)
    print(texto.center(60))
    print("=" * 60)


def subtitulo(texto: str) -> None:
    """Muestra un subtítulo."""
    print("\n" + "-" * 60)
    print(texto)
    print("-" * 60)


def pausar() -> None:
    """Pausa la ejecución hasta que el usuario presione Enter."""
    input("\nPresione Enter para continuar...")


def leer_entero(mensaje: str) -> int:
    """Solicita un número entero hasta recibir un valor válido."""
    while True:
        try:
            return int(input(mensaje).strip())
        except ValueError:
            print("Debe ingresar un número entero.")


def leer_float(mensaje: str) -> float:
    """Solicita un número decimal hasta recibir un valor válido."""
    while True:
        try:
            return float(input(mensaje).strip())
        except ValueError:
            print("Debe ingresar un número válido.")


def leer_telefono(mensaje: str, permitir_vacio: bool = False) -> str:
    """Valida un teléfono con números, espacios y guiones."""
    while True:
        valor = input(mensaje).strip()
        if permitir_vacio and not valor:
            return ""
        if re.fullmatch(r"\+?[0-9\s-]{7,20}", valor):
            return valor
        print("Teléfono inválido. Use solo números, espacios o guiones.")


def leer_fecha(mensaje: str):
    """Solicita una fecha en formato YYYY-MM-DD."""
    while True:
        fecha = input(f"{mensaje} (YYYY-MM-DD): ").strip()

        try:
            return datetime.strptime(fecha, "%Y-%m-%d").date()
        except ValueError:
            print("Fecha inválida. Use el formato YYYY-MM-DD.")


def confirmar(mensaje: str) -> bool:
    """Solicita confirmación al usuario."""
    respuesta = input(f"{mensaje} (s/n): ").strip().lower()
    return respuesta == "s"


def formatear_miembro(miembro: Miembro) -> str:
    """Formatea la información de un miembro sin depender de __str__ roto."""
    return f"Miembro(ID: {miembro.id_miembro}, Nombre: {miembro.nombre} {miembro.apellido})"


# =====================================================================
# MENÚ PRINCIPAL
# =====================================================================


def mostrar_menu_principal() -> None:
    """Muestra el menú principal."""
    titulo("SISTEMA DE GESTIÓN DE GIMNASIO")

    print("1. Gestión de Miembros")
    print("2. Gestión de Membresías")
    print("3. Gestión de Inscripciones")
    print("4. Gestión de Pagos")
    print("5. Gestión de Entrenadores")
    print("6. Gestión de Clases")
    print("7. Gestión de Reservas")
    print("8. Gestión de Rutinas")
    print("9. Ver relaciones entre entidades")
    print("0. Salir")

    print("=" * 60)


def ejecutar_menu(titulo_menu: str, opciones: list[tuple[str, str, callable]]) -> None:
    """Ejecuta un submenú con opciones y acciones reutilizables."""
    while True:
        subtitulo(titulo_menu)

        for numero, descripcion, _ in opciones:
            print(f"{numero}. {descripcion}")

        print("0. Volver")

        opcion = input("\nSeleccione una opción: ").strip()

        accion = next(
            (accion for numero, _, accion in opciones if numero == opcion), None
        )

        if opcion == "0":
            break

        if accion is None:
            print("Opción inválida.")
        else:
            accion()

        pausar()


# =====================================================================
# GESTIÓN DE MIEMBROS
# =====================================================================


def menu_miembros() -> None:
    """Gestiona las operaciones CRUD de miembros."""
    ejecutar_menu(
        "GESTIÓN DE MIEMBROS",
        [
            ("1", "Crear miembro", crear_miembro),
            ("2", "Consultar todos", consultar_miembros),
            ("3", "Consultar por ID", consultar_miembro_por_id),
            ("4", "Actualizar miembro", actualizar_miembro),
            ("5", "Eliminar miembro", eliminar_miembro),
        ],
    )


def crear_miembro() -> None:
    """Crea un nuevo miembro."""
    subtitulo("CREAR MIEMBRO")

    id_miembro = leer_entero("ID del miembro: ")
    nombre = input("Nombre: ").strip()
    apellido = input("Apellido: ").strip()
    email = input("Email: ").strip()
    telefono = leer_telefono("Teléfono: ")
    fecha_registro = leer_fecha("Fecha de registro")

    miembro = Miembro(
        id_miembro,
        nombre,
        apellido,
        email,
        telefono,
        fecha_registro,
    )

    if crud_miembro.crear_miembro(miembro):
        print("Miembro creado correctamente.")
    else:
        print("No fue posible crear el miembro.")


def consultar_miembros() -> None:
    """Consulta todos los miembros."""
    subtitulo("LISTA DE MIEMBROS")

    miembros = crud_miembro.leer_miembros()

    if not miembros:
        print("No hay miembros registrados.")
        return

    for miembro in miembros:
        print(f"• {formatear_miembro(miembro)}")


def consultar_miembro_por_id() -> None:
    """Consulta un miembro por su ID."""
    subtitulo("CONSULTAR MIEMBRO")

    id_miembro = leer_entero("ID del miembro: ")
    miembro = crud_miembro.leer_miembro_por_id(id_miembro)

    if miembro:
        print(f" {formatear_miembro(miembro)}")
    else:
        print(" Miembro no encontrado.")


def actualizar_miembro() -> None:
    """Actualiza los datos de un miembro."""
    subtitulo("ACTUALIZAR MIEMBRO")

    id_miembro = leer_entero("ID del miembro: ")
    miembro = crud_miembro.leer_miembro_por_id(id_miembro)

    if not miembro:
        print(" Miembro no encontrado.")
        return

    print(f"\nDatos actuales: {formatear_miembro(miembro)}")

    nombre = input("Nuevo nombre (Enter para mantener): ").strip()
    apellido = input("Nuevo apellido (Enter para mantener): ").strip()
    email = input("Nuevo email (Enter para mantener): ").strip()
    telefono = leer_telefono(
        "Nuevo teléfono (Enter para mantener): ", permitir_vacio=True
    )

    datos = {
        "nombre": miembro.nombre,
        "apellido": miembro.apellido,
        "email": miembro.email,
        "telefono": miembro.telefono,
    }

    if nombre:
        datos["nombre"] = nombre

    if apellido:
        datos["apellido"] = apellido

    if email:
        datos["email"] = email

    if telefono:
        datos["telefono"] = telefono

    if crud_miembro.actualizar_miembro(id_miembro, **datos):
        print(" Miembro actualizado correctamente.")
    else:
        print(" No fue posible actualizar el miembro.")


def eliminar_miembro() -> None:
    """Elimina un miembro."""
    subtitulo("ELIMINAR MIEMBRO")

    id_miembro = leer_entero("ID del miembro: ")
    miembro = crud_miembro.leer_miembro_por_id(id_miembro)

    if not miembro:
        print(" Miembro no encontrado.")
        return

    print(f"\n{formatear_miembro(miembro)}")

    if confirmar("¿Desea eliminar este miembro?"):
        if crud_miembro.eliminar_miembro(id_miembro):
            print(" Miembro eliminado correctamente.")
        else:
            print(" No fue posible eliminar el miembro.")
    else:
        print(" Operación cancelada.")


# =====================================================================
# GESTIÓN DE MEMBRESÍAS
# =====================================================================


def menu_membresias() -> None:
    """Gestiona las operaciones CRUD de membresías."""
    ejecutar_menu(
        "GESTIÓN DE MEMBRESÍAS",
        [
            ("1", "Crear membresía", crear_membresia),
            ("2", "Consultar todas", consultar_membresias),
            ("3", "Consultar por ID", consultar_membresia_por_id),
            ("4", "Actualizar membresía", actualizar_membresia),
            ("5", "Eliminar membresía", eliminar_membresia),
        ],
    )


def crear_membresia() -> None:
    """Crea una nueva membresía."""
    subtitulo("CREAR MEMBRESÍA")

    id_membresia = leer_entero("ID de la membresía: ")
    id_miembro = leer_entero("ID del miembro: ")
    tipo = input("Tipo de membresía: ").strip()
    precio = leer_float("Precio: ")
    duracion_dias = leer_entero("Duración en días: ")
    fecha_inicio = leer_fecha("Fecha de inicio")
    estado = input("Estado [activa]: ").strip() or "activa"

    membresia = Membresia(
        id_membresia,
        id_miembro,
        tipo,
        precio,
        duracion_dias,
        fecha_inicio,
        estado,
    )

    if crud_membresia.crear_membresia(membresia):
        print(" Membresía creada correctamente.")
    else:
        print(" No fue posible crear la membresía.")


def consultar_membresias() -> None:
    """Consulta todas las membresías."""
    subtitulo("LISTA DE MEMBRESÍAS")

    membresias = crud_membresia.leer_membresias()

    if not membresias:
        print("No hay membresías registradas.")
        return

    for membresia in membresias:
        print(f"• {membresia}")


def consultar_membresia_por_id() -> None:
    """Consulta una membresía por ID."""
    subtitulo("CONSULTAR MEMBRESÍA")

    id_membresia = leer_entero("ID de la membresía: ")
    membresia = crud_membresia.leer_membresia_por_id(id_membresia)

    if membresia:
        print(f" {membresia}")
    else:
        print(" Membresía no encontrada.")


def actualizar_membresia() -> None:
    """Actualiza una membresía."""
    subtitulo("ACTUALIZAR MEMBRESÍA")

    id_membresia = leer_entero("ID de la membresía: ")
    membresia = crud_membresia.leer_membresia_por_id(id_membresia)

    if not membresia:
        print(" Membresía no encontrada.")
        return

    print(f"\nDatos actuales: {membresia}")

    tipo = input("Nuevo tipo (Enter para mantener): ").strip()
    precio_texto = input("Nuevo precio (Enter para mantener): ").strip()
    duracion_texto = input("Nueva duración en días (Enter para mantener): ").strip()

    datos = {}

    if tipo:
        datos["tipo"] = tipo

    if precio_texto:
        try:
            datos["precio"] = float(precio_texto)
        except ValueError:
            print(" El precio debe ser numérico.")
            return

    if duracion_texto:
        try:
            datos["duracion_dias"] = int(duracion_texto)
        except ValueError:
            print(" La duración debe ser un número entero.")
            return

    if not datos:
        print(" No se realizaron cambios.")
        return

    if crud_membresia.actualizar_membresia(id_membresia, **datos):
        print(" Membresía actualizada correctamente.")
    else:
        print(" No fue posible actualizar la membresía.")


def eliminar_membresia() -> None:
    """Elimina una membresía."""
    subtitulo("ELIMINAR MEMBRESÍA")

    id_membresia = leer_entero("ID de la membresía: ")
    membresia = crud_membresia.leer_membresia_por_id(id_membresia)

    if not membresia:
        print(" Membresía no encontrada.")
        return

    print(membresia)

    if confirmar("¿Desea eliminar esta membresía?"):
        if crud_membresia.eliminar_membresia(id_membresia):
            print(" Membresía eliminada correctamente.")
        else:
            print(" No fue posible eliminar la membresía.")


# =====================================================================
# GESTIÓN DE INSCRIPCIONES
# =====================================================================


def menu_inscripciones() -> None:
    """Gestiona las operaciones CRUD de inscripciones."""
    ejecutar_menu(
        "GESTIÓN DE INSCRIPCIONES",
        [
            ("1", "Crear inscripción", crear_inscripcion),
            ("2", "Consultar todas", consultar_inscripciones),
            ("3", "Consultar por ID", consultar_inscripcion_por_id),
            ("4", "Actualizar inscripción", actualizar_inscripcion),
            ("5", "Eliminar inscripción", eliminar_inscripcion),
        ],
    )


def crear_inscripcion() -> None:
    """Crea una inscripción."""
    subtitulo("CREAR INSCRIPCIÓN")

    id_inscripcion = leer_entero("ID de inscripción: ")
    id_miembro = leer_entero("ID del miembro: ")
    id_membresia = leer_entero("ID de la membresía: ")
    fecha_inicio = leer_fecha("Fecha de inicio")
    fecha_fin = leer_fecha("Fecha de finalización")

    estado = input("Estado [activa]: ").strip() or "activa"

    inscripcion = Inscripcion(
        id_inscripcion,
        id_miembro,
        id_membresia,
        fecha_inicio,
        fecha_fin,
        estado,
    )

    if crud_inscripcion.crear_inscripcion(inscripcion):
        print(" Inscripción creada correctamente.")
    else:
        print(" No fue posible crear la inscripción.")


def consultar_inscripciones() -> None:
    """Consulta todas las inscripciones."""
    subtitulo("LISTA DE INSCRIPCIONES")

    inscripciones = crud_inscripcion.leer_inscripciones()

    if not inscripciones:
        print("No hay inscripciones registradas.")
        return

    for inscripcion in inscripciones:
        print(f"• {inscripcion}")


def consultar_inscripcion_por_id() -> None:
    """Consulta una inscripción por ID."""
    subtitulo("CONSULTAR INSCRIPCIÓN")

    id_inscripcion = leer_entero("ID de inscripción: ")
    inscripcion = crud_inscripcion.leer_inscripcion_por_id(id_inscripcion)

    if inscripcion:
        print(f" {inscripcion}")
    else:
        print(" Inscripción no encontrada.")


def actualizar_inscripcion() -> None:
    """Actualiza una inscripción."""
    subtitulo("ACTUALIZAR INSCRIPCIÓN")

    id_inscripcion = leer_entero("ID de inscripción: ")
    inscripcion = crud_inscripcion.leer_inscripcion_por_id(id_inscripcion)

    if not inscripcion:
        print(" Inscripción no encontrada.")
        return

    print(f"\nDatos actuales: {inscripcion}")

    estado = input("Nuevo estado (Enter para mantener): ").strip()

    if not estado:
        print(" No se realizaron cambios.")
        return

    if crud_inscripcion.actualizar_inscripcion(
        id_inscripcion,
        estado=estado,
    ):
        print(" Inscripción actualizada correctamente.")
    else:
        print(" No fue posible actualizar la inscripción.")


def eliminar_inscripcion() -> None:
    """Elimina una inscripción."""
    subtitulo("ELIMINAR INSCRIPCIÓN")

    id_inscripcion = leer_entero("ID de inscripción: ")
    inscripcion = crud_inscripcion.leer_inscripcion_por_id(id_inscripcion)

    if not inscripcion:
        print(" Inscripción no encontrada.")
        return

    if confirmar("¿Desea eliminar esta inscripción?"):
        if crud_inscripcion.eliminar_inscripcion(id_inscripcion):
            print(" Inscripción eliminada correctamente.")
        else:
            print(" No fue posible eliminar la inscripción.")


# =====================================================================
# GESTIÓN DE PAGOS
# =====================================================================


def menu_pagos() -> None:
    """Gestiona las operaciones CRUD de pagos."""
    ejecutar_menu(
        "GESTIÓN DE PAGOS",
        [
            ("1", "Registrar pago", crear_pago),
            ("2", "Consultar todos", consultar_pagos),
            ("3", "Consultar por ID", consultar_pago_por_id),
            ("4", "Actualizar pago", actualizar_pago),
            ("5", "Eliminar pago", eliminar_pago),
        ],
    )


def crear_pago() -> None:
    """Registra un nuevo pago."""
    subtitulo("REGISTRAR PAGO")

    id_pago = leer_entero("ID del pago: ")
    id_miembro = leer_entero("ID del miembro: ")
    monto = leer_float("Monto: ")
    fecha_pago = leer_fecha("Fecha del pago")
    metodo_pago = input("Método de pago: ").strip()
    concepto = input("Concepto: ").strip()

    pago = Pago(
        id_pago,
        id_miembro,
        monto,
        fecha_pago,
        metodo_pago,
        concepto,
    )

    if crud_pago.crear_pago(pago):
        print(" Pago registrado correctamente.")
    else:
        print(" No fue posible registrar el pago.")


def consultar_pagos() -> None:
    """Consulta todos los pagos."""
    subtitulo("LISTA DE PAGOS")

    pagos = crud_pago.leer_pagos()

    if not pagos:
        print("No hay pagos registrados.")
        return

    for pago in pagos:
        print(f"• {pago}")


def consultar_pago_por_id() -> None:
    """Consulta un pago por ID."""
    subtitulo("CONSULTAR PAGO")

    id_pago = leer_entero("ID del pago: ")
    pago = crud_pago.leer_pago_por_id(id_pago)

    if pago:
        print(f"ID miembro: {pago.id_miembro}")
        print(f"Monto: ${pago.monto}")
        print(f"Fecha: {pago.fecha_pago}")
        print(f"Método: {pago.metodo_pago}")
        print(f"Concepto: {pago.concepto}")
    else:
        print(" Pago no encontrado.")


def actualizar_pago() -> None:
    """Actualiza un pago."""
    subtitulo("ACTUALIZAR PAGO")

    id_pago = leer_entero("ID del pago: ")
    pago = crud_pago.leer_pago_por_id(id_pago)

    if not pago:
        print(" Pago no encontrado.")
        return

    print(f"\nDatos actuales: {pago}")

    monto_texto = input("Nuevo monto (Enter para mantener): ").strip()
    metodo = input("Nuevo método de pago (Enter para mantener): ").strip()
    concepto = input("Nuevo concepto (Enter para mantener): ").strip()

    monto = None

    if monto_texto:
        try:
            monto = float(monto_texto)
        except ValueError:
            print(" El monto debe ser numérico.")
            return

    if not monto_texto and not metodo and not concepto:
        print(" No se realizaron cambios.")
        return

    if crud_pago.actualizar_pago(
        id_pago,
        monto=monto,
        metodo_pago=metodo or None,
        concepto=concepto or None,
    ):
        print(" Pago actualizado correctamente.")
    else:
        print(" No fue posible actualizar el pago.")


def eliminar_pago() -> None:
    """Elimina un pago."""
    subtitulo("ELIMINAR PAGO")

    id_pago = leer_entero("ID del pago: ")
    pago = crud_pago.leer_pago_por_id(id_pago)

    if not pago:
        print(" Pago no encontrado.")
        return

    print(pago)

    if confirmar("¿Desea eliminar este pago?"):
        if crud_pago.eliminar_pago(id_pago):
            print(" Pago eliminado correctamente.")
        else:
            print(" No fue posible eliminar el pago.")


# =====================================================================
# GESTIÓN DE ENTRENADORES
# =====================================================================


def menu_entrenadores() -> None:
    """Gestiona las operaciones CRUD de entrenadores."""
    ejecutar_menu(
        "GESTIÓN DE ENTRENADORES",
        [
            ("1", "Crear entrenador", crear_entrenador),
            ("2", "Consultar todos", consultar_entrenadores),
            ("3", "Consultar por ID", consultar_entrenador_por_id),
            ("4", "Actualizar entrenador", actualizar_entrenador),
            ("5", "Eliminar entrenador", eliminar_entrenador),
        ],
    )


def crear_entrenador() -> None:
    """Crea un entrenador."""
    subtitulo("CREAR ENTRENADOR")

    id_entrenador = leer_entero("ID del entrenador: ")
    nombre = input("Nombre: ").strip()
    apellido = input("Apellido: ").strip()
    especialidad = input("Especialidad: ").strip()
    telefono = leer_telefono("Teléfono: ")
    salario = leer_float("Salario: ")

    entrenador = Entrenador(
        id_entrenador,
        nombre,
        apellido,
        especialidad,
        telefono,
        salario,
    )

    if crud_entrenador.crear_entrenador(entrenador):
        print(" Entrenador creado correctamente.")
    else:
        print(" No fue posible crear el entrenador.")


def consultar_entrenadores() -> None:
    """Consulta todos los entrenadores."""
    subtitulo("LISTA DE ENTRENADORES")

    entrenadores = crud_entrenador.leer_entrenadores()

    if not entrenadores:
        print("No hay entrenadores registrados.")
        return

    for entrenador in entrenadores:
        print(f"• {entrenador}")


def consultar_entrenador_por_id() -> None:
    """Consulta un entrenador por ID."""
    subtitulo("CONSULTAR ENTRENADOR")

    id_entrenador = leer_entero("ID del entrenador: ")
    entrenador = crud_entrenador.leer_entrenador_por_id(id_entrenador)

    if entrenador:
        print(f" {entrenador}")
    else:
        print(" Entrenador no encontrado.")


def actualizar_entrenador() -> None:
    """Actualiza un entrenador."""
    subtitulo("ACTUALIZAR ENTRENADOR")

    id_entrenador = leer_entero("ID del entrenador: ")
    entrenador = crud_entrenador.leer_entrenador_por_id(id_entrenador)

    if not entrenador:
        print(" Entrenador no encontrado.")
        return

    print(f"\nDatos actuales: {entrenador}")

    telefono = leer_telefono(
        "Nuevo teléfono (Enter para mantener): ", permitir_vacio=True
    )
    especialidad = input("Nueva especialidad (Enter para mantener): ").strip()
    salario_texto = input("Nuevo salario (Enter para mantener): ").strip()

    datos = {}

    if telefono:
        datos["telefono"] = telefono

    if especialidad:
        datos["especialidad"] = especialidad

    if salario_texto:
        try:
            datos["salario"] = float(salario_texto)
        except ValueError:
            print(" El salario debe ser numérico.")
            return

    if not datos:
        print(" No se realizaron cambios.")
        return

    if crud_entrenador.actualizar_entrenador(
        id_entrenador,
        **datos,
    ):
        print(" Entrenador actualizado correctamente.")
    else:
        print(" No fue posible actualizar el entrenador.")


def eliminar_entrenador() -> None:
    """Elimina un entrenador."""
    subtitulo("ELIMINAR ENTRENADOR")

    id_entrenador = leer_entero("ID del entrenador: ")
    entrenador = crud_entrenador.leer_entrenador_por_id(id_entrenador)

    if not entrenador:
        print(" Entrenador no encontrado.")
        return

    if confirmar("¿Desea eliminar este entrenador?"):
        if crud_entrenador.eliminar_entrenador(id_entrenador):
            print(" Entrenador eliminado correctamente.")
        else:
            print(" No fue posible eliminar el entrenador.")


# =====================================================================
# GESTIÓN DE CLASES
# =====================================================================


def menu_clases() -> None:
    """Gestiona las operaciones CRUD de clases."""
    ejecutar_menu(
        "GESTIÓN DE CLASES",
        [
            ("1", "Crear clase", crear_clase),
            ("2", "Consultar todas", consultar_clases),
            ("3", "Consultar por ID", consultar_clase_por_id),
            ("4", "Actualizar clase", actualizar_clase),
            ("5", "Eliminar clase", eliminar_clase),
        ],
    )


def crear_clase() -> None:
    """Crea una clase."""
    subtitulo("CREAR CLASE")

    id_clase = leer_entero("ID de la clase: ")
    id_entrenador = leer_entero("ID del entrenador: ")
    nombre = input("Nombre de la clase: ").strip()
    dia_semana = input("Día de la semana: ").strip()
    hora = input("Hora: ").strip()
    capacidad_maxima = leer_entero("Capacidad máxima: ")

    clase = Clase(
        id_clase,
        id_entrenador,
        nombre,
        dia_semana,
        hora,
        capacidad_maxima,
    )

    if crud_clase.crear_clase(clase):
        print(" Clase creada correctamente.")
    else:
        print(" No fue posible crear la clase.")


def consultar_clases() -> None:
    """Consulta todas las clases."""
    subtitulo("LISTA DE CLASES")

    clases = crud_clase.leer_clases()

    if not clases:
        print("No hay clases registradas.")
        return

    for clase in clases:
        print(f"• {clase}")


def consultar_clase_por_id() -> None:
    """Consulta una clase por ID."""
    subtitulo("CONSULTAR CLASE")

    id_clase = leer_entero("ID de la clase: ")
    clase = crud_clase.leer_clase_por_id(id_clase)

    if clase:
        print(f" {clase}")
    else:
        print(" Clase no encontrada.")


def actualizar_clase() -> None:
    """Actualiza una clase."""
    subtitulo("ACTUALIZAR CLASE")

    id_clase = leer_entero("ID de la clase: ")
    clase = crud_clase.leer_clase_por_id(id_clase)

    if not clase:
        print(" Clase no encontrada.")
        return

    print(f"\nDatos actuales: {clase}")

    nombre = input("Nuevo nombre (Enter para mantener): ").strip()
    dia = input("Nuevo día (Enter para mantener): ").strip()
    hora = input("Nueva hora (Enter para mantener): ").strip()
    capacidad_texto = input("Nueva capacidad (Enter para mantener): ").strip()

    datos = {}

    if nombre:
        datos["nombre"] = nombre

    if dia:
        datos["dia_semana"] = dia

    if hora:
        datos["hora"] = hora

    if capacidad_texto:
        try:
            datos["capacidad_maxima"] = int(capacidad_texto)
        except ValueError:
            print(" La capacidad debe ser un entero.")
            return

    if not datos:
        print(" No se realizaron cambios.")
        return

    if crud_clase.actualizar_clase(id_clase, **datos):
        print(" Clase actualizada correctamente.")
    else:
        print(" No fue posible actualizar la clase.")


def eliminar_clase() -> None:
    """Elimina una clase."""
    subtitulo("ELIMINAR CLASE")

    id_clase = leer_entero("ID de la clase: ")
    clase = crud_clase.leer_clase_por_id(id_clase)

    if not clase:
        print(" Clase no encontrada.")
        return

    if confirmar("¿Desea eliminar esta clase?"):
        if crud_clase.eliminar_clase(id_clase):
            print(" Clase eliminada correctamente.")
        else:
            print(" No fue posible eliminar la clase.")


# =====================================================================
# GESTIÓN DE RESERVAS
# =====================================================================


def menu_reservas() -> None:
    """Gestiona las operaciones CRUD de reservas."""
    ejecutar_menu(
        "GESTIÓN DE RESERVAS",
        [
            ("1", "Crear reserva", crear_reserva),
            ("2", "Consultar todas", consultar_reservas),
            ("3", "Consultar por ID", consultar_reserva_por_id),
            ("4", "Actualizar reserva", actualizar_reserva),
            ("5", "Eliminar reserva", eliminar_reserva),
        ],
    )


def crear_reserva() -> None:
    """Crea una reserva de clase."""
    subtitulo("CREAR RESERVA")

    id_reserva = leer_entero("ID de reserva: ")
    id_miembro = leer_entero("ID del miembro: ")
    id_clase = leer_entero("ID de la clase: ")
    fecha_reserva = leer_fecha("Fecha de reserva")

    estado = input("Estado [confirmada]: ").strip() or "confirmada"

    reserva = ReservaClase(
        id_reserva,
        id_miembro,
        id_clase,
        fecha_reserva,
        estado,
    )

    if crud_reserva_clase.crear_reserva(reserva):
        print(" Reserva creada correctamente.")
    else:
        print(" No fue posible crear la reserva.")


def consultar_reservas() -> None:
    """Consulta todas las reservas."""
    subtitulo("LISTA DE RESERVAS")

    reservas = crud_reserva_clase.leer_reservas()

    if not reservas:
        print("No hay reservas registradas.")
        return

    for reserva in reservas:
        print(f"• {reserva}")


def consultar_reserva_por_id() -> None:
    """Consulta una reserva por ID."""
    subtitulo("CONSULTAR RESERVA")

    id_reserva = leer_entero("ID de reserva: ")
    reserva = crud_reserva_clase.leer_reserva_por_id(id_reserva)

    if reserva:
        print(f" {reserva}")
    else:
        print(" Reserva no encontrada.")


def actualizar_reserva() -> None:
    """Actualiza una reserva."""
    subtitulo("ACTUALIZAR RESERVA")

    id_reserva = leer_entero("ID de reserva: ")
    reserva = crud_reserva_clase.leer_reserva_por_id(id_reserva)

    if not reserva:
        print(" Reserva no encontrada.")
        return

    print(f"\nDatos actuales: {reserva}")

    estado = input("Nuevo estado (Enter para mantener): ").strip()

    if not estado:
        print(" No se realizaron cambios.")
        return

    if crud_reserva_clase.actualizar_reserva(
        id_reserva,
        estado=estado,
    ):
        print(" Reserva actualizada correctamente.")
    else:
        print(" No fue posible actualizar la reserva.")


def eliminar_reserva() -> None:
    """Elimina una reserva."""
    subtitulo("ELIMINAR RESERVA")

    id_reserva = leer_entero("ID de reserva: ")
    reserva = crud_reserva_clase.leer_reserva_por_id(id_reserva)

    if not reserva:
        print(" Reserva no encontrada.")
        return

    if confirmar("¿Desea eliminar esta reserva?"):
        if crud_reserva_clase.eliminar_reserva(id_reserva):
            print(" Reserva eliminada correctamente.")
        else:
            print(" No fue posible eliminar la reserva.")


# =====================================================================
# GESTIÓN DE RUTINAS
# =====================================================================


def menu_rutinas() -> None:
    """Gestiona las operaciones CRUD de rutinas."""
    ejecutar_menu(
        "GESTIÓN DE RUTINAS",
        [
            ("1", "Crear rutina", crear_rutina),
            ("2", "Consultar todas", consultar_rutinas),
            ("3", "Consultar por ID", consultar_rutina_por_id),
            ("4", "Actualizar rutina", actualizar_rutina),
            ("5", "Eliminar rutina", eliminar_rutina),
        ],
    )


def crear_rutina() -> None:
    """Crea una rutina."""
    subtitulo("CREAR RUTINA")

    id_rutina = leer_entero("ID de rutina: ")
    id_miembro = leer_entero("ID del miembro: ")
    id_entrenador = leer_entero("ID del entrenador: ")
    nombre = input("Nombre de la rutina: ").strip()
    descripcion = input("Descripción: ").strip()
    fecha_creacion = leer_fecha("Fecha de creación")

    rutina = Rutina(
        id_rutina,
        id_miembro,
        id_entrenador,
        nombre,
        descripcion,
        fecha_creacion,
    )

    if crud_rutina.crear_rutina(rutina):
        print(" Rutina creada correctamente.")
    else:
        print(" No fue posible crear la rutina.")


def consultar_rutinas() -> None:
    """Consulta todas las rutinas."""
    subtitulo("LISTA DE RUTINAS")

    rutinas = crud_rutina.leer_rutinas()

    if not rutinas:
        print("No hay rutinas registradas.")
        return

    for rutina in rutinas:
        print(f"• {rutina}")


def consultar_rutina_por_id() -> None:
    """Consulta una rutina por ID."""
    subtitulo("CONSULTAR RUTINA")

    id_rutina = leer_entero("ID de rutina: ")
    rutina = crud_rutina.leer_rutina_por_id(id_rutina)

    if rutina:
        print(f" {rutina}")
    else:
        print(" Rutina no encontrada.")


def actualizar_rutina() -> None:
    """Actualiza una rutina."""
    subtitulo("ACTUALIZAR RUTINA")

    id_rutina = leer_entero("ID de rutina: ")
    rutina = crud_rutina.leer_rutina_por_id(id_rutina)

    if not rutina:
        print(" Rutina no encontrada.")
        return

    print(f"\nDatos actuales: {rutina}")

    nombre = input("Nuevo nombre (Enter para mantener): ").strip()
    descripcion = input("Nueva descripción (Enter para mantener): ").strip()

    datos = {}

    if nombre:
        datos["nombre"] = nombre

    if descripcion:
        datos["descripcion"] = descripcion

    if not datos:
        print(" No se realizaron cambios.")
        return

    if crud_rutina.actualizar_rutina(id_rutina, **datos):
        print(" Rutina actualizada correctamente.")
    else:
        print(" No fue posible actualizar la rutina.")


def eliminar_rutina() -> None:
    """Elimina una rutina."""
    subtitulo("ELIMINAR RUTINA")

    id_rutina = leer_entero("ID de rutina: ")
    rutina = crud_rutina.leer_rutina_por_id(id_rutina)

    if not rutina:
        print(" Rutina no encontrada.")
        return

    if confirmar("¿Desea eliminar esta rutina?"):
        if crud_rutina.eliminar_rutina(id_rutina):
            print(" Rutina eliminada correctamente.")
        else:
            print(" No fue posible eliminar la rutina.")


# =====================================================================
# RELACIONES ENTRE ENTIDADES
# =====================================================================


def ver_relaciones() -> None:
    """Muestra las relaciones principales entre las entidades."""

    titulo("RELACIONES ENTRE ENTIDADES")

    # Miembro -> Membresía
    print("\n MIEMBRO → MEMBRESÍA")
    print("   Relación mediante Inscripción")

    inscripciones = crud_inscripcion.leer_inscripciones()

    if not inscripciones:
        print("   No hay inscripciones registradas.")
    else:
        for inscripcion in inscripciones:
            miembro = crud_miembro.leer_miembro_por_id(inscripcion.id_miembro)
            membresia = crud_membresia.leer_membresia_por_id(inscripcion.id_membresia)

            if miembro and membresia:
                print(f"   {miembro.nombre} {miembro.apellido}" f" → {membresia.tipo}")

    # Miembro -> Pago
    print("\n MIEMBRO → PAGO")

    pagos = crud_pago.leer_pagos()

    if not pagos:
        print("   No hay pagos registrados.")
    else:
        for pago in pagos:
            miembro = crud_miembro.leer_miembro_por_id(pago.id_miembro)

            if miembro:
                print(
                    f"   {miembro.nombre} {miembro.apellido}"
                    f" → ${pago.monto} ({pago.concepto})"
                )

    # Miembro -> Clase
    print("\n MIEMBRO → CLASE")
    print("   Relación mediante Reserva")

    reservas = crud_reserva_clase.leer_reservas()

    if not reservas:
        print("   No hay reservas registradas.")
    else:
        for reserva in reservas:
            miembro = crud_miembro.leer_miembro_por_id(reserva.id_miembro)
            clase = crud_clase.leer_clase_por_id(reserva.id_clase)

            if miembro and clase:
                print(f"   {miembro.nombre} {miembro.apellido}" f" → {clase.nombre}")

    # Miembro -> Entrenador
    print("\n MIEMBRO → ENTRENADOR")
    print("   Relación mediante Rutina")

    rutinas = crud_rutina.leer_rutinas()

    if not rutinas:
        print("   No hay rutinas registradas.")
    else:
        for rutina in rutinas:
            miembro = crud_miembro.leer_miembro_por_id(rutina.id_miembro)
            entrenador = crud_entrenador.leer_entrenador_por_id(rutina.id_entrenador)

            if miembro and entrenador:
                print(
                    f"   {miembro.nombre} {miembro.apellido}"
                    f" → {entrenador.nombre} {entrenador.apellido}"
                )


# =====================================================================
# FUNCIÓN PRINCIPAL
# =====================================================================


def main() -> None:
    """Ejecuta el menú principal de la aplicación."""

    while True:
        mostrar_menu_principal()

        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == "1":
            menu_miembros()

        elif opcion == "2":
            menu_membresias()

        elif opcion == "3":
            menu_inscripciones()

        elif opcion == "4":
            menu_pagos()

        elif opcion == "5":
            menu_entrenadores()

        elif opcion == "6":
            menu_clases()

        elif opcion == "7":
            menu_reservas()

        elif opcion == "8":
            menu_rutinas()

        elif opcion == "9":
            ver_relaciones()
            pausar()

        elif opcion == "0":
            titulo("SISTEMA FINALIZADO")
            print("Los datos almacenados en memoria se perderán.")
            print("¡Gracias por utilizar el sistema! 👋")
            break

        else:
            print("\n Opción inválida.")
            pausar()


if __name__ == "__main__":
    main()
