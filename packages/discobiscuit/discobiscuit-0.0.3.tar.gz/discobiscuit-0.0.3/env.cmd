:: Create virtual env if it does not exist and install dependencies.
@echo off
if not exist ".venv" (
   @echo Creating virtual environment...
    py -m venv .venv
)

(
@echo Installing dependencies...
activate
py -m pip install --upgrade pip
py -m pip install -r requirements.txt
)