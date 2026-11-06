# 5. Cronología y caminos que descartamos

El valor de este caso está también en evitar repetir los intentos que no resolvieron la causa.

| Fase | Resultado observado | Lección |
| --- | --- | --- |
| KVM exige consentimiento | Enhanced seguía imponiendo PIN | El cliente no puede anular cualquier política de plataforma |
| Editar únicamente FITC/OEM | El estado efectivo siguió Enhanced | Un byte y su CRC no sincronizan los datos inicializados |
| Restablecimiento parcial de AMT | Se perdió aprovisionamiento/red anterior; la política no se resolvió | Registrar primero red, claves y alcance del reset |
| Cambiar o eliminar selectivamente archivos MFS de política | No produjo una solución funcional | La integridad y coherencia de los datos importan |
| Trasplantar únicamente MFS de fábrica | CSME dejó de inicializarse; faltaron dispositivos | Conservar coherencia MFS/EFS y compatibilidad |
| Recuperación por USB sin permisos suficientes | Assertions y parada sin continuar | Mantener las guardas y leer el estado real |
| Reiniciar o borrar CMOS | No restauró esos datos de ME | CMOS y datos persistentes CSME son diferentes |
| FDO mediante HDA_SDO | Se comprobó acceso completo a la SPI | El códec facilitó acceso a una señal de arranque del PCH |
| Dos copias completas y restauración de ME propio | Se recuperó la base funcional; reapareció NVMe | Priorizar recuperación antes del cambio de política |
| MFIT sobre datos ya inicializados | Opción de privacidad de solo lectura; builds iguales | No flashear un candidato que no hace el cambio |
| MFIT con base de fábrica MFS/EFS compatible y configuración propia | Candidato Default con código original conservado | Revisar diferencias completas y volver a descomponer |
| Escritura selectiva y readback de toda la flash | 116 sectores de datos verificados, exterior de ME intacto | Que un escritor termine no basta sin lectura posterior |
| Abrir FDO y arrancar normalmente | ME Normal, PrivacyLevel=0 y OptInRequired=0 | Validar la política en ejecución |
| Contraseña/red/opciones de MEBx | El propietario recuperó gestión operativa | Una reconstrucción de datos puede exigir reaprovisionar |
| Firmware Loader de MeshCommander | Falló para el objetivo del propietario | Distinguir el cargador de Web Application Hosting |
| Carga manual Small y después Medium | El propietario confirmó funcionamiento | KVM podía servirse desde la IP de AMT |
| Sustitución por index.htm | Archivo raíz observado en navegador; entrada automática desde / no confirmada | Separar carga del archivo y sustitución efectiva de la portada |

No hubo que desoldar M_BIOS, instalar otro hipervisor ni formatear unidades. El daño no se atribuye a un fallo físico demostrado del NVMe.

## Niveles de evidencia

**Medido por herramientas durante la intervención:** lecturas SPI idénticas, diferencias limitadas, readback final, estado CSME y valores de privacidad/opt-in.

**Confirmado por el propietario:** recuperación de BIOS/MEBx y operación normal; funcionamiento de las aplicaciones Small y Medium.

**Procedimiento externo o aún no probado aquí:** frontera de 65.535 bytes de otra instalación, funcionamiento de Large, entrada automática por /, una matriz completa de funciones de las tres ediciones y persistencia tras futuras actualizaciones de BIOS.

Los resúmenes intermedios del diagnóstico se escribieron antes de terminar la reparación. La ficha de este repositorio recoge el resultado final conocido, no convierte cada plan intermedio en una operación ejecutada.
