# Adventurero

Aplicacion Django para una agencia de viajes con tours, usuarios, roles, reservas, comentarios y documentacion tecnica.

## Ejecutar en local

```bash
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

Luego abre `http://127.0.0.1:8000/`.

Tambien puedes usar los scripts npm configurados para Vercel:

```bash
npm run dev
npm run build
```

## Pruebas

```bash
python -m pytest
```

## Despliegue en Vercel

Este proyecto es Django con templates, CSS y JavaScript puro. En Vercel configura el directorio raiz como `tours`, porque ahi estan `manage.py`, `requirements.txt`, `package.json` y `vercel.json`.

Variables recomendadas en Vercel:

```bash
SECRET_KEY=tu-clave-segura
DEBUG=False
ALLOWED_HOSTS=.vercel.app,tu-proyecto.vercel.app
```

Pasos para subir a GitHub:

```bash
git init
git add .
git commit -m "Preparar proyecto Django para Vercel"
git branch -M main
git remote add origin https://github.com/tu-usuario/tu-repositorio.git
git push -u origin main
```

Pasos para conectar con Vercel:

1. Entra a Vercel y elige `Add New Project`.
2. Importa el repositorio de GitHub.
3. En `Root Directory`, selecciona `tours`.
4. Agrega las variables de entorno anteriores.
5. Deja que Vercel use los comandos de `vercel.json`.
6. Pulsa `Deploy`.

Para actualizar despues del primer deploy:

```bash
git add .
git commit -m "Actualizar Adventurero"
git push
```

Cada push a `main` genera un nuevo despliegue automaticamente.

## Funcionalidades incluidas

- Proyecto Django real con app `core`.
- Modelos: perfiles/roles, categorias, tours, reservas, comentarios y favoritos.
- Registro, login, logout, sesiones, hash de contrasenas y CSRF.
- Login/logout con vistas explicitas y redireccion funcional.
- CRUD de tours restringido a administradores o usuarios staff.
- Listado, busqueda y filtro de tours desde base de datos.
- Reservas para usuarios autenticados.
- Imagenes de tours con `ImageField`, `MEDIA_URL` y `MEDIA_ROOT`.
- HTML centralizado en `templates/` usando `templates/base.html`.
- Datos demo con `python manage.py seed_demo`.
- Documentacion tecnica en `docs/proyecto.md`.
