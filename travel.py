
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

    def print_stats(self):
        print "Number of counties:", self.count() 
        by_state = {}

        for c in self._ctys:
            try:
                by_state[c[1]] += 1
            except KeyError:
                by_state[c[1]] = 1

        print "Number of states:", len(by_state.keys())

        for state, count in sorted(by_state.items(), key=lambda x: x[1], reverse=True):
            print "%s: %d" % (state, count)
