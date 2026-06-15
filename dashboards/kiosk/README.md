# 🏠 Kiosk-dashboard for Home Assistant (iPad)

Et mørkt glassmorphism-dashbord inspirert av **Tunet** og **ha-fusion**, bygget
som vanlig Lovelace så det lever inni HA-en din og er enkelt å skalere.

Visuelt mål: se `mockup/v3_home.png` i repoet.

> ⚠️ **Status: utkast.** Alle entiteter er placeholders (`ENDRE_…`). Jeg når
> ikke HA-instansen din herfra, så send meg entitetslista di (Utviklerverktøy →
> Tilstander), eller bytt dem inn selv. Da finjusterer vi.

---

## 1. HACS-kort som må installeres

Alt er i HACS → *Frontend* → søk og installer:

| Kort | Hva det gjør i dashbordet |
|------|---------------------------|
| **Mushroom** | Pillene, lys/klima/media/vifte-kortene |
| **bubble-card** | Rom-popups (undermenyene per rom) |
| **apexcharts-card** | Strøm/forbruk-grafene |
| **card-mod** | Glass-effekten (blur) i temaet |
| **kiosk-mode** | Skjuler HA sin sidemeny + topptekst |

> Sections-grid, weather-, gauge-, thermostat-, energy- og picture-kortene er
> innebygd i HA – ingen installasjon.

Etter installasjon: **tøm cache / hard refresh** på iPaden.

---

## 2. Legg inn temaet

1. Kopier `theme_glass_kiosk.yaml` til `config/themes/`.
2. Sjekk at `configuration.yaml` har:
   ```yaml
   frontend:
     themes: !include_dir_merge_named themes
   ```
3. Utviklerverktøy → YAML → **Reload themes**.

---

## 3. Legg inn dashbordet

1. Innstillinger → Dashboards → **Legg til dashboard** → Ny tom → gi den
   URL/sti `lovelace-kiosk` (matcher navigasjonen i YAML-en).
2. Åpne dashbordet → 3 prikker → **Rediger** → 3 prikker → **Rå konfigurasjons-editor**.
3. Lim inn hele `dashboard.yaml`, lagre.
4. 3 prikker → Rediger → **Tema: Glass Kiosk**.

> Bruker du `navigation_path`-ene som de er, må dashbordets sti være
> `lovelace-kiosk`. Endrer du stien, søk/erstatt `lovelace-kiosk` i YAML-en.

---

## 4. Kioskmodus (rent utseende)

I `kiosk-mode` legger du i toppen av `dashboard.yaml`:
```yaml
kiosk_mode:
  hide_header: true
  hide_sidebar: true
```
Da forsvinner HA sin meny og topplinje, og bare dashbordet vises.

---

## 5. Lås iPaden (skjul de private bildene)

Kioskmodus styrer bare *utseendet*. For å hindre at noen går ut av dashbordet
og inn i bildene dine:

1. Åpne dashbordet i **HA Companion-appen** eller Safari (fullskjerm).
2. iPad: Innstillinger → Tilgjengelighet → **Veiledet tilgang** → på.
3. Trippelklikk sideknappen for å låse iPaden til *kun* denne appen.
   Da kommer man ikke ut uten koden din.

(Vil du ha automatisk gjenoppstart/alltid-på, kan vi senere se på en dedikert
veggtablet-app, men Veiledet tilgang dekker «begrenset kontroll» helt fint.)

---

## 6. Skalering – legge til nye ting senere

- **Nytt rom:** kopier en `ROM-BLOKK` (markert i `dashboard.yaml`), bytt
  hash + entiteter. Legg til et romkort i «Romsnarveier».
- **Ny enhet:** legg et Mushroom-kort i riktig kolonne/seksjon.
- **Ny underside:** kopier en hel `view:` og legg en chip i fane-navigasjonen.
- Seksjons-visningen ordner kortene responsivt selv – du drar dem bare på plass
  i redigeringsmodus.

---

## 7. Det jeg trenger fra deg for å gjøre den «ekte»

Send meg gjerne, så bytter jeg ut alle `ENDRE_…`:
- Personer (`person.*`), vær (`weather.*`)
- Strømpris-sensor (Nordpool/Tibber) + effekt-nå-sensor
- Elbil-lader (effekt/%/status) + bil (batteri/rekkevidde/device_tracker)
- Lys per rom, klima/termostater, vifter
- Media (Sonos/TV), kameraer, alarm

Enkleste vei: Utviklerverktøy → Tilstander → kopier lista, eller send skjermbilde.
