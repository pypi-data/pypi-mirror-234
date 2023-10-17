# Scripts
 Librería de funciones Python para proyectos RPA

# Tutoriales generales de Python
https://www.w3schools.com/python/default.asp



# Ayuda Pandas
Obtener una lista con los valores del índice de un dataframe:
lista_valores = data_frame.index.to_list()
## Vídeos Interesantes:

Introducción al tramitando de datos con pandas 2023: https://www.youtube.com/watch?v=xi0vhXFPegw&t=17s

Acelerando el tratamiento de datos con pandas: https://www.youtube.com/watch?v=SAFmrTnEHLg

Live completo del trabajo con pandas y datos: https://www.youtube.com/watch?v=xs_L6z9QNYY

25 errores trabajando con pandas: https://www.youtube.com/watch?v=_gaAoJBMJ_Q




# Ayuda con los entornos de Python ENV
Unas guías de ejemplos: 

https://docs.python.org/es/3/tutorial/venv.html

https://www.freecodecamp.org/espanol/news/entornos-virtuales-de-python-explicados-con-ejemplos/


Lo esencial en windows:
en la ventana de comandos teclear python -v
En cualquiera de las entradas se ve la carpeta en las que está instalado el python.

Empezando desde cero:
1.- crear un nuevo entorno: 
C:\Users\jgonzal>python -m venv MiEntorno1

2.- activar el nuevo entorno: 
C:\Users\jgonzal>MiEntorno1\Scripts\activate.bat
(MiEntorno1) C:\Users\jgonzal>
3.- ver los paquetes instalados en el nuevo entorno
(MiEntorno1) C:\Users\jgonzal>python -m pip freeze
(MiEntorno1) C:\Users\jgonzal>

4.- añadir openpyxl al nuevo entorno y comprobar que la librería está instalada
(MiEntorno1) C:\Users\jgonzal>python -m pip install openpyxl
...
(MiEntorno1) C:\Users\jgonzal>python -m pip freeze
et-xmlfile==1.1.0
openpyxl==3.0.10

5.- añadir la librería ULL al nuevo entorno y comprobar que está instalada
(MiEntorno1) C:\Users\jgonzal>python -m pip install ULLRPALIB
...
(MiEntorno1) C:\Users\jgonzal>python -m pip freeze
et-xmlfile==1.1.0
numpy==1.24.1
openpyxl==3.0.10
pandas==1.5.2
python-dateutil==2.8.2
pytz==2022.7
six==1.16.0
ULLRPALIB==4.19.2
xlrd==2.0.1

6.- Elegir en visual estudio code el nuevo entorno
- En la parte inferior derecha se hace click sobre la versión de python
- En el menú superior se puede navegar por las carpetas hasta llegar al fichero python.exe de la carpeta del nuevo entorno
- Una vez realizado esto, cuando ejecutamos desde el visual estudio con Ctrl+F5 ya el se sitúa primero en el nuevo entorno
 

7.- Salir del nuevo entorno en la ventana de comandos si fuera necesario
(MiEntorno1) C:\Users\jgonzal>deactivate
C:\Users\jgonzal>
