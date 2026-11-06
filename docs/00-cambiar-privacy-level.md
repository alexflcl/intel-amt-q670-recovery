# 0. Enhanced → Default partiendo de una placa que funciona

Español · [English](en/00-change-privacy-level.md)

Este recorrido aborda el objetivo original: **cambiar la política de privacidad para poder configurar KVM sin consentimiento local obligatorio**. Se organiza a partir de las etapas que terminaron funcionando en la unidad documentada, omitiendo los ensayos que fallaron.

La secuencia completa, aplicada desde el principio sobre una segunda placa sana, **no se ha probado como un caso independiente**. En nuestra unidad el cambio final se ejecutó después de restaurar su estado funcional. Esta reorganización es una guía de preparación y ejecución basada en ese resultado.

## 1. Comprobar que PrivacyLevel es realmente la causa

Consulta la política efectiva con el cliente de administración o WS-Man.

| Resultado | Siguiente paso |
| --- | --- |
| PrivacyLevel=0, Default | Revisa modo de control y opciones de consentimiento; este cambio de firmware no es necesario |
| PrivacyLevel=1, Enhanced, y no permite desactivar opt-in | Es el escenario de este recorrido |
| ME no inicializa o faltan dispositivos tras una modificación | Comienza por la recuperación de la copia propia |
| No se sabe si la placa implementa AMT | Comprueba primero hardware, firmware y capacidades |

Default permite configurar la política de consentimiento; por sí solo no garantiza que un equipo en cualquier modo de control acepte KVM sin PIN. El modo de control y la configuración de opt-in deben comprobarse también.

## 2. Preparar lo necesario antes de desmontar

- Verifica placa, revisión, códec, BIOS y versión/SKU de CSME. El montaje documentado es Q670M D3H DDR4 rev. 1.1, ALC897 y Corporate H 16.1.30.2255.
- Conserva la configuración de red y acceso AMT que necesitarás restablecer.
- Guarda las claves de recuperación y el material necesario para cualquier dato protegido por PTT/TPM: el procedimiento reinicializa datos de ME.
- Prepara MFIT compatible y una base de fábrica cuya compatibilidad se pueda demostrar. En nuestro caso fue F32 oficial con código ME coincidente.
- Prepara un Linux live y una vía de acceso de mantenimiento. Una NIC USB o PCIe fue útil para acceder al Linux; no sustituye la interfaz de red AMT.
- Guarda las lecturas posibles del estado funcional antes de modificar nada. Si alguna región está bloqueada, registra esa limitación; no inventes su contenido.
- Ten preparados soldador, hilo fino, resistencia de 2 kΩ y equipo de medida. Lee primero el [montaje FDO completo](02-fdo-recuperacion.md).

La estrategia de reversión es volver a tu estado funcional anterior, aunque ese estado siga siendo Enhanced.

## 3. Instalar el montaje FDO sin alimentación

1. Apaga ordenadamente el sistema.
2. Desconecta físicamente la fuente de la corriente y espera a que desaparezca la alimentación residual.
3. Identifica pin 1 y cuenta los pines del ALC897. Confirma la señal y la alimentación correspondientes a tu revisión.
4. En el montaje de nuestra unidad, conecta **pin 9 → resistencia 2 kΩ → pin 5**, usando hilos aislados. Deja una unión accesible para abrirla sin volver a trabajar junto al códec.
5. Comprueba que las soldaduras no unan patas vecinas y que los extremos no toquen otros componentes.

**El puente no cambia PrivacyLevel.** Solo prepara un arranque con acceso de mantenimiento a la flash; para cambiar la política es necesario generar y escribir los datos correspondientes.

## 4. Arrancar el entorno de mantenimiento y comprobar permisos

Arranca el Linux live con el montaje conectado. En nuestro caso, FDO activo produjo FDOPSS=0 y FRACC=0xffff. Los detalles están en el [capítulo del puente](02-fdo-recuperacion.md#comprobar-que-fdo-está-realmente-activo).

CSME puede estar en modo de mantenimiento y MEI/AMT pueden no estar disponibles en ese arranque. No uses una sesión KVM fallida en este estado para evaluar el cambio de privacidad.

Obtén **dos lecturas completas de 32 MiB idénticas**, guárdalas fuera del equipo y confirma el mapa. Estas lecturas son la fuente exacta para preparar y verificar la intervención y para volver atrás.

## 5. Preparar y revisar el candidato Default

Sigue el [procedimiento MFIT](03-mfit-default.md):

1. Conserva configuración y código de tu propia unidad.
2. Usa una base coherente de datos de fábrica MFS/EFS compatible.
3. Construye controles Enhanced y Default.
4. Conserva el código original y toma únicamente el intervalo de datos revisado.
5. Vuelve a descomponer el candidato y comprueba todas las diferencias de configuración.
6. Compara las regiones completas y los sectores que sería necesario escribir.

El comparador offline del repositorio ayuda a revisar el mapa de este caso. No valida por sí solo integridad autenticada ni compatibilidad. El número de sectores depende de las imágenes de entrada: los 116 del caso no son un objetivo fijo para otras unidades.

Si partes de una placa sana, **no hay una fase previa de restauración obligatoria**. Prepara el candidato desde tus propias copias funcionales; el capítulo de recuperación queda como recurso de reversión.

## 6. Escribir, verificar y guardar resultados

La escritura del caso utilizó un ejecutor específico con comprobaciones de placa, mapa, permisos, hashes de origen, límites de sectores y lectura posterior. Los scripts ligados a esas imágenes privadas no se presentan como flasheadores universales para otros lectores.

Antes de usar un escritor para tu unidad, debe quedar definido qué sectores modificará, cómo comprobará la fuente, cómo verificará cada escritura y cómo restaurará una preimagen si falla. No sustituyas este paso por programar toda la salida de MFIT sin revisar las regiones.

Después de escribir, relee toda la SPI: el resultado debe coincidir con el candidato esperado y las otras regiones deben permanecer idénticas. Guarda informes, imágenes y hashes fuera del equipo antes de apagar.

## 7. Abrir FDO sin corriente y arrancar normalmente

Apaga el entorno de mantenimiento, desconecta la fuente y abre la unión de la resistencia. Aísla los extremos. No retires ni cortes el montaje con alimentación.

Arranca con la conexión abierta. En nuestro caso regresaron FDOPSS=1 y FRACC=0x4acf, y CSME pasó a estado Normal. Un arranque normal es necesario para que ME inicialice sus datos y para comprobar AMT.

## 8. Reaprovisionar y comprobar el resultado

1. Entra en MEBx y configura contraseña/red si la reconstrucción restableció esos datos.
2. Activa el acceso de red AMT y configura las opciones de consentimiento permitidas.
3. Consulta **PrivacyLevel=0**, **CanModifyOptInPolicy=1** y **OptInRequired=0**.
4. Comprueba el modo de control. No confundas ProvisioningMode con CurrentControlMode.
5. Abre una **sesión KVM nueva** sin consentimiento previo y comprueba que funciona sin código local.

El alojamiento de MeshCommander es una mejora independiente y se realiza después de tener AMT operativo: [guía web](04-meshcommander-web.md).
