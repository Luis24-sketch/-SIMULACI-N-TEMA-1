import simpy
import random

# Canul Cauich Enrique Jesus
# Cervantes Chimal Luis Fernando

def cliente(env, numero, cajas, datos):

    llegada = env.now

    print("Cliente", numero, "llego al OXXO")

    with cajas.request() as turno:

        if len(cajas.queue) > datos["fila"]:
            datos["fila"] = len(cajas.queue)

        yield turno

        espera = env.now - llegada
        datos["espera"].append(espera)

        print("Cliente", numero, "paso a caja")
        print("Espero", round(espera, 2), "minutos")

        tiempo = random.randint(2, 5)
        datos["atencion"].append(tiempo)

        yield env.timeout(tiempo)

        print("Cliente", numero, "termino su compra y salio")
        print()


def entrada(env, cajas, clientes, datos):

    for i in range(1, clientes + 1):

        env.process(cliente(env, i, cajas, datos))

        tiempo = random.randint(1, 3)

        yield env.timeout(tiempo)


print("Simulacion de fila de OXXO")

clientes = int(input("Numero de clientes: "))
numero_cajas = int(input("Numero de cajas: "))

datos = {
    "espera": [],
    "atencion": [],
    "fila": 0
}

env = simpy.Environment()

cajas = simpy.Resource(env, capacity=numero_cajas)

env.process(entrada(env, cajas, clientes, datos))

print()
print("Iniciando simulacion...")
print()

env.run()

promedio_espera = sum(datos["espera"]) / len(datos["espera"])
promedio_atencion = sum(datos["atencion"]) / len(datos["atencion"])

print("Resultados:")
print("Clientes:", clientes)
print("Cajas:", numero_cajas)
print("Espera promedio:", round(promedio_espera, 2), "minutos")
print("Espera maxima:", round(max(datos["espera"]), 2), "minutos")
print("Atencion promedio:", round(promedio_atencion, 2), "minutos")
print("Fila maxima:", datos["fila"], "clientes")
print("Tiempo total:", round(env.now, 2), "minutos")
