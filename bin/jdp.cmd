@echo off

set PYTHON=%~dp0\..\pgm\jdp-cli\python.exe

%PYTHON% -m jdp_cli %*
