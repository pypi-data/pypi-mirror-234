import sys
import logging
import importlib
#sys.path.append("C:\\dev\\ml\\ml-py\\venv\\Lib\\site-packages")

logger = logging.getLogger('ml_py')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

#import marcuslion

if __name__ == '__main__':
    logger.info('Start marcuslion test')
    try:
        #pathToModules = "c:\\dev\\ml\\ml-py\\venv\\lib\\site-packages\\"
        #sys.path.append(pathToModules)
        #py_ml_lib = __import__("marcuslion")
        #mod = importlib.import_module(pathToModules + "marcuslion")
        #import py-ml-lib
        import marcuslion as ml

        a = ml.add_one(5)
        print("call add one ", a)

        ml.openml()
    except Exception as e:
        #print(e, '|', e.errno, '|', e.value, '|', e.args)
        print("Exception ", e)