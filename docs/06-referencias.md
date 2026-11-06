# 6. Referencias técnicas y créditos

## Intel y fabricante de la placa

- [Gigabyte Q670M D3H DDR4, soporte BIOS](https://www.gigabyte.com/Motherboard/Q670M-D3H-DDR4-rev-10/support): el portal público consultado enumera rev. 1.0; nuestra PCB llevaba rev. 1.1. Comprobar con el fabricante qué paquete corresponde a la unidad antes de utilizar una imagen.
- [Intel AMT_GeneralSettings](https://software.intel.com/sites/manageability/AMT_Implementation_and_Reference_Guide/HTMLDocuments/WS-Management_Class_Reference/AMT_GeneralSettings.htm): significado de privacidad y configuración de red.
- [Intel IPS_OptInService](https://software.intel.com/sites/manageability/AMT_Implementation_and_Reference_Guide/HTMLDocuments/WS-Management_Class_Reference/IPS_OptInService.htm): consentimiento de usuario.
- [Intel IPS_HostBasedSetupService](https://software.intel.com/sites/manageability/AMT_Implementation_and_Reference_Guide/HTMLDocuments/WS-Management_Class_Reference/IPS_HostBasedSetupService.htm): modo de control y aprovisionamiento.
- [Intel 600 Series PCH, Pin Straps](https://edc.intel.com/content/www/us/en/design/ipla/software-development-platforms/client/platforms/alder-lake-desktop/intel-600-series-chipset-family-platform-controller-hub-pch-datasheet-volume/004/pin-straps/): strap de Flash Descriptor Security Override.
- [Intel: Adding Custom Web Applications](https://software.intel.com/sites/manageability/AMT_Implementation_and_Reference_Guide/WordDocuments/addingcustomwebapplications.htm).
- [Intel: Accessing Custom Web Applications](https://software.intel.com/sites/manageability/AMT_Implementation_and_Reference_Guide/WordDocuments/accessingcustomwebapplications.htm).
- [Intel: arquitectura de AMT](https://software.intel.com/sites/manageability/AMT_Implementation_and_Reference_Guide/WordDocuments/hardwareplatformarchitecture1.htm).

## Proyectos utilizados o consultados

- [MeshCommander, Ylian Saint-Hilaire y colaboradores](https://github.com/Ylianst/MeshCommander).
- [Builds para alojamiento en AMT](https://github.com/Ylianst/MeshCommander/tree/master/output).
- [MeshCommander #99: instalación con firmware reciente](https://github.com/Ylianst/MeshCommander/issues/99). Incluye experiencias de jsastriawan, jontywigster, joshtrichards y otros participantes. Es evidencia de sus equipos, no una especificación universal de Intel.
- [Comentario sobre /amt-storage/index.htm](https://github.com/Ylianst/MeshCommander/issues/99#issuecomment-2091734449).
- [Comentario sobre index.htm sin Vendor/App](https://github.com/Ylianst/MeshCommander/issues/99#issuecomment-2574134892).
- [ME Analyzer, de plutomaniac](https://github.com/platomav/MEAnalyzer): ayuda de análisis, con cobertura limitada para algunas estructuras de CSME 16.
- [FreeBSD: interpretación de registros de estado ME](https://cgit.freebsd.org/src/commit/?id=8e5e2c391059eaa0280a32b951e3ab1fac278364): referencia primaria de código para interpretar estado/mode/error.

Las marcas, herramientas y firmware de terceros conservan sus respectivas licencias. Este repositorio no redistribuye sus ejecutables ni las imágenes SPI del equipo.

## Cómo ampliar el caso

Para una corrección o un nuevo caso, indicar:

1. Placa, revisión de PCB, BIOS y CSME exactos.
2. Síntoma inicial y si CSME estaba sano.
3. Método de lectura y qué regiones se verificaron.
4. Cambios aplicados y comprobación de lectura posterior.
5. Valores de privacidad/opt-in y prueba real de KVM.
6. Versión de la aplicación web y URL relativa utilizada, sin IP privada.

Mantener diferenciados los resultados medidos, los comunicados por el usuario y las hipótesis.
