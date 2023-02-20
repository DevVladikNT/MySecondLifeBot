#!/bin/bash
echo "Start bot..."
pm2 start ./MySecondLifeBot/msl_bot.py --interpreter=python3
echo "Done!"
