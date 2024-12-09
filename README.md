Instrucciones de compilación:

Una vez clonado el proyecto, nos dirigimos a la carpeta `Pagina Web - Backend` y, en caso de no tener las dependencias instaladas, usamos los siguientes comandos en la terminal específica de la carpeta:

- `pip install transformers`
- `pip install flask`
- `pip install flask-cors`
- `pip install requests`
- `pip install beautifulSoup4`
- `pip install torch`
- `pip install tf-keras`

Una vez hecho esto, buscamos en la parte superior derecha del IDE Visual Studio Code el símbolo ▶︎ y esperamos hasta que se muestre en la terminal:

* Debugger is active!
* Debugger PIN: 152-883-327

Con esto terminamos el apartado del servidor. Para visualizar la página web, nos dirigimos a la carpeta `Pagina Web - Client`, abrimos su terminal integrada y ejecutamos el comando:

- `npm run dev`

En caso de que este falle, realizar en esta misma terminal:

- `npm install`

Cabe recalcar que para esto es necesario tener instalado Node.js en su laptop. Una vez hecho esto, en la terminal debería verse:

- `VITE v6.0.1  ready in 328 ms`

 - ` ➜  Local:   http://localhost:5173/`
 - ` ➜  Network: use --host to expose`
 - `➜  press h + enter to show help`

Manteniendo shift y dando click en el  `http://localhost:5173/` debera redireccionarlo a la pagina web
