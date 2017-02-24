class Player(object):
    
    reglasPuntos = {
        'campos' : [-1,-1,1,2,3,4,4,4,4,4,4,4,4,4],
        'pastos' : [-1,1,2,3,4,4,4],
        'cereales' : [-1,1,1,1,2,2,3,3,4,4,4,4,4,4,4,4,4,4,4],
        'hortalizas' : [-1,1,2,3,4,4,4,4,4,4,4,4,4,4,4],
        'ovejas' : [-1,1,1,1,2,2,3,3,4,4,4,4,4,4,4,4,4,4,4,4],
        'cerdos' : [-1,1,1,2,2,3,3,4,4,4,4,4,4,4,4,4,4,4,4],
        'vacas' : [-1,1,2,2,3,3,4,4,4,4,4,4,4,4,4,4,4,4],
        }
    
    
    def __init__(self, name, adquisicionesMenoresMano, oficiosMano):
        self.name = name
        #Basicos
        self.trabajadoresTotal = 2
        self.trabajadoresDispo = self.trabajadoresTotal
        self.recienNacidos     = 0
        self.materialCasa = 'madera'
        
        self.adquisicionesMayores = list()
        self.adquisicionesMenores = list()
        self.oficios = list()
        #Granja: 0-vacio, 1-habitacion, 2-campo, 3-pasto, 4-establo, 5-pasto+establo
        self.granja = np.zeros((5,3))
        self.granja[0,0] = 1
        self.granja[0,1] = 1
        self.sembrado = dict()
        self.pastos = dict()
        self.habitaciones =dict({1:{'casilla':(0,0), 'tipoAnimal':'-'},
                                 2:{'casilla':(1,0), 'tipoAnimal':'-'}}
                                 )
        # Mendigos                         
        self.mendigos = 0
                                 
        #Recursos
        self.reserva = collections.Counter()
        self.reserva['comida'] = 0
        self.reserva['piedra'] = 0
        self.reserva['madera'] = 0
        self.reserva['junco'] = 0
        self.reserva['adobe'] = 0
        
        #Animales
        self.reserva['ovejas'] = 0
        self.reserva['cerdos'] = 0
        self.reserva['vacas'] = 0
         #Vegetales
        self.reserva['cereales'] = 0        
        self.reserva['hostalizas'] = 0
        
        # Contador de recursos totales (en lugar de contar en sitios repartidos, por eficiencia)
        self.reservaTotal = collections.Counter()
        self.reservaTotal['cereales'] = 0        
        self.reservaTotal['hortalizas'] = 0    
        self.reservaTotal['ovejas'] = 0    
        self.reservaTotal['cerdos'] = 0    
        self.reservaTotal['vacas'] = 0  
        self.reservaTotal['establos'] = 0
        
        self.pasivas = dict()
        self.pasivas['ahorroMaterialhab'] = 0 # Paga solo 2 del material corr. por habitacion
        
    def cosecha(self):
        #Recolectar
        for k, (tipo, units) in self.sembrado.iteritems():
            if units > 0:
                self.sembrado[k]['units'] -= 1
                self.reserva[tipo] += 1
                if self.sembrado[k]['units'] == 0:
                    self.sembrado[k]['type'] = ''
        
        # Tributos a los dioses
        comidasNecesarias = (self.trabajadoresTotal * 2) - self.recienNacidos
        self.mendigos += -min((self.reserva['comida'] - comidasNecesarias, 0))
        self.reserva['comida'] = max((0, self.reserva['comida'] - comidasNecesarias))
        
        #TODO: reproduccion animales
                    
        
    def getScore(self):
        nHabitaciones = (self.granja==1).sum()
        nCampos = (self.granja==2).sum()
        nPastos = len(self.pastos)
        nVacias = (self.granja==0).sum()
        nEstablosVallados = (self.granja==5).sum()
        #TODO        
        
        puntos = collections.Counter()
        if self.materialCasa == 'adobe':
            puntos['casa'] = nHabitaciones
        elif self.materialCasa == 'piedra':
            puntos['casa'] = 2 * nHabitaciones
        puntos['campos'] = self.reglasPuntos['campos'][nCampos]
        puntos['pastos'] = self.reglasPuntos['pastos'][nPastos]
        puntos['cereales'] = self.reglasPuntos['cereales'][self.reservaTotal['cereales']]
        puntos['hortalizas'] = self.reglasPuntos['hortalizas'][self.reservaTotal['hortalizas']]
        puntos['ovejas'] = self.reglasPuntos['ovejas'][self.reservaTotal['ovejas']]
        puntos['cerdos'] = self.reglasPuntos['cerdos'][self.reservaTotal['cerdos']]
        puntos['vacas'] = self.reglasPuntos['vacas'][self.reservaTotal['vacas']]
        puntos['vacias'] = -nVacias
        puntos['establosVallados'] = nEstablosVallados
        puntos['familia'] = 3 * self.trabajadoresTotal
        puntos['mendigos'] = -3 * self.mendigos
        #TODO: puntos por cartas
        self.printScore() 
        return sum(puntos.values())
        
    def printScore(self):
        s = self.name + "\n\
  Recursos:\n\
    Comida: %d\n\
    Madera: %d\n\
    Adobe : %d\n\
    Junco : %d\n\
    Piedra: %d\n\
  Vegetales:\n\
    Cereales  : %d\n\
    Hortalizas: %d\n\
  Mendigos: %d\n\
                " % (self.reserva['comida'],
                    self.reserva['madera'],
                    self.reserva['adobe'],
                    self.reserva['junco'],
                    self.reserva['piedra'],
                    self.reservaTotal['cereales'],
                    self.reservaTotal['hortalizas'],
                    self.mendigos)
        print s
        
    def toJson(self):
        d = dict()
        d['granja'] = str(self.granja)
        d['trabajadoresTotal'] = str(self.trabajadoresTotal)
        d['trabajadoresDispo'] = str(self.trabajadoresDispo)
        d['recienNacidos'] = str(self.recienNacidos)
        # TODO: Seguir aqui
