#!/bin/bash
export DOTNET_SYSTEM_GLOBALIZATION_INVARIANT=1
cd ~/ripper-bot
poetry run python main/main.py