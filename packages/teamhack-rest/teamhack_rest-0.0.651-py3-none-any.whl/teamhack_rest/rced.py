#! /usr/bin/env python
# Remote Code Execution Daemon

from flask          import Flask, jsonify, request
from flask_restful  import Resource, Api
from importlib      import import_module
from importlib.util import find_spec, LazyLoader, module_from_spec, spec_from_file_location
from inspect        import getmembers, getmodulename, isclass
from sys            import modules, path
from tempfile       import NamedTemporaryFile

path.append('uploads')

app = Flask(__name__)
api = Api(app)

def gensym(length=32, prefix="gensym_"):
  """
  generates a fairly unique symbol, used to make a module name,
  used as a helper function for load_module

  :return: generated symbol

  https://medium.com/@david.bonn.2010/dynamic-loading-of-python-code-2617c04e5f3f
  """
  alphabet = string.ascii_uppercase + string.ascii_lowercase + string.digits
  symbol = "".join([secrets.choice(alphabet) for i in range(length)])

  return prefix + symbol

def load_module(source, module_name=None, lazy=True):
  """
  reads file source and loads it as a module

  :param source: file to load
  :param module_name: name of module to register in sys.modules
  :return: loaded module

  https://medium.com/@david.bonn.2010/dynamic-loading-of-python-code-2617c04e5f3f
  """

  if module_name is None: module_name = gensym()

  spec = spec_from_file_location(module_name, source)
  """ https://stackoverflow.com/questions/32175693/python-importlibs-analogue-for-imp-new-module """
  if lazy: spec.loader = LazyLoader(spec.loader)
  module               = module_from_spec(spec)
  modules[module_name] = module
  spec.loader.exec_module(module)

  return module, module_name

def upload_file(file):
  path = NamedTemporaryFile(delete=False, dir="uploads", suffix='.py')
  path.write(file.encode())
  return path.name

class AddResource(Resource):
  def get(self, file): pass

  def post(self):
    """ https://www.appsloveworld.com/coding/flask/49/pythonflask-how-to-get-text-from-request-with-newlines?expand_article=1 """
    code              = request.get_data()
    code              = code.decode("ascii")
    assert(len(code.splitlines()) > 1)

    path              = upload_file(code)
    name              = getmodulename(path)
    assert name is not None

    module, name      = load_module(path, name) # , False)
    assert name is not None

    """ https://progr.interplanety.org/en/python-how-to-get-defined-classes-list-from-module-py-file/ """
    mems = getmembers(module, isclass)
    assert mems != []

    mems = [(cname, cobj) for cname, cobj in mems if issubclass(cobj, Resource) and cobj is not Resource]
    assert mems != []

    for cname, cobj in mems:
      rp = f'{name}.{cname}'
      api.add_resource(cobj, f'/{rp}')

    return jsonify({'name': name})

def start_server(conn):
  #n = f'{AddResource.__module__}.{AddResource.__name__}'
  #n = f'{AddResource.__name__}'
  n = f'{AddResource.__qualname__}'
  print(f'/{n}')
  api.add_resource(AddResource, f'/{n}')
  app.run(debug=True)

