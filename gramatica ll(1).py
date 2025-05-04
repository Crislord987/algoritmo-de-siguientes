# Función para identificar si un símbolo es terminal
def definir_terminales(simbolo):
    return simbolo.islower() or not simbolo.isalpha()

# Inicialización
producciones = {}
terminales = []
no_terminales = []

# Leer archivo con reglas
try:
    with open('D:/Trabajos u/Quinto semestre/Sistemas operativos/Analizador gramatica/read.py', 'r', encoding='utf-8') as archivo:
        for linea in archivo:
            if not linea.strip():  # Saltar líneas vacías
                continue
            
            try:
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
            except ValueError:
                print(f"Error al procesar la línea: {linea.strip()}")
except FileNotFoundError:
    print("Archivo no encontrado. Asegúrate que la ruta sea correcta.")
    exit(1)

# ------------------ ELIMINACIÓN DE RECURSIVIDAD POR LA IZQUIERDA ------------------

def eliminar_recursividad_izquierda():
    nuevas_producciones = {}
    nuevos_no_terminales = []

    for A in list(no_terminales):  # Usamos list() para crear una copia estática
        recursivas = []
        no_recursivas = []

        for produccion in producciones.get(A, []):
            if produccion and produccion[0] == A:
                recursivas.append(produccion[1:])  # quitar el A
            else:
                no_recursivas.append(produccion)

        if recursivas:
            A_prime = A + "'"
            while A_prime in no_terminales or A_prime in nuevos_no_terminales:
                A_prime += "'"

            nuevos_no_terminales.append(A_prime)

            nuevas_producciones[A] = []
            nuevas_producciones[A_prime] = []

            for prod in no_recursivas:
                nuevas_producciones[A].append(prod + [A_prime])

            for prod in recursivas:
                nuevas_producciones[A_prime].append(prod + [A_prime])

            nuevas_producciones[A_prime].append(['ε'])
        else:
            nuevas_producciones[A] = producciones.get(A, [])

    no_terminales.extend(nuevos_no_terminales)
    producciones.clear()
    producciones.update(nuevas_producciones)

# Ejecutar la eliminación de recursividad
eliminar_recursividad_izquierda()

# ------------------ FIRST ------------------

firsts = {}

def calcular_first(simbolo, visitados=None):
    if visitados is None:
        visitados = set()
    
    # Si simbolo es epsilon, retornar conjunto con epsilon
    if simbolo == 'ε':
        return {'ε'}
    
    # Si es terminal, retornar conjunto con el terminal
    if definir_terminales(simbolo):
        return {simbolo}
    
    # Si ya calculamos FIRST para este símbolo, retornarlo
    if simbolo in firsts:
        return firsts[simbolo]
    
    # Si ya visitamos este símbolo, evitar recursión infinita
    if simbolo in visitados:
        return set()
    
    visitados.add(simbolo)
    resultado = set()
    
    # Si el símbolo no existe en producciones (puede ser un error en la gramática)
    if simbolo not in producciones:
        print(f"Advertencia: No hay producciones para el símbolo '{simbolo}'")
        firsts[simbolo] = set()
        return set()
    
    for produccion in producciones[simbolo]:
        if not produccion:  # Si la producción está vacía
            continue
            
        if produccion[0] == 'ε':  # Si la producción es epsilon
            resultado.add('ε')
            continue
            
        for s in produccion:
            if s == simbolo:  # Evitar recursión directa
                continue
                
            first_s = calcular_first(s, visitados.copy())
            resultado.update(first_s - {'ε'})
            
            if 'ε' not in first_s:
                break
        else:  # Este else pertenece al bucle for, se ejecuta si no hay break
            resultado.add('ε')
    
    firsts[simbolo] = resultado
    return resultado

# Calcular FIRST para todos los no terminales
for nt in no_terminales:
    if nt not in firsts:
        firsts[nt] = calcular_first(nt)

# ------------------ FOLLOW ------------------

follows = {nt: set() for nt in no_terminales}
follows[no_terminales[0]].add('$')  # símbolo inicial

def calcular_follow():
    cambiado = True
    while cambiado:
        cambiado = False
        for A in no_terminales:
            for B in no_terminales:
                for produccion in producciones.get(B, []):
                    for i in range(len(produccion)):
                        if produccion[i] == A:  # Si encontramos A en la producción
                            siguiente = produccion[i+1:]
                            first_siguiente = set()
                            
                            # Si A no es el último símbolo
                            if siguiente:
                                todos_derivan_epsilon = True
                                for s in siguiente:
                                    if s not in firsts:
                                        firsts[s] = calcular_first(s)
                                    
                                    first_s = firsts[s]
                                    first_siguiente.update(first_s - {'ε'})
                                    
                                    if 'ε' not in first_s:
                                        todos_derivan_epsilon = False
                                        break
                                
                                # Si todos los símbolos pueden derivar a epsilon
                                if todos_derivan_epsilon:
                                    antes = len(follows[A])
                                    follows[A].update(follows[B])
                                    if len(follows[A]) > antes:
                                        cambiado = True
                            else:  # Si A es el último símbolo
                                antes = len(follows[A])
                                follows[A].update(follows[B])
                                if len(follows[A]) > antes:
                                    cambiado = True
                            
                            # Agregar FIRST(siguiente) - {ε} a FOLLOW(A)
                            antes = len(follows[A])
                            follows[A].update(first_siguiente)
                            if len(follows[A]) > antes:
                                cambiado = True

# Calcular FOLLOW para todos los no terminales
calcular_follow()

# ------------------ PREDICT ------------------

predict = []

for A in no_terminales:
    for produccion in producciones.get(A, []):
        first_alpha = set()
        todos_derivan_epsilon = True
        
        for simbolo in produccion:
            if simbolo == 'ε':
                first_alpha.add('ε')
                continue
                
            if simbolo not in firsts:
                firsts[simbolo] = calcular_first(simbolo)
                
            f = firsts[simbolo]
            first_alpha.update(f - {'ε'})
            
            if 'ε' not in f:
                todos_derivan_epsilon = False
                break
        
        # Si todos los símbolos pueden derivar a epsilon o la producción es epsilon
        if todos_derivan_epsilon or produccion == ['ε']:
            conjunto_prediccion = (first_alpha - {'ε'}) | follows[A]
        else:
            conjunto_prediccion = first_alpha
        
        predict.append((A, produccion, sorted(list(conjunto_prediccion))))

# ------------------ RESULTADOS ------------------

print("\n--- TERMINALES ---")
print(terminales)

print("\n--- NO TERMINALES ---")
print(no_terminales)

print("\n--- PRODUCCIONES DESPUÉS DE ELIMINAR RECURSIVIDAD IZQUIERDA ---")
for nt, prods in producciones.items():
    for prod in prods:
        print(f"{nt} -> {' '.join(prod)}")

print("\n--- FIRST ---")
for nt in no_terminales:
    print(f"FIRST({nt}) = {sorted(list(firsts.get(nt, set())))}")

print("\n--- FOLLOW ---")
for nt in no_terminales:
    print(f"FOLLOW({nt}) = {sorted(list(follows[nt]))}")

print("\n--- CONJUNTO DE PREDICCIÓN (PREDICT) ---")
for A, produccion, conjunto in predict:
    print(f"PREDICT({A} -> {' '.join(produccion)}) = {conjunto}")

# ------------------ LL(1) CHECK ------------------

# Crear diccionario para agrupar producciones por no terminal
predict_por_no_terminal = {}

for A, produccion, conjunto in predict:
    if A not in predict_por_no_terminal:
        predict_por_no_terminal[A] = []
    predict_por_no_terminal[A].append((produccion, set(conjunto)))

# Función para verificar si dos conjuntos se intersecan
def hay_conflicto(conj1, conj2):
    return not conj1.isdisjoint(conj2)

# Verificar si la gramática es LL(1)
es_LL1 = True
for A, producciones in predict_por_no_terminal.items():
    for i in range(len(producciones)):
        for j in range(i + 1, len(producciones)):
            prod_i, conj_i = producciones[i]
            prod_j, conj_j = producciones[j]
            if hay_conflicto(conj_i, conj_j):
                es_LL1 = False
                print(f"Conflicto LL(1) encontrado en {A}:")
                print(f" - {A} -> {' '.join(prod_i)} PREDICT={sorted(list(conj_i))}")
                print(f" - {A} -> {' '.join(prod_j)} PREDICT={sorted(list(conj_j))}\n")

if es_LL1:
    print("\n La gramática ES LL(1).")
else:
    print("\n La gramática NO es LL(1). Revisa los conflictos mostrados.")