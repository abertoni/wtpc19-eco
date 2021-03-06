# Se importa la superclase de la cual hereda

from sc_animal import Animal

class Predador(Animal):
    """Subclase Predador que hereda de la superclase Animal."""
    
    def decidir(self,terreno):
        """Etapa de planificación. Observa el terreno y decide una acción pensando como predador. Si observa una presa y ésta se encuentra a una distancia inferior a su velocidad máxima, planea comerla; caso contrario, si se encuentra dentro de su rango de visión, planea perseguirla: se mueve para reducir su distancia con la presa más cercana; si tampoco cumple esta última condición, se planea moverse en alguna dirección aleatoria, una cantidad de pasos aleatorios inferior a su velocidad."""
        # Localiza a las presas visibles entre sus vecinos visibles
        vecinos_visibles = terreno.ubicar_vecinos(self)
        presas_visibles = [vecino for vecino in vecinos_visibles if vecino.get_clase() == "Presa"]
        # Si visualiza presas, calcula su distancia a ellas
        if len(presas_visibles) != 0:
            distancias_y_presas = {}
            for presa in presas_visibles:
                posicion_A = terreno.ubicar(self)
                posicion_B = terreno.ubicar(presa)
                distancia = terreno.calcular_distancia(posicion_A, posicion_B)
                distancias_y_presas[distancia] = presa
            # Determina la presa más cercana
            distancia_menor = min(list(distancias_y_presas.keys()))
            presa_mas_cercana = distancias_y_presas[distancia_menor]
            posicion_presa_mas_cercana = terreno.ubicar(presa_mas_cercana)
            # Si está más cerca que su velocidad máxima, planea comerlo (se ubica en la posición de la grilla de la presa y ésta desaparece) 
            if distancia_menor <= self.velocidad:
                self.plan = ("Comer", posicion_presa_mas_cercana)   
            # Si no está lo suficientemente próximo, planea perseguirlo    
            else:
                self.plan = ("Perseguir", posicion_presa_mas_cercana)
        # En caso de no observar presas cercanas, planea moverse en una dirección random para explorar
        else:
            posicion_random = terreno.generar_posicion_random()
            self.plan = ("Explorar", posicion_random)
 
    def ejecutar(self,terreno):
        """Realiza la acción del plan."""
        if self.plan[0] == "Comer":
            # Se mueve a la posición de la presa, borrándola de la grilla
            presa_objetivo = self.plan[1]
            terreno.mover(self, presa_objetivo)
            # Gana energía por consumir su presa
            self.modificar_energia(self.nutricion)
        elif self.plan[0] == "Perseguir" or self.plan[0] == "Explorar":
            # Se aproxima a su presa objetivo / se mueve a una posición random
            posicion_objetivo = self.plan[1]
            terreno.mover(self, posicion_objetivo)
            # Pierde energía por moverse
            self.modificar_energia(-self.coste_moverse)
