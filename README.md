# Analizador de Gramáticas LL(1)

Este proyecto implementa un **analizador de gramáticas** que, a partir de un conjunto de producciones, calcula:

- **Conjunto FIRST** de cada símbolo no terminal.
- **Conjunto FOLLOW** de cada símbolo no terminal.
- **Conjuntos de PREDICCIÓN (PREDICT)** para cada producción, útiles para la construcción de una tabla LL(1).

---

## 📋 Contenido

- `codigo.py` — script principal en Python.
- `gramatica.txt` — archivo de texto con las producciones de la gramática (ver formato abajo).

---

## 🛠 Requisitos

- Python 3.6 o superior
- (Opcional) Entorno virtual (virtualenv, venv, conda, etc.)

---

## 🚀 Instalación

1. Clona o descarga este repositorio.
2. Coloca tus reglas de gramática en el archivo `gramatica.txt` siguiendo el formato especificado más abajo.
3. (Opcional) Crea y activa un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate      # Linux / macOS
   .\venv\Scripts\activate       # Windows PowerShell
   ```
4. Instala dependencias (si las hubiera). Por defecto no se requiere ninguna librería externa.

---

## ⚙️ Formato de entrada

- Cada línea de `gramatica.txt` define una producción en la forma:
  ```
  NoTerminal -> X Y Z ...
  ```
  - **NoTerminal** es el símbolo no terminal en el lado izquierdo.
  - Los símbolos de la derecha van separados por espacios.
  - Un símbolo terminal es cualquier carácter en minúscula o no alfabético.
  - Para la **ε** (producción vacía), usa el literal `ε`.

**Ejemplo** `gramatica.txt`:

```txt
S -> A B
A -> a A
A -> ε
B -> b B
B -> ε
```

---

## 📂 Uso

Desde la línea de comandos, sitúate en la carpeta del proyecto y ejecuta:

```bash
python codigo.py
```

- El script leerá `gramatica.txt` (ruta configurable en el código).
- Calcula e imprime por pantalla:
  - Lista de **TERMINALES** y **NO TERMINALES**.
  - Conjuntos **FIRST( X )** para cada no terminal.
  - Conjuntos **FOLLOW( X )** para cada no terminal.
  - Conjuntos de **PREDICCIÓN** para cada producción.

---

## 🔍 ¿Cómo funciona?

1. **Lectura y clasificación**

   - Se leen las producciones desde un archivo de texto.
   - Se separan y clasifican los símbolos en terminales y no terminales.

2. **Cálculo de FIRST**

   - Para cada símbolo:
     - Si es terminal, FIRST(símbolo) = { símbolo }.
     - Si es no terminal, recorre sus producciones aplicando las reglas de FIRST, incluyendo manejo de ε.

3. **Cálculo de FOLLOW**

   - Inicializa FOLLOW(S) = { `$` } para el símbolo inicial.
   - Itera hasta estabilizarse:
     - Para cada producción A → α B β, añade FIRST(β) \ {ε} a FOLLOW(B).
     - Si β puede derivar en ε (o β es vacío), añade FOLLOW(A) a FOLLOW(B).

4. **Conjuntos de PREDICCIÓN**

   - Para cada producción A → α:
     - Si ε ∉ FIRST(α), PREDICT = FIRST(α).
     - Si ε ∈ FIRST(α), PREDICT = (FIRST(α) \ {ε}) ∪ FOLLOW(A).

---

## 📝 Ejemplo de salida

```txt
--- TERMINALES ---
['a', 'b', 'ε']

--- NO TERMINALES ---
['S', 'A', 'B']

--- FIRST ---
FIRST(S) = ['a', 'b', 'ε']
FIRST(A) = ['a', 'ε']
FIRST(B) = ['b', 'ε']

--- FOLLOW ---
FOLLOW(S) = ['$']
FOLLOW(A) = ['a', 'b', '$']
FOLLOW(B) = ['$']

--- CONJUNTO DE PREDICCIÓN (PREDICT) ---
PREDICT(S -> A B) = ['a', 'b', '$']
PREDICT(A -> a A) = ['a']
PREDICT(A -> ε)   = ['b', '$']
PREDICT(B -> b B) = ['b']
PREDICT(B -> ε)   = ['$']
```

---

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Para aportar:

1. Haz un *fork* del repositorio.
2. Crea una rama con tu feature o corrección:
   ```bash
   git checkout -b feature/nombre-de-tu-feature
   ```
3. Realiza tus cambios y haz un *commit*:
   ```bash
   git commit -m "Descripción de tu cambio"
   ```
4. Empuja a tu repositorio remoto y abre un *Pull Request*.

---

## 📄 Licencia

Este proyecto está bajo la Licencia [MIT](LICENSE). ¡Puedes usarlo y modificarlo libremente!

---

