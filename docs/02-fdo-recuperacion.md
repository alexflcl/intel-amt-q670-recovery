# 2. FDO físico y recuperación de la copia propia

Este montaje pertenece a la **Gigabyte Q670M D3H DDR4 rev. 1.1 con Realtek ALC897** estudiada. En otra revisión puede cambiar el códec, la ruta de la señal o la alimentación.

## Por qué utilizamos el chip de audio

Intel documenta HDA_SDO como una señal de strap para Flash Descriptor Security Override en esta familia de PCH: importa el nivel de la señal en el momento de muestreo del arranque. El códec de audio nos proporcionó un punto accesible de esa conexión. [Intel 600 Series PCH: Pin Straps](https://edc.intel.com/content/www/us/en/design/ipla/software-development-platforms/client/platforms/alder-lake-desktop/intel-600-series-chipset-family-platform-controller-hub-pch-datasheet-volume/004/pin-straps/).

No se estaba reparando el audio ni usando su memoria como BIOS.

## Montaje utilizado y mediciones

Se identificaron en nuestro ALC897:

| Punto | Uso en el montaje del caso |
| --- | --- |
| Pin 5 | HDA_SDO / señal de override |
| Pin 9 | DVDDIO, medido aproximadamente a 3,43 V |
| Entre ambos | Resistencia de 2 kΩ y dos hilos finos |

~~~text
ALC897: pin 9, DVDDIO ---- resistencia 2 kΩ ---- pin 5, HDA_SDO
~~~

La resistencia no tiene polaridad. La numeración debe comprobarse desde la marca de pin 1 del encapsulado y su documentación; la orientación de una fotografía girada no es una referencia suficiente. La medida de 3,43 V es la obtenida en esta placa, no un valor que deba aplicarse desde una fuente externa.

Para preparar o abrir la conexión se apagó el equipo, se desconectó la fuente de la red y se esperó a que desapareciera la alimentación residual. Se aislaron las uniones. La conexión se mantuvo durante el arranque de recuperación y se abrió sin corriente antes del arranque normal.

El osciloscopio se usó como instrumento de medida; su salida GEN no alimentó el circuito. Una lectura previa de unos 5,12 V correspondía a la alimentación USB y no se utilizó para polarizar HDA_SDO. Con un osciloscopio de banco, su pinza de masa debe ir a una masa identificada de la placa; no debe conectarse a un pin arbitrario.

## Comprobar que FDO está realmente activo

En este equipo se observaron:

| Indicador | Arranque con FDO | Arranque normal final |
| --- | --- | --- |
| FDOPSS | 0 | 1 |
| FRACC | 0xffff | 0x4acf |
| CSME | Modo 4, override; sin inicialización normal | Modo 0, Normal |
| MEI/HECI | No disponible en el arranque de mantenimiento observado | Disponible |

Estos son valores del controlador y de la plataforma del caso, no direcciones universales ni instrucciones para modificar registros. Se verificaron permisos y estado antes de intentar escribir.

**No se evaluó el resultado final de AMT con la resistencia conectada.** Primero se terminó la escritura y se guardaron las copias; después se abrió FDO y se comprobó un arranque normal.

## Copias y recuperación

1. Se leyeron **dos veces los 32 MiB completos** de la SPI con FDO activo. Ambas lecturas fueron idénticas.
2. Se compararon descriptor, GbE, BIOS y la región adicional con las copias anteriores.
3. Se restauró la región ME de la **copia propia anterior al daño**.
4. El escritor original comprobó cada sector y contemplaba restauración de su preimagen si fallaba la operación.
5. Se releyó toda la flash y se verificó que solo había cambiado la zona prevista.
6. Se guardaron resultados y copias en el USB y en otro ordenador antes del apagado.

La restauración de la copia propia escribió 106 sectores de 4 KiB. Recuperó la base funcional; el cambio de privacidad se hizo después y escribió 116 sectores distintos respecto a su fuente. Estos recuentos documentan dos intervenciones separadas.

En el primer estado averiado no aparecía el NVMe. Después de restaurar ME volvió a detectarse. Por tanto, la ausencia del disco no justificaba formatearlo ni reinstalar Proxmox.

## Cómo se salió de FDO

Se apagó ordenadamente y se desconectó la fuente. El usuario abrió la conexión cortando un tramo libre de uno de los hilos, lejos de las patas del códec, y aisló ambos extremos. Esto permitió dejar los puntos soldados disponibles para una recuperación futura sin mantener el override activo.

El arranque normal final mostró HFSTS1=0x90000245, estado de trabajo 5, modo 0, inicialización completa y error 0. Volvieron MEI, NVMe y el funcionamiento normal de Proxmox.

## Lo que no fue necesario

No se desoldó el chip M_BIOS. En esta placa se identificó un **Macronix MX25L25673GZ4I-08G, WSON de ocho contactos, 32 MiB y 3,3 V**: sus contactos inferiores no se agarran como las patas expuestas de un SOIC8.

La huella vacía EC_BIOS no se trató como un conector de programación. Una huella sin componente necesita esquema o comprobaciones eléctricas para determinar su función.
