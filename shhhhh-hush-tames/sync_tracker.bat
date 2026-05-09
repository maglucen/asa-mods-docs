@echo off
cd /d A:\Mods\asa-mods-docs\shhhhh-hush-tames
python sync_tracker_from_notion.py
if errorlevel 1 (
  echo.
  echo Sync failed.
  pause
  exit /b 1
)
echo.
echo Tracker and progress bar synced successfully.
pause
