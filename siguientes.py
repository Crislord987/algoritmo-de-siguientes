# Función para identificar si un símbolo es terminal
def definir_terminales(simbolo):
    return simbolo.islower() or not simbolo.isalpha()

# Inicialización
producciones = {}
terminales = []
no_terminales = []

# Leer archivo con reglas
with open('D:/Trabajos u/Quinto semestre/Sistemas operativos/Analizador gramatica/read.py', 'r', encoding='utf-8') as archivo:
    for linea in archivo:
        izquierda, derecha = linea.strip().split("->")
        izquierda = izquierda.strip()
        simbolos = derecha.strip().split()

        if izquierda not in no_terminales:
            no_terminales.append(izquierda)

        for simbolo in simbolos:
            if definir_terminales(simbolo):
                if simbolo not in terminales:
                    terminales.append(simbolo)
            elif simbolo not in no_terminales:
                no_terminales.append(simbolo)

        if izquierda not in producciones:
            producciones[izquierda] = []
        producciones[izquierda].append(simbolos)

# ------------------ FIRST ------------------

firsts = {}

def calcular_first(simbolo, visitados=None):
    if visitados is None:
        visitados = set()

    if definir_terminales(simbolo):
        return {simbolo}

    if simbolo in firsts:
        return firsts[simbolo]

    visitados.add(simbolo)
    resultado = set()

    for produccion in producciones.get(simbolo, []):
        for s in produccion:
            first_s = calcular_first(s, visitados.copy())
            resultado.update(first_s - {'ε'})
            if 'ε' not in first_s:
                break
        else:
            resultado.add('ε')

    firsts[simbolo] = resultado
    return resultado

for nt in no_terminales:
    calcular_first(nt)

# ------------------ FOLLOW ------------------

follows = {nt: set() for nt in no_terminales}
follows[no_terminales[0]].add('$')  # símbolo inicial

def calcular_follow():
    cambiado = True
    while cambiado:
        cambiado = False
        for A in no_terminales:
            for produccion in producciones.get(A, []):
                for i in range(len(produccion)):
                    B = produccion[i]
                    if B in no_terminales:
                        siguiente = produccion[i+1:]
                        first_siguiente = set()

                        if siguiente:
                            for s in siguiente:
                                first_s = calcular_first(s)
                                first_siguiente.update(first_s - {'ε'})
                                if 'ε' not in first_s:
                                    break
                            else:
                                first_siguiente.add('ε')
                        else:
                            first_siguiente.add('ε')

                        antes = len(follows[B])
                        follows[B].update(first_siguiente - {'ε'})
                        if 'ε' in first_siguiente:
                            follows[B].update(follows[A])
                        if len(follows[B]) > antes:
                            cambiado = True

calcular_follow()

# ------------------ PREDICT ------------------

predict = []

for A in no_terminales:
    for produccion in producciones[A]:
        first_alpha = set()
        for simbolo in produccion:
            f = calcular_first(simbolo)
            first_alpha.update(f - {'ε'})
            if 'ε' not in f:
                break
        else:
            first_alpha.add('ε')

        # Si epsilon en FIRST(α), agregar FOLLOW(A)
        if 'ε' in first_alpha:
            conjunto_prediccion = (first_alpha - {'ε'}) | follows[A]
        else:
            conjunto_prediccion = first_alpha

        predict.append((A, produccion, sorted(conjunto_prediccion)))

# ------------------ RESULTADOS ------------------

print("\n--- TERMINALES ---")
print(terminales)

print("\n--- NO TERMINALES ---")
print(no_terminales)

print("\n--- FIRST ---")
for nt in no_terminales:
    print(f"FIRST({nt}) = {sorted(firsts[nt])}")

print("\n--- FOLLOW ---")
for nt in no_terminales:
    print(f"FOLLOW({nt}) = {sorted(follows[nt])}")

print("\n--- CONJUNTO DE PREDICCIÓN (PREDICT) ---")
for A, produccion, conjunto in predict:
    print(f"PREDICT({A} -> {' '.join(produccion)}) = {conjunto}")
