set hostspath=%windir%\System32\drivers\etc\hosts

echo 127.0.0.1 bioprint >> %hostspath%

C:\Python27\python.exe %~dp0../bioprint/setup.py install