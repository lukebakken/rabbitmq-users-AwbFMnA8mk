echo on
setlocal
set RABBITMQ_BASE=%~dp0\rabbitmq
set RABBITMQ_CONFIG_FILE=%~dp0\rabbitmq.conf
%~dp0\rabbitmq_server-3.11.9\sbin\rabbitmq-server.bat
