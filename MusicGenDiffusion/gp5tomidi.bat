@echo off
set "gp5Dir=C:\Users\Maxim\Desktop\MusicGenDiffusion V3\training_data"
set "midiDir=C:\Users\Maxim\Desktop\MusicGenDiffusion V3\training_midi"
set "musescorePath=C:\Program Files\MuseScore 3\bin"

cd "%musescorePath%"

for %%f in ("%gp5Dir%\*.gp5") do (
    MuseScore3.exe "%%f" -o "%midiDir%\%%~nf.mid"
)
for %%f in ("%gp5Dir%\*.gp4") do (
    MuseScore3.exe "%%f" -o "%midiDir%\%%~nf.mid"
)
for %%f in ("%gp5Dir%\*.gp3") do (
    MuseScore3.exe "%%f" -o "%midiDir%\%%~nf.mid"
)
for %%f in ("%gp5Dir%\*.gp2") do (
    MuseScore3.exe "%%f" -o "%midiDir%\%%~nf.mid"
)
for %%f in ("%gp5Dir%\*.gpx") do (
    MuseScore3.exe "%%f" -o "%midiDir%\%%~nf.mid"
)