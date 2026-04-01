# Python FC — Sistema de Gestión de Cancha 4-3-3

Proyecto de evaluación del Módulo 4 del Bootcamp Python SENCE.
Sistema de gestión de plantilla de fútbol con visualización interactiva en terminal.

**Repositorio:** https://github.com/Angelopaolo23/python-fc

---

## ¿Qué hace?

Permite construir un equipo de fútbol posición por posición sobre una formación 4-3-3, con persistencia de datos y visualización en tiempo real de la cancha en la terminal.

- Agregar jugadores y capitanes a posiciones específicas de la formación
- Validar datos de entrada con reglas de negocio (edad, goles, nombre, posición)
- Persistir el equipo en disco y recuperarlo automáticamente al iniciar
- Visualizar la cancha actualizada tras cada jugador agregado

---

## Objetivos de aprendizaje

### Programación Orientada a Objetos
- Herencia: `Capitan` extiende `Jugador` usando `super()`
- Polimorfismo: `mostrar_info()` se comporta distinto según la clase
- Encapsulamiento: cada clase tiene una responsabilidad única y definida

### Arquitectura y Patrones de Diseño
- **Patrón Repository**: separación total entre la lógica de negocio y la persistencia de datos
- **Arquitectura Limpia**: las capas internas (modelos) no conocen a las capas externas (renderer, main)
- **Principio de Responsabilidad Única (SRP)**: cada módulo hace una sola cosa

### Manejo de Archivos y Persistencia
- Serialización de objetos Python a JSON con campo `"tipo"` para preservar la clase
- Rehidratación: reconstrucción de objetos `Jugador` o `Capitan` desde datos planos
- Uso de `pathlib.Path` para manejo de rutas

### Excepciones Personalizadas
- Jerarquía de errores con clase base `EquipoError`
- Errores específicos por tipo de validación: `EdadInvalidaError`, `GolesInvalidosError`, `PosicionInvalidaError`, `LargoNombreError`
- Manejo con `try/except` en el bucle principal

### Type Hinting
- Anotaciones de tipo en todos los métodos y atributos
- Uso de `Dict`, `Union`, `Optional` del módulo `typing`

### Librería Rich
- Renderizado de tablas con `rich.table.Table`
- Paneles anidados con `rich.panel.Panel`
- Layout en columnas con `rich.columns.Columns`
- Objetos `Text` con estilos aplicados programáticamente

---

## Estructura del proyecto

```
app/
  models.py       — Jugador y Capitan
  exceptions.py   — Errores personalizados del dominio
  validators.py   — Validación de reglas de negocio
  repository.py   — Persistencia JSON (Patrón Repository)
  renderer_v2.py  — Visualización de la cancha con Rich
data/
  jugadores.json  — Datos del equipo (generado automáticamente)
main.py           — Orquestador principal
```

---

## Instalación y uso

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar
python main.py
```

### Posiciones disponibles (formación 4-3-3)

| Línea | Posiciones |
|---|---|
| Arquero | `ARQ` |
| Defensa | `DEF1` `DEF2` `DEF3` `DEF4` |
| Mediocampo | `MED1` `MED2` `MED3` |
| Delantera | `DEL1` `DEL2` `DEL3` |

### Reglas de validación

| Campo | Regla |
|---|---|
| Nombre | Entre 2 y 25 caracteres |
| Edad | Entre 15 y 50 años |
| Goles | No negativos |
| Posición | Debe ser una de las 11 posiciones válidas |
| Liderazgo | Entre 1 y 10 (solo capitanes) |

---

## Tecnologías

- Python 3.10+
- [Rich](https://github.com/Textualize/rich) — visualización en terminal
