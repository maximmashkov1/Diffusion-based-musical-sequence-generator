@echo off
set "insert_path\training_data"
set "midiDir=insert_path\training_midi"
set "musescorePath=insert_path\MuseScore 3\bin"

cd "%musescorePath%"

for %%f in ("%gp5Dir%\*.gp5") do (
    MuseScore3.exe "%%f" -o "%midiDir%\%%~nf.mid"
)
