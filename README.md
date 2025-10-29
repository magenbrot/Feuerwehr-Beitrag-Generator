![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fgithub.com%2Fmagenbrot%2FFeuerwehr-Beitrag-Generator%2Fraw%2Frefs%2Fheads%2Fmain%2Fpackage.json&query=version&label=Version)
[![CodeQL](https://github.com/magenbrot/Feuerwehr-Beitrag-Generator/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/magenbrot/Feuerwehr-Beitrag-Generator/actions/workflows/github-code-scanning/codeql)
[![Publish Docker image](https://github.com/magenbrot/Feuerwehr-Beitrag-Generator/actions/workflows/docker-image.yml/badge.svg)](https://github.com/magenbrot/Feuerwehr-Beitrag-Generator/actions/workflows/docker-image.yml)
[![Dependabot Updates](https://github.com/magenbrot/Feuerwehr-Beitrag-Generator/actions/workflows/dependabot/dependabot-updates/badge.svg)](https://github.com/magenbrot/Feuerwehr-Beitrag-Generator/actions/workflows/dependabot/dependabot-updates)

# Feuerwehr-Beitrag-Generator

Erstelle ein Social Media Post für Facebook und Instagram für deine Feuerwehr in Sekunden. Dieser Fork ist angepasst für die Freiwillige Feuerwehr Werdau.

Demo-Website: [112.ovtec.it](https://112.ovtec.it/)

Forked from [Turbopixel](https://github.com/turbopixel/Feuerwehr-Beitrag-Generator)

## vite Konfiguration

[Vite Configuration Reference](https://vitejs.dev/config/).

## Mitmachen

Dieses Projekt ist in vue.js mit vite entwickelt. Führe auf deiner Konsole die folgenden
Befehle aus, um an diesem Projekt mitzumachen.

[Forke](https://github.com/magenbrot/Feuerwehr-Beitrag-Generator/fork) dieses Repository und checke den Code in deiner lokalen Umgebung aus.

### Mit Docker entwickeln/veröffentlichen

siehe auch [Wiki](https://github.com/magenbrot/Feuerwehr-Beitrag-Generator/wiki/Pers%C3%B6nliche-Notizen-zur-Erzeugung-eines-neuen-Releases)

#### Code anpassen

Mach die notwendigen Änderungen am Code. Erzeuge auch gerne einen Pull Request für dieses Repository.

#### Docker image erzeugen und testen

```sh
docker buildx build . -t magenbrot/ffpostcreator
docker run -it -p 8080:80 --rm --name ffpostcreator <your-dockerid>/ffpostcreator:latest
```

Die App ist jetzt zum lokalen Testen unter [http://127.0.0.1:8080/](http://127.0.0.1:8080/) erreichbar

#### Docker Image veröffentlichen

```sh
docker login -u <your-username> --password-stdin
# Passwort nach Aufforderung eingeben
# Ein erfolgreicher Login wird mit 'Login Succeeded' angezeigt

docker push <your-dockerid>/ffpostcreator
# ohne Angabe eines Tags (: nach dem Namen) wird der Tag 'latest' verwendet
```

#### Deployment

Für die Veröffentlichung der App empfiehlt es sich einen Reverseproxy mit HTTPS wie nginx davor zu setzen.

Beispiel via Docker Compose:

```sh
  ffpostcreator:
    image: <your-dockerid>/ffpostcreator:latest
    container_name: ffpostcreator
    ports:
      - 8095:80
    restart: unless-stopped
```

### Lokal ausführen

#### npm Pakete installieren

```sh
npm install
```

#### Projekt lokal ausführen mit hot-reload

```sh
npm run dev
```

#### Projekt kompilieren

```sh
npm run build
```
