# 1. Inicializa Git en tu carpeta
git init

# 2. Agrega todos los archivos permitidos (app.py, requirements.txt, .gitignore)
git add .

# 3. Guarda esta versión con un mensaje
git commit -m "Primera versión: App de limpieza de vigencia RRHH"

# 4. Cambia el nombre de la rama principal a "main"
git branch -M main

# 5. Conecta tu carpeta local con tu repositorio de GitHub 
# (Copia la URL exacta que te da GitHub en su página)
git remote add origin https://github.com/TU_USUARIO/depurador-rrhh.git

# 6. Empuja el código a GitHub
git push -u origin main
