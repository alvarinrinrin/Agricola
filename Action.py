# -*- coding: utf-8 -*-
"""
Created on Wed Mar 01 19:34:11 2017

@author: rafel
"""

class Action(object):
    # Todo son acciones, incluso las de sacrificar animal para obtener comida. Lo unico que algunas cuestan trabajadores,
    # que se considera que se "gastan" y se "reponen" cada ronda
    # Las subacciones son las distintas posibilidades que tiene cada jugador en cada accion

    # A un objeto Action se le puede pedir (a modo de interfaz):
    #  ocupada            : Si esta ocupado o no.
    #  units              : Unidades que contiene, en caso que sea de tipo "acumulacion".
    #  material           : Tipo de material del cual tiene |units| unidades.
    #  replenishFunction  : En caso que sea de tipo "acumulacion", se le aplica este efecto cada inicio de ronda.
    #  subactionsFunction : Devuelve una lista de subActions que puede realizar el jugador "currentPlayer" con los 
    #                       recursos de los que dispone.

    #TODO: Quitar la funcion applyFunction de esta clase, ya que la que se aplica es la subAction ahora. 
    #TODO: meter la funcion que crea la lista de subacciones en la lista subactionsFunction
    def __init__(self, name):
        self.name    = name
        self.ocupada = False
        if name == 'Mina':
            self.replenishFunction  = self._rMina
            self.subactionsFunction = self._sMina
            self.costTrabajadores   = 1
            self.units              = 0
            self.material           = 'adobe'
        if name == 'Bosque':
            self.replenishFunction = self._rBosque
            self.subactionsFunction = self._sBosque
            self.costTrabajadores  = 1
            self.units             = 0
            self.material          = 'madera'
        if name == 'Juncal':
            self.replenishFunction = self._rJuncal
            self.subactionsFunction = self._sJuncal
            self.costTrabajadores  = 1
            self.units             = 0
            self.material          = 'junco'
        if name == 'Pesca':
            self.replenishFunction = self._rPesca
            self.subactionsFunction = self._sPesca
            self.costTrabajadores  = 1
            self.units             = 0
            self.material          = 'comida'
        if name == 'Semilla de cereales':
            self.replenishFunction = self._rSemillaCereales
            self.subactionsFunction = self._sSemillaCereales
            self.costTrabajadores  = 1
        if name == 'Jornalero':
            self.replenishFunction = self._rJornalero
            self.subactionsFunction = self._sJornalero
            self.costTrabajadores  = 1
        if name == 'Labranza':
            self.replenishFunction = self._rLabranza
            self.subactionsFunction = self._sLabranza
            self.costTrabajadores  = 1
        if name == 'Lugar de encuentro':
            self.replenishFunction = self._rLugarEncuentro
            self.subactionsFunction = self._sLugarEncuentro
            self.costTrabajadores  = 1
        if name == 'Arboleda_3':
            self.replenishFunction = self._rArboleda_3
            self.subactionsFunction = self._sArboleda_3
            self.costTrabajadores  = 1
            self.units             = 0
            self.material          = 'madera'
        if name == 'Yacimiento_3':
            self.replenishFunction = self._rYacimiento_3
            self.subactionsFunction = self._sYacimiento_3
            self.costTrabajadores  = 1
            self.units             = 0
            self.material          = 'adobe'
        

#    def applyAction(self, game, params):
#        self.applyFunction(game, params)
        
        
    def applyReplenish(self):
        self.replenishFunction()
        
        
    def getSubactionsList(self):
        self.subactionsFunction()
        
#    # Funciones de acciones
#    def _fMina(action, game, params=None):
#        cp = game.currentPlayer
#        cp.reserva['adobe'] += action.units
#        action.units = 0
#        cp.trabajadoresDispo -= action.costTrabajadores
#        action.ocupada = True
#        
#    def _fPesca(action, game, params=None):
#        cp = game.currentPlayer
#        cp.reserva['comida'] += action.units
#        action.units = 0
#        cp.trabajadoresDispo -= action.costTrabajadores
#        action.ocupada = True
#        
#    def _fJornalero(action, game, params=None):
#        #TODO: Aciones que se disparan al usar jornalero
#        cp = game.currentPlayer
#        cp.reserva['comida'] += 2
#        cp.trabajadoresDispo -= action.costTrabajadores
#        action.ocupada = True
#        
#    def _fSemillaCereales(action, game, params=None):
#        cp = game.currentPlayer
#        cp.reserva['cereales'] += 1
#        cp.reservaTotal['cereales'] += 1
#        cp.trabajadoresDispo -= action.costTrabajadores
#        action.ocupada = True
#        
#    def _fBosque(action, game, params=None):
#        cp = game.currentPlayer
#        cp.reserva['madera'] += action.units
#        action.units = 0
#        cp.trabajadoresDispo -= action.costTrabajadores
#        action.ocupada = True
#        
#    def _fArboleda_3(action, game, params=None):
#        cp = game.currentPlayer
#        cp.reserva['madera'] += action.units
#        action.units = 0
#        cp.trabajadoresDispo -= action.costTrabajadores
#        action.ocupada = True
#        
#    def _fJuncal(action, game, params=None):
#        cp = game.currentPlayer
#        cp.reserva['junco'] += action.units
#        action.units = 0
#        cp.trabajadoresDispo -= action.costTrabajadores
#        action.ocupada = True
#        
#    def _fYacimiento_3(action, game, params=None):
#        cp = game.currentPlayer
#        cp.reserva['adobe'] += action.units
#        action.units = 0
#        cp.trabajadoresDispo -= action.costTrabajadores
#        action.ocupada = True
#        
#    def _fLabranza(action, game, params):
#        # Params:  casilla en la que pone el campo. Ej: params = (1,3)
#        casilla = params
#        cp = game.currentPlayer
#        cp.granja[casilla] = 2
#        cp.sembrado[casilla] = {'type':'', 'units':0}
#        cp.trabajadoresDispo -= action.costTrabajadores
#        action.ocupada = True
#        
#    def _fLugarEncuentro(action, game, params):
#        # Params: lista de 2 elementos
#        #  Quiere el token: boolean
#        #  TODO:Carta que quiere bajar
#        cp = game.currentPlayer
#        game.dealer = game.turn
#        cp.trabajadoresDispo -= action.costTrabajadores
#        action.ocupada = True
#        
#    def _fAmpliarGranja(action, game, params=None):
#        # listHabs:     lista de casillas donde poner la habitacion
#        # listEstablos: idem pero para establos
#        cp = game.currentPlayer
#        listHabs, listEstablos = params
#        for hab in listHabs:
#            cp.granja[hab] = 1
#            cp.reserva[cp.materialCasa] -= 5
#            cp.reserva['junco'] -= 2
#        for establo in listEstablos:
#            if cp.granja[establo] == 3:
#                # Si es un pasto (3), establo vallado (5)
#                cp.granja[establo] = 5
#            else:
#                # Si no habia nada, establo (4)
#                cp.granja[establo] = 4
#            cp.reserva['madera'] -= 2
#        cp.trabajadoresDispo -= action.costTrabajadores
            
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
    def _sYacimiento_3(self):
        pass
    def _sPesca(self):
        pass
    def _sBosque(self):
        pass
    def _sArboleda_3(self):
        pass
    def _sJuncal(self):
        pass
    def _sJornalero(self):
        pass
    def _sSemillaCereales(self):
        pass
    def _sLabranza(self):
        pass
    def _sLugarEncuentro(self):
        pass    
        
    def __str__(self):
        s = self.name
        if hasattr(self, 'units'):
            s += ' --> %d %s(s)' % (self.units, self.material)
        return s
