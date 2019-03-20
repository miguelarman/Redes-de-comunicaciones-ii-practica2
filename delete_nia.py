from securebox_requests import *
import sys

if (len(sys.argv) < 2):
    print('Introduce los nias a borrar')
    exit()

for nia in sys.argv[1:]:
    ret = user_delete(nia, verbose=True)
    print(ret)
