import re
import uuid
from datetime import datetime, date

# Entidades
from src.entities.miembro import Miembro
from src.entities.membresia import Membresia
from src.entities.inscripcion import Inscripcion
from src.entities.pago import Pago
from src.entities.entrenador import Entrenador
from src.entities.clase import Clase
from src.entities.reserva_clase import ReservaClase
from src.entities.rutina import Rutina

# CRUDs
from src.crud import crud_miembro
from src.crud import crud_membresia
from src.crud import crud_inscripcion
from src.crud import crud_pago
from src.crud import crud_entrenador
from src.crud import crud_clase
from src.crud import crud_reserva_clase
from src.crud import crud_rutina

# =====================================================================
# FUNCIONES DE AYUDA
# =====================================================================


def titulo(texto: str) -> None:
    print("\n" + "=" * 60)
    print(texto.center(60))
    print("=" * 60)


def subtitulo(texto: str) -> None:
    print("\n" + "-" * 60)
    print(texto)
    print("-" * 60)


def pausar() -> None:
    input("\nPresione Enter para continuar...")


def leer_float(mensaje: str) -> float:
    while True:
        try:
            return float(input(mensaje).strip())
        except ValueError:
            print("Debe ingresar un número válido.")


def leer_entero(mensaje: str) -> int:
    while True:
        try:
            return int(input(mensaje).strip())
        except ValueError:
            print("Debe ingresar un número entero.")


def leer_telefono(mensaje: str, permitir_vacio: bool = False) -> str:
    while True:
        valor = input(mensaje).strip()
        if permitir_vacio and not valor:
            return ""
        if re.fullmatch(r"\+?[0-9\s-]{7,20}", valor):
            return valor
        print("Teléfono inválido. Use solo números, espacios o guiones.")


def leer_fecha(mensaje: str, usar_hoy: bool = False) -> date:
    while True:
        fecha = input(f"{mensaje} (YYYY-MM-DD, Enter para hoy): ").strip()
        if not fecha and usar_hoy:
            return date.today()
        try:
            return datetime.strptime(fecha, "%Y-%m-%d").date()
        except ValueError:
            print("Fecha inválida. Use el formato YYYY-MM-DD.")


def leer_uuid(mensaje: str) -> uuid.UUID:
    """Solicita un UUID válido al usuario."""
    while True:
        valor = input(mensaje).strip()
        try:
            return uuid.UUID(valor)
        except ValueError:
            print("ID inválido. Debe ser un UUID válido.")


def confirmar(mensaje: str) -> bool:
    respuesta = input(f"{mensaje} (s/n): ").strip().lower()
    return respuesta == "s"


def seleccionar_estado(mensaje: str = "Selecciona un estado") -> str:
    """Muestra un menú para elegir el estado de la inscripción."""
    print(f"{mensaje}:")
    print("1. activa")
    print("2. vencida")
    print("3. cancelada")
    print("4. suspendida")
    print("5. pendiente")

    while True:
        opcion = input("Opción (1-5): ").strip()
        estados = {
            "1": "activa",
            "2": "vencida",
            "3": "cancelada",
            "4": "suspendida",
            "5": "pendiente",
        }
        if opcion in estados:
            return estados[opcion]
        print("Opción inválida. Ingresa un número del 1 al 5.")


# =====================================================================
# MENÚ PRINCIPAL
# =====================================================================


def mostrar_menu_principal() -> None:
    titulo("SISTEMA DE GESTIÓN DE GIMNASIO")
    print("1. Gestión de Miembros")
    print("2. Gestión de Membresías")
    print("3. Gestión de Inscripciones")
    print("4. Gestión de Pagos")
    print("5. Gestión de Entrenadores")
    print("6. Gestión de Clases")
    print("7. Gestión de Reservas")
    print("8. Gestión de Rutinas")
    print("0. Salir")
    print("=" * 60)


def ejecutar_menu(titulo_menu: str, opciones: list[tuple[str, str, callable]]) -> None:
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
# 1. MIEMBROS
# =====================================================================


def menu_miembros() -> None:
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
    subtitulo("CREAR MIEMBRO")
    nombre = input("Nombre: ").strip()
    apellido = input("Apellido: ").strip()
    email = input("Email: ").strip()
    telefono = leer_telefono("Teléfono: ")
    fecha_registro = leer_fecha("Fecha de registro", usar_hoy=True)

    if crud_miembro.crear(nombre, apellido, email, telefono, fecha_registro):
        print("✓ Miembro creado correctamente.")
    else:
        print("✗ No fue posible crear el miembro (¿Email duplicado?).")


def consultar_miembros() -> None:
    subtitulo("LISTA DE MIEMBROS")
    miembros = crud_miembro.listar()  # ← Cambiado de leer_miembros()
    if not miembros:
        print("No hay miembros registrados.")
        return
    for m in miembros:
        print(f"• ID: {m.id_miembro} | {m.nombre} {m.apellido} | {m.email}")


def consultar_miembro_por_id() -> None:
    subtitulo("CONSULTAR MIEMBRO")
    id_miembro = leer_uuid("ID del miembro (UUID): ")
    miembro = crud_miembro.obtener(id_miembro)  # ← Cambiado de leer_miembro_por_id()
    print(
        f"✓ {miembro.nombre} {miembro.apellido} ({miembro.email})"
        if miembro
        else "✗ Miembro no encontrado."
    )


def actualizar_miembro() -> None:
    subtitulo("ACTUALIZAR MIEMBRO")
    id_miembro = leer_uuid("ID del miembro a actualizar (UUID): ")

    # Usar obtener() en lugar de leer_miembro_por_id()
    if not crud_miembro.obtener(id_miembro):
        print("✗ Miembro no encontrado.")
        return

    nombre = input("Nuevo nombre (Enter para mantener): ").strip() or None
    apellido = input("Nuevo apellido (Enter para mantener): ").strip() or None
    email = input("Nuevo email (Enter para mantener): ").strip() or None
    telefono = (
        leer_telefono("Nuevo teléfono (Enter para mantener): ", permitir_vacio=True)
        or None
    )

    if crud_miembro.actualizar(id_miembro, nombre, apellido, email, telefono):
        print("✓ Miembro actualizado.")
    else:
        print("✗ Error al actualizar (¿Email en uso?).")


def eliminar_miembro() -> None:
    subtitulo("ELIMINAR MIEMBRO")
    id_miembro = leer_uuid("ID del miembro a eliminar (UUID): ")
    if crud_miembro.eliminar(id_miembro):  # ← Cambiado de eliminar_miembro()
        print("✓ Miembro eliminado.")
    else:
        print("✗ Miembro no encontrado.")


# =====================================================================
# 2. MEMBRESÍAS
# =====================================================================


def menu_membresias() -> None:
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
    subtitulo("CREAR MEMBRESÍA")
    tipo = input("Tipo de membresía: ").strip()
    precio = leer_float("Precio: ")
    duracion_dias = leer_entero("Duración en días: ")
    fecha_inicio = leer_fecha("Fecha de inicio", usar_hoy=True)
    estado = input("Estado [activa]: ").strip() or "activa"

    if crud_membresia.crear_membresia(
        tipo, precio, duracion_dias, fecha_inicio, estado
    ):
        print("✓ Membresía creada.")
    else:
        print("✗ Error al crear (¿Tipo duplicado?).")


def consultar_membresias() -> None:
    subtitulo("LISTA DE MEMBRESÍAS")
    for m in crud_membresia.leer_membresias() or []:
        print(f"• ID: {m.id_membresia} | {m.tipo} | ${m.precio} | {m.estado}")


def consultar_membresia_por_id() -> None:
    id_m = leer_uuid("ID de la membresía (UUID): ")
    m = crud_membresia.leer_membresia_por_id(id_m)
    print(f"✓ {m.tipo} (${m.precio})" if m else "✗ No encontrada.")


def actualizar_membresia() -> None:
    id_m = leer_uuid("ID de la membresía (UUID): ")
    if not crud_membresia.leer_membresia_por_id(id_m):
        print("✗ No encontrada.")
        return

    tipo = input("Nuevo tipo (Enter para mantener): ").strip() or None
    precio_txt = input("Nuevo precio (Enter para mantener): ").strip()
    duracion_txt = input("Nueva duración (Enter para mantener): ").strip()
    estado = input("Nuevo estado (Enter para mantener): ").strip() or None

    precio = float(precio_txt) if precio_txt else None
    duracion = int(duracion_txt) if duracion_txt else None

    if crud_membresia.actualizar_membresia(id_m, tipo, precio, duracion, None, estado):
        print("✓ Actualizada.")
    else:
        print("✗ Error.")


def eliminar_membresia() -> None:
    id_m = leer_uuid("ID de la membresía (UUID): ")
    if crud_membresia.eliminar_membresia(id_m):
        print("✓ Eliminada.")
    else:
        print("✗ No encontrada.")


# =====================================================================
# 3. INSCRIPCIONES
# =====================================================================


def menu_inscripciones() -> None:
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
    subtitulo("CREAR INSCRIPCIÓN")
    id_miembro = leer_uuid("ID del Miembro (UUID): ")
    id_membresia = leer_uuid("ID de la Membresía (UUID): ")
    fecha_inicio = leer_fecha("Fecha de inicio", usar_hoy=True)

    # Seleccionamos el estado con el menú limpio
    estado = seleccionar_estado("Estado de la inscripción")

    # Guardamos el resultado en una variable para poder leer sus datos
    inscripcion_creada = crud_inscripcion.crear_inscripcion(
        id_miembro, id_membresia, fecha_inicio, estado
    )

    if inscripcion_creada:
        print("✓ Inscripción creada correctamente.")
        # Aquí mostramos la fecha de fin que calculó el CRUD
        print(
            f"   Fecha de fin calculada automáticamente: {inscripcion_creada.fecha_fin}"
        )
    else:
        print(
            "✗ Error: Ya existe una inscripción activa para este miembro o la membresía no existe."
        )


def consultar_inscripciones() -> None:
    for i in crud_inscripcion.leer_inscripciones() or []:
        print(f"• ID: {i.id_inscripcion} | Miembro: {i.id_miembro} | {i.estado}")


def consultar_inscripcion_por_id() -> None:
    id_i = leer_uuid("ID de inscripción (UUID): ")
    i = crud_inscripcion.leer_inscripcion_por_id(id_i)
    print(f"✓ {i.estado}" if i else "✗ No encontrada.")


def actualizar_inscripcion() -> None:
    subtitulo("ACTUALIZAR INSCRIPCIÓN")
    id_i = leer_uuid("ID de inscripción (UUID): ")

    # 1. Buscamos la inscripción actual
    inscripcion = crud_inscripcion.leer_inscripcion_por_id(id_i)
    if not inscripcion:
        print("✗ No encontrada.")
        return

    print(f"Estado actual: {inscripcion.estado}")

    # 2. Seleccionamos el nuevo estado
    nuevo_estado = seleccionar_estado("Nuevo estado")

    # 3. VALIDACIÓN: Si es el mismo, no hacemos el update
    if nuevo_estado == inscripcion.estado:
        print(
            f"⚠️ La inscripción ya está en estado '{nuevo_estado}'. No se realizaron cambios."
        )
        return

    # 4. Si es diferente, sí actualizamos
    if crud_inscripcion.actualizar_inscripcion(id_i, None, None, nuevo_estado):
        print(f"✓ Estado actualizado a '{nuevo_estado}'.")
    else:
        print("✗ Error al actualizar.")


def eliminar_inscripcion() -> None:
    id_i = leer_uuid("ID de inscripción (UUID): ")
    if crud_inscripcion.eliminar_inscripcion(id_i):
        print("✓ Eliminada.")
    else:
        print("✗ No encontrada.")


# =====================================================================
# 4. PAGOS
# =====================================================================


def menu_pagos() -> None:
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
    subtitulo("REGISTRAR PAGO")
    id_miembro = leer_uuid("ID del Miembro (UUID): ")
    monto = leer_float("Monto: ")
    fecha_pago = leer_fecha("Fecha del pago", usar_hoy=True)
    metodo = input("Método de pago: ").strip()
    concepto = input("Concepto: ").strip()

    if crud_pago.crear_pago(id_miembro, monto, fecha_pago, metodo, concepto):
        print("✓ Pago registrado.")
    else:
        print("✗ Error.")


def consultar_pagos() -> None:
    for p in crud_pago.leer_pagos() or []:
        print(
            f"• ID: {p.id_pago} | Miembro: {p.id_miembro} | ${p.monto} ({p.concepto})"
        )


def consultar_pago_por_id() -> None:
    id_p = leer_uuid("ID del pago (UUID): ")
    p = crud_pago.leer_pago_por_id(id_p)
    print(f"✓ ${p.monto}" if p else "✗ No encontrado.")


def actualizar_pago() -> None:
    id_p = leer_uuid("ID del pago (UUID): ")
    if not crud_pago.leer_pago_por_id(id_p):
        print("✗ No encontrado.")
        return

    monto_txt = input("Nuevo monto (Enter para mantener): ").strip()
    metodo = input("Nuevo método (Enter para mantener): ").strip() or None
    concepto = input("Nuevo concepto (Enter para mantener): ").strip() or None

    monto = float(monto_txt) if monto_txt else None
    if crud_pago.actualizar_pago(id_p, monto, metodo, concepto):
        print("✓ Actualizado.")
    else:
        print("✗ Error.")


def eliminar_pago() -> None:
    id_p = leer_uuid("ID del pago (UUID): ")
    if crud_pago.eliminar_pago(id_p):
        print("✓ Eliminado.")
    else:
        print("✗ No encontrado.")


# =====================================================================
# 5. ENTRENADORES
# =====================================================================


def menu_entrenadores() -> None:
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
    subtitulo("CREAR ENTRENADOR")
    nombre = input("Nombre: ").strip()
    apellido = input("Apellido: ").strip()
    especialidad = input("Especialidad: ").strip()
    telefono = leer_telefono("Teléfono: ")
    salario = leer_float("Salario: ")

    if crud_entrenador.crear_entrenador(
        nombre, apellido, especialidad, telefono, salario
    ):
        print("✓ Entrenador creado.")
    else:
        print(" Error.")


def consultar_entrenadores() -> None:
    for e in crud_entrenador.leer_entrenadores() or []:
        print(f"• ID: {e.id_entrenador} | {e.nombre} {e.apellido} | {e.especialidad}")


def consultar_entrenador_por_id() -> None:
    id_e = leer_uuid("ID del entrenador (UUID): ")
    e = crud_entrenador.leer_entrenador_por_id(id_e)
    print(f"✓ {e.nombre}" if e else "✗ No encontrado.")


def actualizar_entrenador() -> None:
    id_e = leer_uuid("ID del entrenador (UUID): ")
    if not crud_entrenador.leer_entrenador_por_id(id_e):
        print("✗ No encontrado.")
        return

    esp = input("Nueva especialidad (Enter para mantener): ").strip() or None
    tel = (
        leer_telefono("Nuevo teléfono (Enter para mantener): ", permitir_vacio=True)
        or None
    )
    sal_txt = input("Nuevo salario (Enter para mantener): ").strip()
    salario = float(sal_txt) if sal_txt else None

    if crud_entrenador.actualizar_entrenador(id_e, esp, tel, salario):
        print("✓ Actualizado.")
    else:
        print("✗ Error.")


def eliminar_entrenador() -> None:
    id_e = leer_uuid("ID del entrenador (UUID): ")
    if crud_entrenador.eliminar_entrenador(id_e):
        print("✓ Eliminado.")
    else:
        print("✗ No encontrado.")


# =====================================================================
# 6. CLASES
# =====================================================================


def menu_clases() -> None:
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
    subtitulo("CREAR CLASE")
    id_entrenador = leer_uuid("ID del Entrenador (UUID): ")
    nombre = input("Nombre de la clase: ").strip()
    dia = input("Día de la semana: ").strip()
    hora = input("Hora: ").strip()
    cap = leer_entero("Capacidad máxima: ")

    if crud_clase.crear(id_entrenador, nombre, dia, hora, cap):
        print("✓ Clase creada.")
    else:
        print("✗ Error al crear.")


def consultar_clases() -> None:
    subtitulo("LISTA DE CLASES")
    # CAMBIO: Usamos leer_clases() en lugar de listar()
    for c in crud_clase.leer_clases() or []:
        print(f"• ID: {c.id_clase} | {c.nombre} ({c.dia_semana} {c.hora})")


def consultar_clase_por_id() -> None:
    subtitulo("CONSULTAR CLASE")
    id_c = leer_uuid("ID de la clase (UUID): ")
    # CAMBIO: Usamos leer_clase_por_id() en lugar de obtener()
    c = crud_clase.leer_clase_por_id(id_c)
    print(f"✓ {c.nombre}" if c else "✗ No encontrada.")


def actualizar_clase() -> None:
    subtitulo("ACTUALIZAR CLASE")
    id_c = leer_uuid("ID de la clase (UUID): ")
    # CAMBIO: Usamos leer_clase_por_id()
    if not crud_clase.leer_clase_por_id(id_c):
        print("✗ No encontrada.")
        return

    nom = input("Nuevo nombre (Enter para mantener): ").strip() or None
    dia = input("Nuevo día (Enter para mantener): ").strip() or None
    hora = input("Nueva hora (Enter para mantener): ").strip() or None
    cap_txt = input("Nueva capacidad (Enter para mantener): ").strip()
    cap = int(cap_txt) if cap_txt else None

    # CAMBIO: Usamos actualizar_clase()
    if crud_clase.actualizar_clase(id_c, nom, dia, hora, cap):
        print("✓ Actualizada.")
    else:
        print("✗ Error.")


def eliminar_clase() -> None:
    subtitulo("ELIMINAR CLASE")
    id_c = leer_uuid("ID de la clase (UUID): ")

    # Primero verificamos que exista
    clase = crud_clase.leer_clase_por_id(id_c)
    if not clase:
        print("✗ Clase no encontrada.")
        return

    print(f"Clase: {clase.nombre} ({clase.dia_semana} {clase.hora})")

    if confirmar("¿Desea eliminar esta clase?"):
        if crud_clase.eliminar_clase(id_c):
            print("✓ Clase eliminada correctamente.")
        else:
            print("✗ No se pudo eliminar la clase.")
            print("  ⚠️ Posible causa: La clase tiene reservas asociadas.")
            print("  💡 Solución: Elimina primero las reservas de esta clase.")
    else:
        print("Operación cancelada.")


# =====================================================================
# 7. RESERVAS
# =====================================================================


def menu_reservas() -> None:
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
    subtitulo("CREAR RESERVA")
    id_miembro = leer_uuid("ID del Miembro (UUID): ")
    id_clase = leer_uuid("ID de la Clase (UUID): ")
    fecha = leer_fecha("Fecha de reserva", usar_hoy=True)
    estado = seleccionar_estado("Estado de la reserva")

    if crud_reserva_clase.crear(id_miembro, id_clase, fecha, estado):
        print("✓ Reserva creada.")
    else:
        print("✗ Error al crear (¿Miembro o Clase no existen?).")


def consultar_reservas() -> None:
    subtitulo("LISTA DE RESERVAS")
    # CAMBIO: Usamos listar() en lugar de leer_reservas()
    for r in crud_reserva_clase.listar() or []:
        print(
            f"• ID: {r.id_reserva} | Miembro: {r.id_miembro} | Clase: {r.id_clase} | {r.estado}"
        )


def consultar_reserva_por_id() -> None:
    subtitulo("CONSULTAR RESERVA")
    id_r = leer_uuid("ID de la reserva (UUID): ")
    # CAMBIO: Usamos obtener() en lugar de leer_reserva_por_id()
    r = crud_reserva_clase.obtener(id_r)
    print(f"✓ {r.estado}" if r else "✗ No encontrada.")


def actualizar_reserva() -> None:
    subtitulo("ACTUALIZAR RESERVA")
    id_r = leer_uuid("ID de la reserva (UUID): ")
    # CAMBIO: Usamos obtener()
    if not crud_reserva_clase.obtener(id_r):
        print("✗ No encontrada.")
        return

    estado = seleccionar_estado("Nuevo estado de la reserva")

    # CAMBIO: Usamos actualizar()
    if crud_reserva_clase.actualizar(id_r, estado):
        print("✓ Actualizada.")
    else:
        print("✗ Error.")


def eliminar_reserva() -> None:
    subtitulo("ELIMINAR RESERVA")
    id_r = leer_uuid("ID de la reserva (UUID): ")
    # CAMBIO: Usamos eliminar()
    if crud_reserva_clase.eliminar(id_r):
        print("✓ Eliminada.")
    else:
        print("✗ No encontrada.")


# =====================================================================
# 8. RUTINAS
# =====================================================================


def menu_rutinas() -> None:
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
    subtitulo("CREAR RUTINA")
    id_miembro = leer_uuid("ID del Miembro (UUID): ")
    id_entrenador = leer_uuid("ID del Entrenador (UUID): ")
    nombre = input("Nombre de la rutina: ").strip()
    desc = input("Descripción: ").strip()
    fecha = leer_fecha("Fecha de creación", usar_hoy=True)

    if crud_rutina.crear(id_miembro, id_entrenador, nombre, desc, fecha):
        print("✓ Rutina creada.")
    else:
        print("✗ Error al crear.")


def consultar_rutinas() -> None:
    subtitulo("LISTA DE RUTINAS")
    # CAMBIO: listar()
    for r in crud_rutina.listar() or []:
        print(f"• ID: {r.id_rutina} | {r.nombre} (Miembro: {r.id_miembro})")


def consultar_rutina_por_id() -> None:
    subtitulo("CONSULTAR RUTINA")
    id_r = leer_uuid("ID de la rutina (UUID): ")
    # CAMBIO: obtener()
    r = crud_rutina.obtener(id_r)
    print(f"✓ {r.nombre}" if r else "✗ No encontrada.")


def actualizar_rutina() -> None:
    subtitulo("ACTUALIZAR RUTINA")
    id_r = leer_uuid("ID de la rutina (UUID): ")
    if not crud_rutina.obtener(id_r):
        print("✗ No encontrada.")
        return

    nom = input("Nuevo nombre (Enter para mantener): ").strip() or None
    desc = input("Nueva descripción (Enter para mantener): ").strip() or None

    if crud_rutina.actualizar(id_r, nom, desc):
        print("✓ Actualizada.")
    else:
        print("✗ Error.")


def eliminar_rutina() -> None:
    subtitulo("ELIMINAR RUTINA")
    id_r = leer_uuid("ID de la rutina (UUID): ")
    if crud_rutina.eliminar(id_r):
        print("✓ Eliminada.")
    else:
        print("✗ No encontrada.")


# =====================================================================
# MAIN
# =====================================================================


def main() -> None:
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
        elif opcion == "0":
            titulo("SISTEMA FINALIZADO")
            print("✓ Todos los cambios han sido guardados en la base de datos Neon.")
            print("¡Gracias por utilizar el sistema! 👋")
            break
        else:
            print("\n✗ Opción inválida.")
            pausar()


if __name__ == "__main__":
    main()
