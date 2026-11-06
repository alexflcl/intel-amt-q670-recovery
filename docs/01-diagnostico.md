# 1. Diagnóstico: distinguir privacidad, activación y avería de ME

Español · [English](en/01-diagnostics.md)

## El síntoma inicial

AMT estaba disponible, pero la política Enhanced obligaba al consentimiento local para KVM. Desactivar una casilla del cliente de gestión no eliminaba una restricción impuesta por la plataforma.

La propiedad de ejecución AMT_GeneralSettings.PrivacyLevel utiliza Default=0, Enhanced=1 y Extreme=2. En Enhanced no se permite desactivar opt-in. Debe consultarse la política efectiva, además de la configuración de fabricación que aparezca en el volcado. [Referencia de Intel](https://software.intel.com/sites/manageability/AMT_Implementation_and_Reference_Guide/HTMLDocuments/WS-Management_Class_Reference/AMT_GeneralSettings.htm).

Hay una diferencia de codificación relevante en este caso: el byte de configuración OEM/FITC observado utilizaba 01 para Default y 02 para Enhanced, mientras que WS-Man devolvía 0 y 1 respectivamente. No debe copiarse un número entre ambas representaciones.

## Qué registrar antes de tocar firmware

- Modelo exacto de placa, revisión de PCB, versión de BIOS y versión/SKU de ME.
- Si MEBx abre y si permite configurar contraseña, red y consentimiento.
- Qué puertos de AMT responden y si la red está activada.
- Qué dice PrivacyLevel y si IPS_OptInService permite modificar OptInRequired.
- Estado de CSME, presencia de MEI/HECI, NVMe y red.
- Método de lectura de la SPI y regiones realmente accesibles.

En Linux pueden recogerse las identidades y dispositivos con herramientas de consulta:

~~~sh
sudo dmidecode -t baseboard -t bios
lspci -nn
lsblk -o NAME,SIZE,TYPE,MODEL
ls /dev/mei*
~~~

Estos comandos no comprueban por sí solos las protecciones de la flash ni la política AMT. Revisa sus salidas antes de publicarlas: pueden contener datos del equipo.

## No confundir tres estados distintos

| Estado | Qué observamos o cómo se comprueba |
| --- | --- |
| AMT sin aprovisionar | Puede pedir reactivación en MEBx, contraseña y activación de red |
| AMT operativo con privacidad Enhanced | CSME puede estar sano, pero la política impide quitar el PIN |
| CSME sin inicializar o en un modo de mantenimiento | Pueden faltar MEI y otros dispositivos; no equivale a un fallo del cliente KVM |

En nuestra recuperación, cargar valores predeterminados de BIOS, retirar la pila CMOS y un reinicio normal no resolvieron los datos internos de ME. Un borrado CMOS no debe darse por equivalente a restaurar MFS/EFS.

## Los errores que detuvieron el USB de recuperación

Se observaron, en versiones del script del caso:

~~~text
AssertionError
assert event['sector_count'] == 1 and not event['mtd_writeable_after_cleanup']
~~~

y:

~~~text
AssertionError: ME write override was not granted after request
~~~

Eran condiciones de parada de los scripts: indicaban que el estado esperado o los permisos no coincidían. El número de línea depende de la versión del script. El texto no demuestra que el hardware haya concedido escritura ME. No se solucionó eliminando las comprobaciones ni repitiendo escrituras a ciegas.

Se conservó el USB con los resultados, se leyó el estado real de la flash y se pasó a un método físico de override comprobable.

## Medición de privacidad y verificación final

Con CSME sano se consultaron las clases mediante WS-Man. Como herramienta de diagnóstico se usó temporalmente una pasarela LMS limitada a loopback y acceso local autorizado; esto facilitó la lectura cuando la conectividad AMT externa aún no estaba lista.

Valores finales observados:

~~~text
AMT_GeneralSettings.PrivacyLevel = 0
AMT_GeneralSettings.AMTNetworkEnabled = 1
IPS_OptInService.CanModifyOptInPolicy = 1
IPS_OptInService.OptInRequired = 0
IPS_OptInService.OptInState = 0
~~~

ProvisioningMode, ProvisioningState y CurrentControlMode son propiedades distintas. **ProvisioningMode=1 no se utiliza aquí como prueba de Admin Control Mode.** Para acreditar ACM mediante software hay que consultar el modo de control correspondiente, por ejemplo IPS_HostBasedSetupService.CurrentControlMode.

Una propiedad que permite KVM tampoco prueba que una sesión real funcione. Después de las lecturas, el propietario comprobó el acceso operativo y el funcionamiento de MeshCommander Small y Medium desde el navegador.
