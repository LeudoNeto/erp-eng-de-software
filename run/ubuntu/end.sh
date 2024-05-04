#!/bin/bash

echo "Encerrando servidor Django..."
pkill -f "python manage.py runserver 2030"

echo "Encerrando servidor React..."
pkill -f "npm start"

echo "Encerrando servidor Nginx..."
pkill -f "nginx -c ./nginx/nginx.conf"
