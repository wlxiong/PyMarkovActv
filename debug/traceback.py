import sys, traceback

def print_exc_plus():
    """
    Print the usual traceback information, followed by a listing of all the
    local variables in each frame.
    """
    
    # traceback.print_exc()
    
    tb = sys.exc_info()[2]
    stack = []

    while tb:
        stack.append(tb.tb_frame)
        tb = tb.tb_next
        
    print "\n _______Debug (backtracks)_______ \n (locals by frame, innermost last)"

##     tb = sys.exc_info()[2]
##     while 1:
##         if not tb.tb_next:
##             break
##         tb = tb.tb_next
##     stack = []
##     f = tb.tb_frame
##     while f:
##         stack.append(f)
##         f = f.f_back
##     stack.reverse()
##     traceback.print_exc()
##     print "Locals by frame, innermost last"
    
    if stack:
        stack.pop(0)
        
    for frame in stack:
        if frame.f_code.co_name == '<module>':
            continue
        print
        print "File \"%s\", line %s, in %s" % (frame.f_code.co_filename,
                                             frame.f_lineno,
                                             frame.f_code.co_name)
        for key, value in frame.f_locals.items():
            print " .%s = " % key, 
            #We have to be careful not to cause a new error in our error
            #printer! Calling str() on an unknown object could cause an
            #error we don't want.
            try:
                print value
            except:
                print "<ERROR WHILE PRINTING VALUE>"
                
    print "\n _______Debug (backtracks)_______ \n          (end of debug)\n"

if __name__ == '__main__':
    " Recipe 52215: Get more information from tracebacks (Python) "
    try:
        if len(sys.argv) < 2:
            sys.stderr.write(' trackbacks: no input file\n')
        elif sys.argv[1] == 'tb.py':
            print __file__, sys.argv[1]
            sys.stderr.write(' trackbacks: cannot debug myself\n')
        else:
            execfile(sys.argv[1])
    except:
        print_exc_plus()
