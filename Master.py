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

