"""
    Digits game
    based on pys60_gametemplate:
    https://github.com/howdyworld/pys60_gametemplate
"""
import os
import sys
import e32

# dir path where game package located
PACKAGE_LOC = "E:\\Data\\python"
if PACKAGE_LOC not in sys.path:
    sys.path.append(PACKAGE_LOC)

try:
    from digits import game
    game.Game().run()
except Exception, e:
    #import appuifw
    #appuifw.note(u"Exception: %s" % (e))
    print e

