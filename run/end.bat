@echo off

echo Encerrando servidor Django...
taskkill /F /IM "python.exe"

echo Encerrando servidor React...
taskkill /F /IM "node.exe"

echo Encerrando servidor Nginx...
taskkill /F /IM "nginx.exe"
