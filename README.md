# Intel AMT en Gigabyte Q670: cambiar PrivacyLevel, habilitar KVM sin PIN y recuperar ME

[English overview](README.en.md)

Caso real documentado el **6 de noviembre de 2026**: una **Gigabyte Q670M D3H DDR4, revisión 1.1, BIOS F34a**, con **CSME Corporate H 16.1.30.2255**.

El objetivo era utilizar KVM sin introducir un código de consentimiento en la pantalla local. La política **Enhanced** impedía desactivar esa exigencia. Durante la investigación, una modificación incompleta de los datos de ME dejó el subsistema sin inicializar y desaparecieron dispositivos, entre ellos el NVMe. Recuperamos el estado funcional y reconstruimos la configuración **Default**. Después alojamos MeshCommander dentro de AMT para abrir KVM desde un navegador, usando la propia IP de AMT.

**Puedes seguir el recorrido de cambio de PrivacyLevel partiendo de una placa que funciona.** La avería forma parte de la historia de este caso y permite explicar cómo recuperarnos; no es un paso necesario para cambiar la política.

➡ **[Recorrido principal: Enhanced → Default desde una placa sana](docs/00-cambiar-privacy-level.md)**  
➡ **[Puente FDO en ALC897: foto, identificación, secuencia y efectos](docs/02-fdo-recuperacion.md)**

## Resultado y alcance

| Comprobación | Resultado |
| --- | --- |
| Proxmox, NVMe y red integrada | Recuperados |
| CSME después de retirar FDO | Estado Normal, inicialización completa, error 0 |
| PrivacyLevel efectivo | 0, Default |
| OptInRequired efectivo | 0 |
| AMTNetworkEnabled | 1 |
| MeshCommander Small y Medium alojados en AMT | Funcionamiento confirmado por el propietario |
| Sustituir la página inicial por index.htm | Procedimiento incluido; navegación automática desde / pendiente de confirmación explícita |

Los valores técnicos finales se resumen en [la ficha de evidencias](evidence/case-study.json). Se distingue entre mediciones del sistema, comprobaciones de imágenes y resultados comunicados por el propietario.

**Este caso no demuestra un método universal para todas las Q670 ni para todas las versiones 16.1.** Las direcciones de memoria, el mapa de flash y el montaje físico corresponden a la unidad estudiada.

## Por dónde empezar

1. **AMT ya funciona y solo quieres KVM desde su IP:** ve directamente a [MeshCommander en el almacenamiento web](docs/04-meshcommander-web.md). No necesitas modificar la política de privacidad ni reconstruir ME si tus opciones de consentimiento ya son suficientes.
2. **AMT funciona, pero no permite quitar el PIN:** sigue el [recorrido de cambio de PrivacyLevel](docs/00-cambiar-privacy-level.md), que empieza por confirmar la causa.
3. **ME no se inicializa o han desaparecido dispositivos tras modificarlo:** lee [FDO y recuperación](docs/02-fdo-recuperacion.md).
4. **Necesitas entender cómo cambiamos Enhanced a Default:** consulta [la reconstrucción con MFIT](docs/03-mfit-default.md) y [los intentos que no resolvieron el problema](docs/05-cronologia.md).

La utilidad [check_q670_images.py](tools/check_q670_images.py) compara imágenes offline y comprueba qué zonas cambian. No escribe firmware y no certifica que una imagen pueda arrancar.

## Qué hizo posible la recuperación

- Tener una copia propia de ME anterior a los ensayos y obtener después dos lecturas completas idénticas de la SPI.
- Activar temporalmente Flash Descriptor Override mediante una señal de arranque accesible en el códec de audio.
- Restaurar primero la copia propia, preservando las otras regiones.
- Reconstruir conjuntamente los datos de fábrica MFS/EFS con MFIT 16.1 y la configuración de nuestra unidad.
- Conservar el código firmado original y limitar la escritura final a los sectores de datos necesarios.
- Verificar toda la flash después de escribir y comprobar CSME/AMT tras un arranque normal sin FDO.

## Material y herramientas

En el caso se utilizaron Linux live con SSH, un segundo ordenador Windows, Intel Modular Flash Image Tool 16.1.25.2091, ME Analyzer como análisis complementario, soldador, hilo fino y una resistencia de 2 kΩ. La alimentación se midió con un osciloscopio FNIRSI 1014D; un multímetro es más sencillo para esa medición de continua. No fue necesario desoldar la flash ni utilizar un programador externo.

Las herramientas de Intel y los firmwares deben obtenerse de una fuente autorizada. Este repositorio contiene documentación original y un comparador offline; las descargas de terceros se enlazan a sus proyectos. Los volcados de una placa pueden contener claves, aprovisionamiento e identificadores propios: utiliza tus copias y mantenlas fuera de repositorios públicos.

## Fuentes y aportaciones

[Referencias técnicas y créditos](docs/06-referencias.md). Si aportas un caso, indica modelo, revisión, BIOS, versión/SKU de CSME, síntoma y cómo verificaste el resultado. Comparte registros depurados, sin credenciales, MAC, UUID ni imágenes completas de la flash.

Documentación preparada por **alexflcl**, con asistencia de Codex, a partir del diagnóstico y la recuperación de su propio equipo. Licencia [MIT](LICENSE) para el contenido original de este repositorio.
