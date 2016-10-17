
class TravelManager(object):
    def __init__(self, counties):
        self._ctys = counties

    def contains(self, *args):
        cntns = False
        try:
            county, state = args
            cntns = (county, state) in self._ctys
        except ValueError:
            ctys, states = zip(*self._ctys)
            cntns = args[0] in states
        return cntns

    def count(self, states=False):
        if states:
            ctys, sts = zip(*self._ctys)
            cnt = len(list(set(sts)))
        else:
            cnt = len(self._ctys)
        return cnt
