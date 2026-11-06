# 3. Reconstruir Default con MFIT conservando el código original

Esta es la parte específica del caso que hizo efectivo el cambio de privacidad. Requiere una copia propia válida, identificación exacta de las particiones y herramientas compatibles. Una imagen de otra unidad no conserva necesariamente las claves, configuración y datos de fabricación de la tuya.

## Mapa observado

Todos los intervalos de este documento son semiabiertos: incluyen el inicio y excluyen el final.

| Región | Inicio SPI | Final SPI |
| --- | --- | --- |
| Descriptor | 0x0000000 | 0x0001000 |
| GbE | 0x0001000 | 0x0003000 |
| ME | 0x0003000 | 0x0766000 |
| Región 9 / Device Expansion 2 | 0x0766000 | 0x1000000 |
| BIOS | 0x1000000 | 0x2000000 |

La región 9 devolvía error de lectura antes de FDO. Más adelante se pudo leer por completo. **Una región inaccesible no debe rellenarse con FF suponiendo que está vacía.**

En la región ME de este caso, el área MDAT usada para el candidato quedó acotada al intervalo relativo **0x1ca000..0x34f000**. En direcciones absolutas SPI era **0x1cd000..0x352000**. Es un dato del mapa concreto, no una plantilla para otras versiones.

## Herramienta y fuente de fábrica

Se utilizó Intel Modular Flash Image Tool **16.1.25.2091**, aportado localmente por el propietario. La firma Authenticode del ejecutable Windows se verificó como válida, con firmante Intel Corporation.

Como base de datos de fábrica se estudió la imagen oficial **F32 para la misma placa**. Se comprobó que el código nativo de ME coincidía con el original de nuestra unidad. F34a también se examinó, pero la imagen oficial disponible contenía otra variante de ME y no se usó como sustituto completo.

Las versiones de BIOS y el nombre de la placa no bastan para demostrar que dos regiones ME son intercambiables. Se compararon componentes, versión, SKU, mapa y contenido.

## Por qué un cambio de un byte no bastó

La configuración OEM/FITC era solo una de las representaciones de la política. En los datos MFS inicializados se observaron archivos de política con metadatos de integridad. Cambiar el byte OEM y su CRC no actualizó por sí solo el estado efectivo de AMT.

MFIT también avisó que PrivacyLvl era de solo lectura al reconstruir la imagen ya inicializada. Los builds de control y Default resultaron idénticos. Ese ensayo se descartó.

No se fabricaron HMAC ni se intentó presentar un CRC correcto como autenticación válida de los archivos MFS.

## Procedimiento que sí dio resultado

1. **Descomponer el volcado propio restaurado** con MFIT y guardar su configuración completa y componentes.
2. **Descomponer F32 oficial** y localizar su ME Sub Partition de fábrica, que incluía conjuntamente la base MFS/EFS no inicializada.
3. Preparar una configuración de trabajo que mantuviera los valores y componentes propios y utilizara esa base de datos de fábrica como MeRegionFile.
4. Generar dos imágenes de control desde esa misma base: una Enhanced y otra Default. La única opción funcional cambiada fue:

~~~text
CsePlugin:AmtProvisioningNvars:PrivacyLevel#RedirectionPrivSecLevel
Enhanced -> Default
~~~

5. Comparar ambos builds. Se encontraron cinco bytes distintos: cuatro de CRC y uno de política. En nuestra SPI estaban en 0x34500c..0x345010 y 0x345440. Esto comparaba **los dos builds de fábrica**: no significa que el parche aplicado al estado vivo fuera de cinco bytes.
6. Construir el candidato final conservando el prefijo y sufijo de ME originales y tomando solo **MDAT** de la salida Default. MFIT también había variado doce bytes fuera de MDAT; esos cambios no se conservaron.
7. Volver a descomponer el candidato final. Todos los valores no relacionados con rutas coincidieron con la configuración original salvo Enhanced -> Default; el único componente binario distinto fue la subpartición de datos ME.
8. Comparar el código firmado y el mapa con el original. ME Analyzer se utilizó como comprobación independiente, con sus limitaciones para esta generación.
9. Obtener dos nuevas copias completas idénticas inmediatamente antes de escribir, preparar la lista de sectores diferentes y verificar que todos caían dentro del área permitida.
10. Escribir únicamente los 116 sectores de datos necesarios y releer toda la SPI para comprobar el resultado y que el exterior de ME siguiera idéntico.

La reinicialización de datos implica perder el aprovisionamiento AMT anterior y puede afectar al estado de PTT/TPM. En el caso se había autorizado ese restablecimiento antes de la intervención; no debe suponerse que conserva credenciales ni objetos sellados al TPM. Las claves de recuperación y los datos necesarios deben estar disponibles previamente.

## Uso de la interfaz de MFIT

La ayuda de la versión empleada admite descomposición, carga de configuración, valores y reconstrucción:

~~~powershell
.\mfit.exe --help
.\mfit.exe --decompose .\own-spi.bin --saveconfig .\own-config.xml
~~~

Una vez preparado y revisado un XML con componentes propios y base de datos de fábrica compatible, la forma de reconstrucción es:

~~~powershell
.\mfit.exe --decompose .\own-spi.bin --loadconfig .\prepared-config.xml --setvalues "CsePlugin:AmtProvisioningNvars:PrivacyLevel#RedirectionPrivSecLevel=Default" --build .\review-only.bin --saveconfig .\review-config.xml
~~~

El ejemplo muestra sintaxis de la herramienta; no prepara el XML ni verifica la compatibilidad. **review-only.bin es una salida para revisar, no una instrucción para programar la flash completa.** El candidato aplicado en nuestro caso se ensambló de forma selectiva según el paso 6.

Los XML pueden contener configuración propia del equipo y rutas locales. Este repositorio no proporciona un XML de fabricación genérico ni un flasheador listo para otras unidades.

## Validación estática y arranque

ME Analyzer informó una advertencia sobre una tabla EFS. Se contrastó con la fuente F32 oficial y allí apareció la misma advertencia. Se conservaron firmas de código válidas y se reconoció la limitación del analizador. Ninguna de esas comprobaciones estáticas sustituyó a probar el arranque.

Tras escribir, se retiró FDO sin corriente y se arrancó normalmente. Se accedió a BIOS/MEBx, se configuró contraseña, se activó la red y se deshabilitó opt-in. Entonces se midieron **PrivacyLevel=0 y OptInRequired=0**.

Durante ese primer arranque los datos recién creados pasan a inicializados. Por eso el hash posterior de toda la región ME puede cambiar legítimamente: debe revisarse qué zona cambió, además de comprobar salud y política efectiva.
