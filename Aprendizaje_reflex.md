# 🚀 SEMANA 1 - APRENDER COMPONENTES REFLEX

## 🎯 OBJETIVO FINAL
Al final de la semana, todos tendrán una página que:
- Muestre "AutoMercado" como título
- Permita escribir su nombre en un campo
- Muestre "Hola, [su nombre]" dinámicamente

**Con 3 componentes separados que trabajen juntos.**

---

## 📅 DÍA 1: INSTALACIÓN Y PRIMER COMPONENTE

### **Objetivo del día:**
Crear un componente que muestre "AutoMercado" en el navegador.

### **Setup inicial:**
```bash
# Instalar Python y pip si no los tienen
pip install reflex
reflex init automercado
cd automercado
reflex run
```

### **Pistas para el primer componente:**
```python
import reflex as rx

def mi_primer_componente() -> rx.Component:
    # Aquí necesitas devolver algo que muestre texto
    # Pista: rx.text() o rx.heading() pueden ser útiles
    pass

app = rx.App()
# ¿Cómo agregas una página que use tu componente?
```

**🎯 Objetivo específico:** Ver "AutoMercado" en grande en el navegador
**💡 Pista clave:** Un componente es una función que devuelve algo visual

---

## 📅 DÍA 2: SEGUNDO COMPONENTE CON INTERACTIVIDAD

### **Objetivo del día:**
Crear un componente con un campo de texto donde puedan escribir su nombre.

### **Pistas para el segundo componente:**
- Necesitarás algo llamado "State" para recordar lo que escriben
- `rx.input()` es útil para campos de texto
- El State tiene variables que cambian cuando el usuario hace algo

```python
class MiEstado(rx.State):
    # ¿Qué variable necesitas para guardar el nombre?
    pass

def componente_nombre() -> rx.Component:
    # ¿Cómo conectas un input con el estado?
    pass
```

**🎯 Objetivo específico:** Escribir en un campo y que "algo" recuerde lo que escribieron
**💡 Pista clave:** Para que algo "recuerde", necesitas State

---

## 📅 DÍA 3: TERCER COMPONENTE QUE SE ACTUALIZA

### **Objetivo del día:**
Crear un componente que muestre "Hola, [nombre]" y cambie cuando escriben algo diferente.

### **Pistas para el tercer componente:**
- Este componente necesita "leer" lo que está guardado en el State
- Cuando el State cambia, el componente se actualiza solo
- `rx.text()` puede mostrar texto dinámico

```python
def componente_saludo() -> rx.Component:
    # ¿Cómo accedes a la variable del State desde aquí?
    # ¿Cómo combinas texto fijo ("Hola, ") con texto variable?
    pass
```

**🎯 Objetivo específico:** Ver "Hola, [su nombre]" que cambia mientras escriben
**💡 Pista clave:** Los componentes pueden "leer" del State automáticamente

---

## 📅 DÍA 4: JUNTAR LOS TRES COMPONENTES

### **Objetivo del día:**
Hacer que los 3 componentes aparezcan juntos en una sola página.

### **Pistas para la integración:**
- Necesitas una función que combine los 3 componentes
- `rx.vstack()` apila cosas verticalmente
- `rx.hstack()` pone cosas lado a lado

```python
def pagina_completa() -> rx.Component:
    return rx.vstack(
        # ¿Cómo llamas a tus 3 componentes aquí?
        # ¿En qué orden los pones?
    )
```

**🎯 Objetivo específico:** Los 3 componentes trabajando juntos en una página bonita
**💡 Pista clave:** Los componentes se pueden combinar como piezas de LEGO

---

## 📅 DÍA 5: MEJORAR EL DISEÑO

### **Objetivo del día:**
Hacer que se vea mejor con colores, espacios y estilos.

### **Pistas para el styling:**
- Los componentes pueden tener parámetros como `color`, `font_size`, `padding`
- `rx.center()` centra cosas
- `bg` cambia el color de fondo

```python
def componente_bonito() -> rx.Component:
    return rx.vstack(
        rx.heading("AutoMercado", color="blue", font_size="2xl"),
        # ¿Qué otros estilos puedes agregar?
        # ¿Cómo haces que tenga más espacio entre elementos?
        spacing="2rem",  # Pista gratis
        padding="2rem"
    )
```

**🎯 Objetivo específico:** Una página que se vea profesional y no como un ejercicio
**💡 Pista clave:** Los estilos hacen que los componentes se vean como una app real

---

## 🎯 CONCEPTOS CLAVE QUE HABRÁN APRENDIDO

Al final de la semana entenderán:

### **¿Qué es un componente?**
Una función que devuelve algo visual que se puede reutilizar.

### **¿Cómo funciona el State?**
Un lugar donde guardar información que puede cambiar y que los componentes pueden leer.

### **¿Cómo se comunican los componentes?**
A través del State compartido - uno escribe, otro lee, automáticamente se actualiza.

### **¿Cómo se organiza una aplicación?**
Componentes pequeños que se combinan para hacer páginas completas.

---

## 🔄 PATRÓN DIARIO RECOMENDADO

**Para cada día:**

1. **Primera hora:** Leer el objetivo y las pistas
2. **Segunda hora:** Experimentar y escribir código
3. **Tercera hora:** Hacer que funcione y probarlo
4. **Opcional:** Tomar screenshot de lo que lograron

**Al final del día:** Cada uno debería poder mostrar su progreso funcionando

---

## 🎉 RESULTADO FINAL

Al final de la semana, todos tendrán:
- ✅ Una página web funcionando
- ✅ Entendimiento práctico de componentes
- ✅ Experiencia con State
- ✅ Confianza para especializarse en sus roles

**Y lo más importante:** Sabrán que pueden construir cosas reales con Reflex.

---

## 📚 RECURSOS DE APOYO

- **Documentación oficial:** https://reflex.dev/docs/
- **Ejemplos simples:** https://reflex.dev/docs/getting-started/
- **Si algo no funciona:** Leer el mensaje de error completo (casi siempre dice qué está mal)

**Regla de oro:** Si algo no funciona después de 30 minutos, está bien parar y probar algo más simple. El objetivo es aprender, no frustrarse.

---

