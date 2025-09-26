#!/bin/bash
cd "C:/Users/Admin/OneDrive/Desktop/py/SQLAlchemyDatabase/Goongram" || exit

FILE="app.py"

# Append a timestamp comment (always unique change)
echo "# Auto commit: $(date '+%Y-%m-%d %H:%M:%S')" >> "$FILE"

# Git commit and push
git add "$FILE"
git commit -m "Recent Changes"
git push origin master   # <-- change to main if that's your branch
