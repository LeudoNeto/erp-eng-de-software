#!/bin/bash

echo "Iniciando servidor Django..."
python3 manage.py runserver 2030 &

echo "Iniciando servidor React..."
cd ./jsketcher/ && npm start &

echo "Aguardando servidor React iniciar..."
sleep 15

echo "Compilando arquivo do React..."
curl http://localhost:3000/desenho_do_projeto/

echo "Iniciando servidor Nginx..."
nginx -c ./nginx/nginx.conf &
