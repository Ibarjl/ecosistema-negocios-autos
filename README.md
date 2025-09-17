
# ECOSISTEMA-NEGOCIOS-AUTOS
**WORK IN PROGRESS!**

Ecosistema digital modular para el sector automotriz, diseñado para escalar y facilitar el desarrollo colaborativo.

## 🗂️ Estructura principal del repositorio

```
backend_rx/         # Lógica de negocio, autenticación, modelos y servicios
  apps/             # Módulos funcionales: autenticación, mercado, modelos, servicio
compartido/         # Constantes, esquemas y tipos reutilizables
frontend_rx/        # Frontend principal: componentes, estados, estilos, páginas
mercado/            # Marketplace especializado y recursos visuales
main/               # Entrada principal de la aplicación
alembic/            # Migraciones de base de datos
assets/             # Recursos estáticos
reflex.db           # Base de datos local
requirements.txt    # Dependencias del proyecto
rxconfig.py         # Configuración Reflex
```

## 📦 Módulos principales

- **backend_rx/**: Lógica de negocio, autenticación, modelos de datos y servicios comunes.
- **compartido/**: Esquemas, constantes y tipos de datos reutilizables en todo el ecosistema.
- **frontend_rx/**: Componentes, estados, estilos y páginas del frontend principal.
- **mercado/**: Marketplace para compra/venta de autos, frontend especializado y recursos visuales.
- **main/**: Punto de entrada de la aplicación.

La arquitectura facilita la integración de nuevas funcionalidades y la reutilización de código.

---

> **¿Primera vez en el proyecto?**
> - Para instrucciones detalladas y ejemplos, revisa [Quick_Start.md](./Quick_Start.md).
> - Para aprender Reflex y practicar, revisa [Aprendizaje_reflex.md](./Aprendizaje_reflex.md).

---

## 🚀 Guía rápida para comenzar

1. **Clona el repositorio:**
   ```bash
   git clone <URL-del-repositorio>
   cd ecosistema-negocios-autos
   ```

2. **Crea y activa un entorno virtual:**
   - En Windows:
     ```bash
     python -m venv .venv
     .venv\Scripts\activate
     ```
   - En Linux/Mac:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

3. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecuta la aplicación (usando Reflex):**
   ```bash
   reflex run
   ```

5. **¡Listo!**
   Ya puedes comenzar a desarrollar y colaborar en el proyecto.

---

## 🤝 Recomendaciones para colaboradores

- Sigue la estructura modular para nuevas funcionalidades.
- Documenta tus cambios y actualiza los archivos relevantes.
- Usa entornos virtuales para evitar conflictos de dependencias.
- Revisa los archivos de ayuda y ejemplos antes de comenzar.

---

¿Dudas o sugerencias? Abre un issue o contacta a los mantenedores.
