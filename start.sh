#!/bin/bash
echo "Start bot..."
cat ../MSLB_tools/token.txt > pm2 start msl_bot.py --interpreter=python3
echo "Done!"
