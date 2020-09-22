@echo Off
   set PLUGIN_PATH=%USERPROFILE%\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins
   set PLUGIN=LuniPlugin
   rem Create the plugin folder if it does not exist 
   if not exist "%PLUGIN_PATH%\%PLUGIN%" mkdir "%PLUGIN_PATH%\%PLUGIN%"
   rem copy all contents to destination - /mir means -overwrite destination
   robocopy "%~dp0\%PLUGIN%"  "%PLUGIN_PATH%\%PLUGIN%" /mir /is /it 