@echo off

echo Iniciando servidor Django...
start /B cmd /c "python manage.py runserver 2030"

echo Iniciando servidor React...
start /B cmd /c "cd .\jsketcher\ && npm start"

echo Iniciando servidor Nginx...
start /B cmd /c "nginx -c .\nginx\nginx.conf"
