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
