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
