# Playbook contenuti Instagram — profilo emanuelefranzini1

Guida tecnica per la sessione che ogni sera prepara i contenuti del giorno dopo.

## Stile visivo (non cambiarlo)

- Fondo carta a quadretti, schede tipo finestra con tre pallini, etichetta in monospace in alto (`// 01 · tema` e contatore `1/5`).
- Titoli in Montserrat 800 blu navy `#002B5C`; la parola chiave in Playfair Display corsivo arancione `#FF6B00`.
- Logo ControlIA in basso a destra su ogni immagine e su ogni fotogramma. Nessuna firma testuale.
- Nessuna mascotte, nessun elemento copiato da altri profili.

## Generatore

Cartella `generator/`: `fonts/` (Montserrat, Playfair, JetBrains Mono), `logo.png`, `reel/`.

- `reel/render2.py`: base (fondo, `Frame.layer`, `card`, `pill`, `rich`, `pr`, `ease`).
- `reel/reels.py`: aiuti per i video (`Hd` titoli, `header`, `T`, `pillL`, `tick`, `typed`, `stamp`, `cta`, `mini`, `put_logo`, `frame`) e tre reel di esempio. Un reel è una lista di `(funzione_scena, durata)`; aggiungilo al dizionario `REELS`. `python3 reels.py preview` crea i fogli di controllo, `python3 reels.py full` crea gli mp4 (1080x1920, 30 fps) in `/home/claude/reel/`.
- `reel/drafts.py`: esempi di storie (1080x1920) e slide di carosello (1080x1350) statiche.

Servono Python con Pillow e `ffmpeg`. Per ogni nuovo contenuto scrivi un nuovo file nella stessa cartella che importa questi aiuti; non modificare gli esempi.

Controlli prima di consegnare: guarda un fotogramma o l'immagine di ogni scena; nessun testo deve uscire dalle schede o dai margini (90 px ai lati); nelle storie e nei reel lascia liberi i primi 250 px e gli ultimi 300 px.

## Dove vanno i file

`media/AAAA-MM-GG/` (data di pubblicazione), ramo `media`. Dopo il push ogni file è raggiungibile da
`https://raw.githubusercontent.com/ControlIA89/social-media/media/media/AAAA-MM-GG/<file>`.

## Registro

`media/registro.md`: una riga per contenuto pubblicato (data, formato, tema, titolo, parola chiave dell'invito). Leggilo prima di scegliere i temi, per non ripeterti, e aggiornalo a fine lavoro.

## Analisi delle performance

Ogni domenica un'attività programmata scrive `media/analisi/AAAA-MM-GG.md` e aggiorna `media/analisi/ultima.md`. Prima di scegliere temi, ganci e formati leggi `media/analisi/ultima.md` e applicala. Se contraddice una regola di questo file, vale questo file.

## Audio dei reel

Ogni reel esce con un sottofondo di musica classica e senza voce: il Preludio in do maggiore di Bach (scelta di Emanuele del 17 nov 2026). Il brano è di pubblico dominio e viene suonato da zero dal generatore, quindi non ha diritti di terzi.

```
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 reel.mp4)
python3 generator/reel/musica_classica.py bach $D musica.wav
ffmpeg -y -i reel.mp4 -i musica.wav -filter_complex "[1:a]lowpass=f=7000,highpass=f=40,loudnorm=I=-19:TP=-2[a]" \
  -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 160k -shortest reel_con_musica.mp4
```

Lo stesso script suona anche `satie` e `pachelbel`: usali solo se Emanuele lo chiede. `musica_focus.py` (lo-fi) non si usa più.

Serve il pacchetto Python `soundfile` (`pip install soundfile`). Controlla con ffprobe che il file finale abbia una traccia audio lunga quanto il video. Se la musica non si riesce a generare, pubblica il reel muto e segnalalo nel riepilogo.
