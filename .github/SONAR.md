# SonarCloud setup for this repository

Pasos rápidos para que el análisis en SonarCloud funcione correctamente:

1. Crear/Importar el proyecto en SonarCloud
   - Entra en https://sonarcloud.io y haz login con tu cuenta de GitHub.
   - Selecciona la organización `everocha11`.
   - Ve a **Projects → Analyze new project** y elige el repositorio `EveRocha11/VetRed`.
   - Confirma el `projectKey` como `EveRocha11_VetRed` (o ajusta `sonar-project.properties`).

2. Generar token en SonarCloud
   - En SonarCloud: `My Account` → `Security` → `Generate Tokens`.
   - Copia el token (no podrás verlo después).

3. Añadir secreto en GitHub
   - En el repositorio: `Settings → Secrets and variables → Actions` → `New repository secret`.
   - Nombre: `SONAR_TOKEN`
   - Valor: pega el token generado en SonarCloud.

4. Ejecutar el workflow
   - Abre un PR desde la rama `fix/sonar-key` hacia `main` o haz push a `main`.
   - En GitHub: `Actions` → selecciona `SonarCloud Scan` y revisa los logs.

5. Comandos útiles (opcional, usando GitHub CLI `gh`)
   - Crear PR desde la rama actual:
     `gh pr create --title "Fix SonarCloud config" --body "Alinea projectKey and workflow" --base main --head fix/sonar-key --web`

6. Notas
   - Si ves `Could not find a default branch for project with key '...'`, asegúrate que el proyecto fue importado en SonarCloud y que tiene una rama por defecto (`main`).
   - Si ves `Unauthorized`, revisa que `SONAR_TOKEN` esté correcto.
