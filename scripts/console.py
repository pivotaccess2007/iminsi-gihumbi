import os, sys
import code
import readline
import rlcompleter


objects = {}
readline.set_completer(rlcompleter.Completer(objects).complete)
readline.parse_and_bind("tab:complete")


def rwabugiri_main(argv):
  pcks  = os.path.join(os.getcwd(), 'packages')
  env   = os.environ
  env.update({'PYTHONPATH': pcks})
  argl  = argv
  argl.append(env)
  code.interact(local=objects)
  return os.execlpe('python', *argl)

if __name__ == '__main__':
  bottom  = sys.exit(rwabugiri_main(sys.argv))

