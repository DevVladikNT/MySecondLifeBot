#!/bin/bash
bot_folder=$(basename "$PWD")
parent_folder=$(cd ../ && pwd)

echo "Stop bot..."
pm2 stop msl_bot.py

echo "Saving database..."
mv db.sqlite ../MSLB_tools

echo "Removing bot dir..."
cd ..
rm -rf $bot_folder

echo "Downloading bot update..."
git clone git@github.com:DevVladikNT/MySecondLifeBot

echo "Restore database..."
mv ./MSLB_tools/db.sqlite ./MySecondLifeBot

./MySecondLifeBot/start.sh
