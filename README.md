# Verificación-de-brechas-para-algun-correo
Ejercicio hecho en vscode para identificar brechas en correo electronicos 
Primero se creó una carpeta donde estará un archivo .txt y este script de python. En el archivo .txt se guardar el apikey proporcionado.
Se ejecutará el script en la terminal desde el modo administrador como: python verificar_correo.py correo@example.com(este se cambiaria por el correo que se desee verificar).
Si no le deja ejecutarlo, verifique que tenga instalado la libreria request.
Al ejecutarlo, se analizará el correo y mostrara cuantás brechas y de dónde son, tomando 10 segundos de espera por cada brecha mostrada.
