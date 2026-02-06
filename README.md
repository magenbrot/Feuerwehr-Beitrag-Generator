![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fgithub.com%2Fmagenbrot%2FFeuerwehr-Beitrag-Generator%2Fraw%2Frefs%2Fheads%2Fmain%2Fpackage.json&query=version&label=Version)
[![CodeQL](https://github.com/magenbrot/Feuerwehr-Beitrag-Generator/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/magenbrot/Feuerwehr-Beitrag-Generator/actions/workflows/github-code-scanning/codeql)
[![Publish Docker image](https://github.com/magenbrot/Feuerwehr-Beitrag-Generator/actions/workflows/docker-image.yml/badge.svg)](https://github.com/magenbrot/Feuerwehr-Beitrag-Generator/actions/workflows/docker-image.yml)
[![Dependabot Updates](https://github.com/magenbrot/Feuerwehr-Beitrag-Generator/actions/workflows/dependabot/dependabot-updates/badge.svg)](https://github.com/magenbrot/Feuerwehr-Beitrag-Generator/actions/workflows/dependabot/dependabot-updates)

# Feuerwehr-Beitrag-Generator

Erstelle einen Social Media Post für Facebook und Instagram für deine Feuerwehr in Sekunden.

Demo-Website: [112.ovtec.it](https://112.ovtec.it/)

Forked from [Turbopixel](https://github.com/turbopixel/Feuerwehr-Beitrag-Generator)

## Konfiguration

Damit der Generator für deine Feuerwehr passt (Ortsnamen, Fahrzeuge, Tags), musst du eine Konfigurationsdatei anlegen.

1.  Kopiere die Vorlage:
    ```sh
    cp src/config.js.dist src/config.js
    ```
2.  Bearbeite `src/config.js` und trage deine lokalen Daten ein (Ortsnamen, Einheiten, Standard-Tags).

*Hinweis: `src/config.js` wird von git ignoriert, damit deine persönlichen Einstellungen nicht versehentlich veröffentlicht werden.*

## Mitmachen

Dieses Projekt ist in vue.js mit vite entwickelt. Führe auf deiner Konsole die folgenden
Befehle aus, um an diesem Projekt mitzumachen.

[Forke](https://github.com/magenbrot/Feuerwehr-Beitrag-Generator/fork) dieses Repository und checke den Code in deiner lokalen Umgebung aus.

### Lokal ausführen

#### 1. npm Pakete installieren

```sh
npm install
```

#### 2. Konfiguration erstellen
(Siehe oben unter "Konfiguration")

#### 3. Projekt lokal ausführen mit hot-reload

```sh
npm run dev
```

#### 4. Projekt kompilieren

```sh
npm run build
```

## Docker / Deployment

### Manuelles Bauen

Wenn du das Docker-Image lokal baust, stelle sicher, dass du vorher `src/config.js` angelegt hast. Diese wird beim Build-Prozess fest in die Anwendung integriert.

```sh
docker build -t ffpostcreator .
```

### GitHub Actions (CI/CD)

Da die `src/config.js` nicht im Repository liegt, muss sie für den automatischen Build-Prozess via GitHub Secrets bereitgestellt werden.

1.  Kodiere deine lokale `src/config.js` als Base64:
    ```sh
    base64 -w 0 src/config.js
    # MacOS: base64 -b 0 src/config.js
    ```
2.  Gehe in deinem GitHub Repository zu **Settings** -> **Secrets and variables** -> **Actions**.
3.  Erstelle ein neues **Repository Secret** mit dem Namen `APP_CONFIG_BASE64`.
4.  Füge den Base64-String als Wert ein.

Der Workflow (`docker-image.yml`) prüft beim Bauen, ob dieses Secret existiert, und injiziert die Konfiguration automatisch vor dem Build. Existiert das Secret nicht, wird die Standard-Konfiguration (`src/config.js.dist`) verwendet.

### Deployment via Docker Compose

```yaml
services:
  ffpostcreator:
    image: ghcr.io/magenbrot/feuerwehr-beitrag-generator:latest
    container_name: ffpostcreator
    ports:
      - 8095:80
    restart: unless-stopped
```
