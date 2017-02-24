# -*- coding: utf-8 -*-
"""
Created on Tue Feb 07 20:28:04 2017

@author: rafel
"""
import sys
import numpy as np
import collections
import random
#Considerar:
#   Una IA es capaz de, dado un estado de la partida,
#   ponerse en el lugar del jugador al que le toca jugar y dar una acción a realizar por
#   dicho jugador.

#TODO: Estoy adaptando toda la entrada/salida en formato JSON
#TODO: Meter subacciones.

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

class Action(object):
    # Todo son acciones, incluso las de sacrificar animal para obtener comida. Lo unico que algunas cuestan trabajadores,
    # que se considera que se "gastan" y se "reponen" cada ronda
    # Las subacciones son las distintas posibilidades que tiene cada jugador en cada accion
    #TODO: Seguir metiendo acciones aqui. 
    #TODO: meter la funcion que crea la lista de subacciones en la lista subactionsFunction
    def __init__(self, name):
        self.name    = name
        self.ocupada = False
        if name == 'Mina':
            self.applyFunction      = self._fMina
            self.replenishFunction  = self._rMina
            self.subactionsFunction = self._sMina
            self.costTrabajadores   = 1
            self.units              = 0
            self.material           = 'adobe'
        if name == 'Bosque':
            self.applyFunction     = self._fBosque
            self.replenishFunction = self._rBosque
            self.costTrabajadores  = 1
            self.units             = 0
            self.material          = 'madera'
        if name == 'Juncal':
            self.applyFunction     = self._fJuncal
            self.replenishFunction = self._rJuncal
            self.costTrabajadores  = 1
            self.units             = 0
            self.material          = 'junco'
        if name == 'Pesca':
            self.applyFunction     = self._fPesca
            self.replenishFunction = self._rPesca
            self.costTrabajadores  = 1
            self.units             = 0
            self.material          = 'comida'
        if name == 'Semilla de cereales':
            self.applyFunction     = self._fSemillaCereales
            self.replenishFunction = self._rSemillaCereales
            self.costTrabajadores  = 1
        if name == 'Jornalero':
            self.applyFunction     = self._fJornalero
            self.replenishFunction = self._rJornalero
            self.costTrabajadores  = 1
        if name == 'Labranza':
            self.applyFunction     = self._fLabranza
            self.replenishFunction = self._rLabranza
            self.costTrabajadores  = 1
        if name == 'Lugar de encuentro':
            self.applyFunction     = self._fLugarEncuentro
            self.replenishFunction = self._rLugarEncuentro
            self.costTrabajadores  = 1
        if name == 'Arboleda_3':
            self.applyFunction     = self._fArboleda_3
            self.replenishFunction = self._rArboleda_3
            self.costTrabajadores  = 1
            self.units             = 0
            self.material          = 'madera'
        if name == 'Yacimiento_3':
            self.applyFunction     = self._fYacimiento_3
            self.replenishFunction = self._rYacimiento_3
            self.costTrabajadores  = 1
            self.units             = 0
            self.material          = 'adobe'
        
        
    def applyAction(self, game, params):
        self.applyFunction(game, params)
        
        
    def applyReplenish(self):
        self.replenishFunction()
        
        
    def getSubactionsList(self):
        self.subactionsFunction()
        
    # Funciones de acciones
    def _fMina(action, game, params=None):
        cp = game.currentPlayer
        cp.reserva['adobe'] += action.units
        action.units = 0
        cp.trabajadoresDispo -= action.costTrabajadores
        action.ocupada = True
        
    def _fPesca(action, game, params=None):
        cp = game.currentPlayer
        cp.reserva['comida'] += action.units
        action.units = 0
        cp.trabajadoresDispo -= action.costTrabajadores
        action.ocupada = True
        
    def _fJornalero(action, game, params=None):
        #TODO: Aciones que se disparan al usar jornalero
        cp = game.currentPlayer
        cp.reserva['comida'] += 2
        cp.trabajadoresDispo -= action.costTrabajadores
        action.ocupada = True
        
    def _fSemillaCereales(action, game, params=None):
        cp = game.currentPlayer
        cp.reserva['cereales'] += 1
        cp.reservaTotal['cereales'] += 1
        cp.trabajadoresDispo -= action.costTrabajadores
        action.ocupada = True
        
    def _fBosque(action, game, params=None):
        cp = game.currentPlayer
        cp.reserva['madera'] += action.units
        action.units = 0
        cp.trabajadoresDispo -= action.costTrabajadores
        action.ocupada = True
        
    def _fArboleda_3(action, game, params=None):
        cp = game.currentPlayer
        cp.reserva['madera'] += action.units
        action.units = 0
        cp.trabajadoresDispo -= action.costTrabajadores
        action.ocupada = True
        
    def _fJuncal(action, game, params=None):
        cp = game.currentPlayer
        cp.reserva['junco'] += action.units
        action.units = 0
        cp.trabajadoresDispo -= action.costTrabajadores
        action.ocupada = True
        
    def _fYacimiento_3(action, game, params=None):
        cp = game.currentPlayer
        cp.reserva['adobe'] += action.units
        action.units = 0
        cp.trabajadoresDispo -= action.costTrabajadores
        action.ocupada = True
        
    def _fLabranza(action, game, params):
        # Params:  casilla en la que pone el campo. Ej: params = (1,3)
        casilla = params
        cp = game.currentPlayer
        cp.granja[casilla] = 2
        cp.sembrado[casilla] = {'type':'', 'units':0}
        cp.trabajadoresDispo -= action.costTrabajadores
        action.ocupada = True
        
    def _fLugarEncuentro(action, game, params):
        # Params: lista de 2 elementos
        #  Quiere el token: boolean
        #  TODO:Carta que quiere bajar
        cp = game.currentPlayer
        game.dealer = game.turn
        cp.trabajadoresDispo -= action.costTrabajadores
        action.ocupada = True
        
    def _fAmpliarGranja(action, game, params=None):
        # listHabs:     lista de casillas donde poner la habitacion
        # listEstablos: idem pero para establos
        cp = game.currentPlayer
        listHabs, listEstablos = params
        for hab in listHabs:
            cp.granja[hab] = 1
            cp.reserva[cp.materialCasa] -= 5
            cp.reserva['junco'] -= 2
        for establo in listEstablos:
            if cp.granja[establo] == 3:
                # Si es un pasto (3), establo vallado (5)
                cp.granja[establo] = 5
            else:
                # Si no habia nada, establo (4)
                cp.granja[establo] = 4
            cp.reserva['madera'] -= 2
        cp.trabajadoresDispo -= action.costTrabajadores
            
    # Funciones de reponer
    def _rMina(self):
        self.units += 1
    def _rYacimiento_3(self):
        self.units += 1
    def _rPesca(self):
        self.units += 1
    def _rBosque(self):
        self.units += 3
    def _rArboleda_3(self):
        self.units += 2
    def _rJuncal(self):
        self.units += 1
    def _rJornalero(self):
        pass
    def _rSemillaCereales(self):
        pass
    def _rLabranza(self):
        pass
    def _rLugarEncuentro(self):
        pass
    
    # Funciones para obtener subacciones
    #TODO: estas funciones generan el listado de subacciones posibles dado el estado del jugador actual
    def _sMina(self, player):
        pass
        
        
    def __str__(self):
        s = self.name
        if hasattr(self, 'units'):
            s += ' --> %d %s(s)' % (self.units, self.material)
        return s
        

class Agricola(object):
    
    def __init__(self, playerNames, json=None):
        self.players = list()
        for i in range(0, len(playerNames)):
            self.players.append(Player(playerNames[i], [], []))
        self.round = 0
        self.dealer = random.randint(0,len(playerNames)-1)
        self.actions = list()
        self.actions.append(Action('Mina'))
        self.actions.append(Action('Bosque'))
        self.actions.append(Action('Juncal'))
        self.actions.append(Action('Pesca'))
        self.actions.append(Action('Pesca'))
        self.actions.append(Action('Jornalero'))
        self.actions.append(Action('Labranza'))
        self.actions.append(Action('Labranza'))
        self.actions.append(Action('Labranza'))
        self.actions.append(Action('Lugar de encuentro'))
        self.actions.append(Action('Semilla de cereales'))
        self.actions.append(Action('Arboleda_3'))
        self.actions.append(Action('Yacimiento_3'))
        self.nextRound()
        self.refreshPossibleActions()

    
    def nextTurn(self):
        turnoIncial = self.turn
        self.turn = (self.turn + 1) % len(self.players)
        while self.players[self.turn].trabajadoresDispo == 0 and self.turn != turnoIncial:
            self.turn = (self.turn + 1) % len(self.players)
        self.currentPlayer = self.players[self.turn]
        
    def isEndOfRound(self):
        return sum([p.trabajadoresDispo for p in self.players]) == 0
            
    
    def nextRound(self):
        #TODO: Sacar accion nueva al tablero
        self.round += 1
        self.turn = self.dealer
        self.currentPlayer = self.players[self.turn]
        self.replenish()
        for p in self.players:
            p.trabajadoresDispo = p.trabajadoresTotal
        for a in self.actions:
            a.ocupada = False
        self.refreshPossibleActions()
        
    def replenish(self):
        for action in self.actions:
            action.applyReplenish()
            
    def cosecha(self):
        for p in self.players:
            p.cosecha()
    
    def isFinished(self):
        if self.round < 1:
            return False
        for p in self.players:
            if p.trabajadoresDispo > 0:
                return False
        return True
        
    def getScoreAll(self):
        for p in self.players:
            print p.getScore()
    
    def _isPossibleAction(self, action):
        #TODO: Filtrar si el jugador no puede asumir el coste
        if action.ocupada:
            return True
        return False
    
    def refreshPossibleActions(self):
        self.possibleActions = list()
        for action in self.actions:
            if not self._isPossibleAction(action):
                self.possibleActions.append(action)
    
    def getPossibleActions(self):
        return self.possibleActions
        
    def getAllActions(self):
        return self.actions
        
    def printState(self):
        print "Ronda %d, turno para %s, le quedan %d trabajadores" % (
            self.round, 
            self.currentPlayer.name, 
            self.currentPlayer.trabajadoresDispo)

    def applyAction(self, action, params=None):
        action.applyAction(self, params)
        self.refreshPossibleActions()
        
    def toJson(self):
        d = dict()
        d['players'] = dict()
        for i,p in enumerate(self.players):
            d['players'][i] = p.toJson()
        d['dealer'] = self.dealer
        d['turn'] = self.turn
        d['round'] = self.round
        return d
        
        
class Master(object):
    def __init__(self):
        self.agricola = Agricola(('Player1', 'Player2', 'Player3'))
        
        self.ias            = dict()
        self.ias['Player1'] = ArtificialIntelligence()
        self.ias['Player2'] = ArtificialIntelligence()
        self.ias['Player3'] = ArtificialIntelligence()
    
    def playGame(self):
        self.playRound()
        self.playRound()
        self.playRound()
        self.playRound()
        self.cosecha()
        self.playRound()
        self.playRound()
        self.playRound()
        self.cosecha()
        self.playRound()
        self.playRound()
        self.cosecha()
        self.playRound()
        self.playRound()
        self.cosecha()
        self.playRound()
        self.playRound()
        self.cosecha()
        self.playRound()
        self.cosecha()
        print self.agricola.getScoreAll()
        print "TERMINA EL JUEGO"
        
    def playRound(self):
        while not self.agricola.isEndOfRound():
            self.agricola.printState()
            action, params = self.ias[self.agricola.currentPlayer.name].nextMove(self.agricola)
            self.agricola.applyAction(action, params)
            print "%s juega %s" % (self.agricola.currentPlayer.name, action.name)
            self.agricola.nextTurn()
        self.agricola.nextRound()
    
    def cosecha(self):
        self.agricola.cosecha()

        
        
        
        
class ArtificialIntelligence(object):
    def __init__(self):
        pass
    
    def nextMove(self, agricola):
        cp = agricola.currentPlayer
        params = None
        actions = agricola.getPossibleActions()
        action = actions[random.randint(0,len(actions)-1)]
        if action.name == 'Labranza':
            params = tuple(self._selectCampoLocation(cp.granja))
        return action, params
        
    # labranza
    def _selectCampoLocation(self, granja):
        return self._getVaciosGranja(granja)[0]
    
    def _getVaciosGranja(self, granja):
        return np.transpose(np.where(granja == 0))
        
        

class IAManual(object):
    def __init__(self):
        pass
    
    def nextMove(self, agricola):
        actions = agricola.getPossibleActions()
        for i, action in enumerate(actions):
            print str(i) + ' --> ' + str(action)
        decision = raw_input()
        return actions[int(decision)]

       
m = Master()
print m.agricola.toJson()
m.playGame()


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
