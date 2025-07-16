# Pruebas UI con Selenium para la interfaz web de ***UrbanRoutes***

UrbanRoutes es una aplicación de alquiler de vehículo, donde los usuarios pueden disponer de diferentes servicios de transporte. En este proyecto se realizan pruebas de UI a la interfaz web de la aplicación, asegurando que se cumplan los requisitos para el alquiler de vehículo de una tarifa en específico.

## 🧪 Herramientas utilizadas

- Python 3.12
- Selenium
- Pytest
- POM(Page Object Model)

## ✅ Pruebas implementadas

Estas pruebas fueron automatizadas utilizando Selenium WebDriver con el patrón Page Object Model (POM) en Python, lo que permite una mayor modularidad, reutilización y mantenibilidad del código. Las pruebas realizadas se centran en comprobar el funcionamiento de pedido de taxi para la tarifa **"Comfort"**. Para ello, se prueban las siguientes funcionalidades:

- Selección de dirección de **origen** y **destino**
- Selección del modo de viaje **"Pedir un taxi"**
- Elección de la tarifa **"Comfort"**
- Ingreso y verificación del **número telefónico**
- Ingreso de datos de **tarjeta de crédito**
- Inclusión de un **mensaje para el conductor**
- Selección de **productos adicionales** ofrecidos con la tarifa
- Solicitud del **pedido de taxi**
- Verificación del **tiempo estimado de llegada** del conductor

Durante la ejecución, se validan los resultados en cada paso mediante aserciones (`assert`) para asegurar que los valores mostrados coincidan con lo esperado.

## ▶️ Ejecución de pruebas

Primero, debe asegurarse de tener los siguientes recursos:

``` bash
    pip install selenium pytest
```

Para realizar las pruebas, ejecuta:

``` bash
    pytest -v
```