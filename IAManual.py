class IAManual(object):
    def __init__(self):
        pass
    
    def nextMove(self, agricola):
        actions = agricola.getPossibleActions()
        for i, action in enumerate(actions):
            print str(i) + ' --> ' + str(action)
        decision = raw_input()
        return actions[int(decision)]

