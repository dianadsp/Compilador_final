# Para correr:
```
python3 -m pip install matplotlib
python3 -m pip install rply
python3 -m pip install tk

python3 Compilador.py
```

# Codigos Ejemplo:
```
#Esto es un comentario

FLOAT max_count = 10.0;
INTEGER max_tabla = 200;
STRING str_p = "Hola Mundo";
LIST l_tabla = [100,"Adios",max_tabla,3.14];

PRINT ([max_count,max_tabla,str_p]);
PRINT (l_tabla);

max_count = max_count+1;
PRINT (max_count);
max_count = max_count+1;
PRINT (max_count);
max_count = max_count+1;
PRINT (max_count);
```

# Descomentar Linea por linea para probar errores
```
#descomentar linea por linea para probar errores sintacticos
#?
#/   

FLOAT max_count = 10.0;
INTEGER max_tabla = 200;
STRING str_p = "Hola Mundo";
LIST l_tabla = [100,"Adios",max_tabla,3.14];

#descomentar linea por linea para probar errores semanticos

#INTEGER var = "Hola";
#PRINT (var);
#PRINT (str_p * 8);
```
