# Comparación offline de imágenes

Requiere Python 3. No instala paquetes y no abre dispositivos físicos. Solo acepta archivos completos de 32 MiB con firma de descriptor y regiones correspondientes al caso publicado.

~~~sh
python tools/check_q670_images.py before.bin candidate.bin
~~~

Salida JSON por stdout:

- Hashes de los dos archivos y si son idénticos.
- Número de bytes y sectores de 4 KiB diferentes.
- Direcciones SPI de los sectores afectados.
- Igualdad de todo lo situado fuera de ME.
- Igualdad de todo lo situado fuera del intervalo MDAT documentado.

Código de salida:

| Código | Significado |
| --- | --- |
| 0 | No se observaron cambios fuera de MDAT; incluye imágenes idénticas |
| 1 | Hay cambios fuera de MDAT |
| 2 | Entrada rechazada o fallo de lectura |

**Un 0 solo comprueba la ubicación de diferencias.** No comprueba autenticación MFS/EFS, firmas Intel, CPU/PCH, política de fabricación, compatibilidad de una fuente de fábrica ni arranque. Los datos dentro de MDAT pueden ser incorrectos aunque todo lo demás sea idéntico.

Para comprobar dos lecturas de respaldo, revisa además identical=true. Dos lecturas idénticas pueden seguir siendo incompletas o reflejar un estado averiado; también hacen falta un método de adquisición válido y una copia anterior conocida.

El programa no guarda el informe. Si lo compartes, revisa sus datos y la procedencia de las imágenes. No subas los archivos before.bin y candidate.bin a GitHub.

En la preparación de esta publicación se ejecutó contra la copia restaurada y el candidato archivados del caso: detectó 382.236 bytes distintos en 116 sectores, todos dentro de MDAT, con todo el exterior de ME idéntico. También se comprobó que detectaba un cambio adicional de un bit en BIOS como diferencia fuera del área permitida.
