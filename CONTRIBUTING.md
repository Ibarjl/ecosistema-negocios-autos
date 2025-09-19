# Guía de Contribución - Ecosistema Negocios Autos

## Introducción 
Esta guía te ayudara a entender el proceso de contribución al proyecto, las convenciones y mejores prácticas que se deben seguir para contribuir de manera efectiva.

## Estructura de Ramas
Seguimos un modelo de ramas basado en permisos especificos:

- `main`: Rama principal que contiene el código de producción.
- `ramas personales` : Cada desarrollador tiene su propia rama para trabajar en sus cambios.
    - Las ramas personales deben solicitarse a Ibar.
    - Cada colaborador es responsable de mantener su rama actualizada con la rama principal.

## Proceso de Contribución

1. Clonar el repositorio: 
```bash
git clone https://github.com/Ibarjl/ecosistema-negocios-autos.git
```
2. Cambiar a tu rama:
```bash
git checkout <tu-rama>
```
3. Mantener tu rama actualizada:
```bash
git checkout main 
git pull
git checkout <tu-rama>
git merge main

4. Commit de cambios:
git add .
git commit -m "Descripción de los cambios"

5. Push a tu rama:
git push origin <tu-rama>
```
## Commits Frecuentes
- `feat`: Se utiliza cuando se introduce una nueva funcionalidad.
- `fix`: Se utiliza cuando se corrige un error.
- `docs`: Se utiliza cuando se realizan cambios en la documentación.
- `style`: Se utiliza cuando se realizan cambios en el formato o la presentación del código (sin cambios en la lógica).
- `refactor`: Se utiliza cuando se realizan cambios en el código que no son ni una corrección ni una nueva funcionalidad.
- `test`: Se utiliza cuando se realizan cambios en los tests.
- `chore`: Se utiliza cuando se realizan cambios en el proceso de construcción, la configuración o las herramientas.

## Revision de codigo 
Ibar se encargara de revisar y fusionar tus cambios en la rama principal.
Aborda todos los comentarios y sugerencias. 


