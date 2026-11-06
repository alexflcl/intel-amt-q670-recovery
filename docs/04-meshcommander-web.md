# 4. MeshCommander dentro de AMT 16.1: KVM desde la IP del equipo

Si AMT ya funciona, esta parte se puede hacer por separado de FDO y de la reconstrucción de privacidad.

En nuestro caso, el propietario confirmó que **Small funciona** y después que **Medium funciona bien**. Son aplicaciones alojadas en el servidor web de AMT, accesibles aunque Proxmox no esté funcionando, siempre que AMT conserve alimentación y conectividad. No se necesita mantener MeshCentral en otra máquina.

## Descargas

Utiliza MeshCommander normal, con su sección Web Applications. El Firmware Loader antiguo puede fallar en AMT 16.1; un fallo del loader no demuestra que Web Application Hosting esté inutilizado en tu versión.

| Archivo | Tamaño mostrado por GitHub | Resultado en nuestra unidad |
| --- | --- | --- |
| [Firmware-Small.gz](https://raw.githubusercontent.com/Ylianst/MeshCommander/master/output/Firmware-Small.gz) | 39,5 KB | Funcionó |
| [Firmware-Medium.gz](https://raw.githubusercontent.com/Ylianst/MeshCommander/master/output/Firmware-Medium.gz) | 59,8 KB | Funcionó |
| [Firmware-Large.gz](https://raw.githubusercontent.com/Ylianst/MeshCommander/master/output/Firmware-Large.gz) | 70,8 KB | No probado |

[Carpeta oficial de builds](https://github.com/Ylianst/MeshCommander/tree/master/output) y [proyecto MeshCommander](https://github.com/Ylianst/MeshCommander). Los archivos enlazados a master pueden cambiar; guarda localmente el archivo que te funcione y su SHA-256.

No se comprobó una matriz completa de funciones de Small frente a Medium ni se midió una mejora de rendimiento de KVM.

## Instalar una aplicación con enlace

1. Descarga Small para la primera prueba. Si funciona, puedes repetir con Medium.
2. Renombra la copia comprimida a **fwm.htm.gz**, sin descomprimirla. Muestra las extensiones en el Explorador para evitar un nombre terminado en .gz.gz.
3. Abre MeshCommander normal en un ordenador de la red y conecta a la IP actual de AMT con tu cuenta de administración. Para TLS se utiliza el puerto 16993.
4. Abre **Web Applications**, selecciona fwm.htm.gz y comprueba que el nombre de destino queda como fwm.htm y el tipo como text/html. El cargador maneja el sufijo .gz; no subas el HTML descomprimido como sustitución automática de este procedimiento.
5. En el procedimiento empleado se dejaron Vendor y Application vacíos y se añadió un nombre de enlace, por ejemplo MeshCommander. Si se elige una carpeta propia, anota la ruta resultante.
6. Sube el archivo y abre la página AMT en el navegador:

~~~text
https://<IP-AMT>:16993/
~~~

7. En **Web Applications Links**, abre MeshCommander y comprueba una sesión KVM.

La IP de Proxmox y la IP configurada en AMT pueden ser distintas. Tras restablecer datos ME, AMT puede perder una configuración estática anterior y volver a DHCP.

La [incidencia #99 del proyecto](https://github.com/Ylianst/MeshCommander/issues/99) documenta este enfoque en 16.1.30, los problemas de nombres/MIME y que algunas versiones posteriores deshabilitan WebUI. No todas las variantes 16.1 se comportan igual.

## Hacer que MeshCommander sea la página inicial

Este paso se indicó al propietario después de probar Medium. Se ha observado una pestaña con MeshCommander en /amt-storage/index.htm; la apertura automática al visitar solo / no quedó confirmada explícitamente en el relato.

1. Conserva el enlace funcional anterior como respaldo y su archivo .gz local.
2. Copia el paquete Medium que ya funcionó y renombra la copia a **index.htm.gz**.
3. En Web Applications, deja **Vendor, Application y Link vacíos**.
4. Selecciona la copia comprimida y verifica que el destino se llama **index.htm**, con tipo text/html. No elimines la compresión.
5. Sube el archivo. La ubicación especial es la raíz del almacenamiento de aplicaciones, **/amt-storage/index.htm**. No se trata de crear otra aplicación dentro de /amt-storage/vendor/app/.
6. Prueba por separado estas dos direcciones, con recarga forzada o en una sesión nueva:

~~~text
https://<IP-AMT>:16993/amt-storage/index.htm
https://<IP-AMT>:16993/
~~~

La primera comprueba el archivo alojado; la segunda comprueba que el firmware lo utiliza como página de entrada. Si solo funciona la primera, conserva esa URL y registra el comportamiento de tu versión.

La sustitución de index sin Vendor/App está descrita en [este comentario del proyecto](https://github.com/Ylianst/MeshCommander/issues/99#issuecomment-2574134892). Vaciar Link evita añadir un enlace visible innecesario; la ubicación y el nombre son lo que determina la sustitución.

Para volver atrás, utiliza el cliente MeshCommander externo y elimina únicamente el index.htm añadido desde la gestión de aplicaciones, si la interfaz permite esa operación. Una orden para vaciar todo el almacenamiento también elimina las aplicaciones de respaldo, por lo que no equivale a retirar solo index.

## Tamaño total y límite de carga

Intel documenta hasta **200 KB compartidos** para estas aplicaciones/datos y el uso de transferencia HTTP fragmentada. No es lo mismo que el tamaño aceptado por una operación concreta del cliente. [Intel: Adding Custom Web Applications](https://software.intel.com/sites/manageability/AMT_Implementation_and_Reference_Guide/WordDocuments/addingcustomwebapplications.htm).

En la incidencia #99 se reportó una frontera práctica de 65.535 bytes en una ruta de carga de AMT 16.1. Medium está por debajo; Large la supera. No medimos ese límite en nuestra unidad ni probamos Large. Si falla una carga mayor, revisa tamaño, espacio ocupado, ruta, MIME y soporte del cliente antes de atribuirlo únicamente a falta de almacenamiento total.

## Errores que conviene distinguir

| Síntoma | Qué revisar |
| --- | --- |
| El navegador descarga console u otro archivo | Nombre, extensión y tipo MIME; utiliza el paquete comprimido con nombre .htm.gz |
| Loader falla, pero MeshCommander conecta | Prueba la carga manual en Web Applications |
| HTTP 500 al subir | Revisa compresión, tamaño y almacenamiento; no es un diagnóstico único |
| Web browser access disabled / page unavailable | Puede ser WebUI deshabilitado o una ruta incorrecta; contrasta la versión y la URL exacta |
| El archivo abre pero KVM falla | Comprueba KVM, consentimiento, gráficos y autenticación independientemente del alojamiento HTML |
| AmtLoadWebApp no existe | Versiones modernas de MeshCMD retiraron esa acción; no presupongas que una guía antigua describe tu ejecutable |

La descarga y carga de la aplicación web no sustituye una actualización de seguridad de CSME. No es necesario degradar firmware como parte de este procedimiento. Mantén la interfaz de administración dentro de una red de gestión o acceso privado controlado.
