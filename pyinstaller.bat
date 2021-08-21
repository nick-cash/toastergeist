REM Edit paths before running:
C:\python27\python "E:\Program Files\pyinstaller-2.0\pyinstaller.py" -w -F -i images\icon.ico main.py button.py creditsmenu.py game.py level.py mainmenu.py menu.py pausemenu.py sprite.py ldpygame\__init__.py ldpygame\asset_manager.py ldpygame\clock.py ldpygame\event_responder.py ldpygame\game.py ldpygame\screen.py ldpygame\sprite.py ldpygame\sprite_events.py ldpygame\timer.py

pause
REM If packaged as single file.
xcopy /s /I fonts dist\fonts
xcopy /s /I images dist\images
xcopy /s /I sounds dist\sounds
REM xcopy /s /I fonts dist\main\fonts If packaged as directory
REM xcopy /s /I graphics dist\main\images
REM xcopy /s /I sounds dist\main\sounds
pause
