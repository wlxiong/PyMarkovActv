# Discrete choice model
import hashlib
import math

class Alternative(object):
    """ A basic class for choice alternatives. 
    """
    def __init__(self, name, coeff, utility, parent, volume=None):
        self.name, self.util, self.coeff = name, utility, coeff
        self.parent, self.children = parent, []
        self.volume = volume
        # add this alternative to the children list of its parent
        if self.parent != None:
            self.parent.add_child(self)
        # varables to be calculated
        self.mid_child_util = None
        self.inclusive_value = None
        self.choice_prob = None
    
    def __eq__(self, other):
        try:
            other.name
        except:
            return False
        else:
            return self.name == other.name
    
    def __repr__(self):
        if self.parent == None:
            return "%s(nil)" % (self.name)
        return "%s(%s)" % (self.name, self.parent)

    def __hash__(self):
        # return int(hashlib.md5(repr(self)).hexdigest(), 16)
        return hash(repr(self))
        
    def add_child(self, new_child):
        self.children.append(new_child)
        
    def calc_mid_child_util(self):
        if self.mid_child_util != None:
            return self.mid_child_util
        if len(self.children) == 0:
            self.mid_child_util = 0.0
        else:
            min_util = min( [ each_child.util for each_child in self.children ] )
            max_util = max( [ each_child.util for each_child in self.children ] )
            self.mid_child_util = (min_util + max_util)/2.0
        return self.mid_child_util
    
    def calc_inclusive_value(self):
        if self.inclusive_value != None:
            return self.inclusive_value
        if len(self.children) == 0:
            self.inclusive_value = self.util
        else:            
            mid_util = self.calc_mid_child_util()
            exp_sum_util = 0.0
            for each_child in self.children:
                exp_sum_util += math.exp(self.coeff * (each_child.calc_inclusive_value() - mid_util))
            log_sum_util = self.mid_child_util + math.log(exp_sum_util) / self.coeff
            self.inclusive_value = log_sum_util + self.util
        return self.inclusive_value
    
    def calc_choice_prob(self):
        if self.choice_prob != None:
            return self.choice_prob
        if self.parent == None:
            self.choice_prob = float('nan')
        else:
            mid_util = self.parent.calc_mid_child_util()
            log_sum_util = self.parent.calc_inclusive_value() - self.parent.util
            exp_sum_util = math.exp( (log_sum_util - mid_util) * self.parent.coeff)
            self.choice_prob = math.exp(self.parent.coeff * (self.calc_inclusive_value() - mid_util)) / exp_sum_util
        return self.choice_prob
        
    def calc_choice_volume(self):
        if self.volume != None:
            return self.volume 
        if self.parent == None:
            raise Exception('No enough data for calculate population! ')
        else:
            total_volume = self.parent.calc_choice_volume()
            self.volume = total_volume * self.calc_choice_prob()
        return self.volume
        
        
def main():
    a = Alternative('a', 0.005, 0.0, None, 2000)
    b = Alternative('b', 0.01, 5, a)
    c = Alternative('c', 0.01, 0, a)
    d = Alternative('d', 0.01, 5, a)
    e = Alternative('e', 0.05, 5, c)
    f = Alternative('f', 0.05, 5, c)
    
    print a.children
    print b.children
    print c.children
    print d.children
    print e.children
    print f.children
    
    print "calc_inclusive_value"
    print a.calc_inclusive_value()
    print b.calc_inclusive_value()
    print c.calc_inclusive_value()
    print d.calc_inclusive_value()
    print e.calc_inclusive_value()
    print f.calc_inclusive_value()
    
    print "calc_choice_prob"
    print  a.calc_choice_prob()
    print  b.calc_choice_prob()
    print  c.calc_choice_prob()
    print  d.calc_choice_prob()
    print  e.calc_choice_prob()
    print  f.calc_choice_prob()
    
    print "calc_population"
    print a.calc_choice_volume()
    print b.calc_choice_volume()
    print c.calc_choice_volume()
    print d.calc_choice_volume()
    print e.calc_choice_volume()
    print f.calc_choice_volume()
    
if __name__ == '__main__':
    main()
