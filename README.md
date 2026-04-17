# tesis_acuacultura_ia
Sistema basado en inteligencia artificial para la predicción de riesgo sanitario en la producción de camarón

## Descripción

Este proyecto tiene como objetivo desarrollar un modelo de inteligencia artificial capaz de predecir el nivel de riesgo sanitario en la producción de camarón, utilizando variables de calidad de agua.

El modelo busca apoyar la toma de decisiones operativas en sistemas acuícolas, reduciendo la dependencia exclusiva de la interpretación técnica en campo.

Adicionalmente, este proyecto representa el primer paso en el desarrollo de un **asesor técnico acuícola basado en datos**, cuyo objetivo es permitir la toma de decisiones fundamentadas en información objetiva, minimizando la dependencia de criterios subjetivos y opiniones.

---

## Dataset

El dataset utilizado proviene de reportes reales de análisis de calidad de agua en piscinas de producción acuícola.

Incluye variables como:

- TAN
- NH3 (amoníaco tóxico)
- Nitritos (NO2)
- Nitratos (NO3)
- Fosfatos (PO4)
- Sulfuro
- Alcalinidad
- pH
- Temperatura
- Salinidad

La variable objetivo es:

- **NRS (Nivel de Riesgo Sanitario): Bajo, Medio, Alto**

---

## Modelos implementados

### Modelo principal
- Random Forest
- Accuracy: 84%

### Modelo baseline
- Decision Tree
- Accuracy: 77%

---

## Resultados

El modelo Random Forest mostró una mejora en el desempeño frente al baseline, evidenciando mayor capacidad para capturar relaciones no lineales entre variables.

Las variables más relevantes fueron:

- PO4
- TAN
- NH3
- Temperatura

---

## Estructura del repositorio

/notebooks
01_modelo_principal.ipynb
02_baseline_modelo.ipynb

Base_de_datos_CA.xlsx

---

## Conclusión

El modelo desarrollado demuestra que es posible predecir el riesgo sanitario a partir de variables de calidad de agua.

Este proyecto constituye una base sólida para la evolución hacia un sistema inteligente de apoyo a decisiones en acuacultura, alineado con un enfoque de gestión basado en datos.

---

## Integrantes

- Maria Victoria Maldonado Peralta
- Carlos alberto Moya Vera
