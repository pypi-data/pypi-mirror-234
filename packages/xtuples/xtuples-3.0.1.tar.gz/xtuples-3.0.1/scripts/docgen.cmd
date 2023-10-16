del /f /s /q docs 1>nul
rmdir /s /q mydir
mkdir docs
python -m pdoc src/xtuples -o ./docs --html --force
move docs\xtuples\* docs\
rmdir docs\xtuples