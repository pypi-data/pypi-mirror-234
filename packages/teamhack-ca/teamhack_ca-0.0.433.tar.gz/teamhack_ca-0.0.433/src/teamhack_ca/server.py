# /usr/bin/env python3
# TODO escape file path names

from flask            import Flask, jsonify, request
from subprocess       import run
#from teamhack_db.sql  import insert
#from teamhack_db.util import get_name, get_record_type

def create_app():
  app = Flask(__name__)
  #api = Api(app)

  def keypair(name):
    with open('private/%s.key' % (name,), 'r') as f: key = f.read()
    with open(  'certs/%s.crt' % (name,), 'r') as f: crt = f.read()
    return {
      'key':  key,
      'cert': cert,
    }

  @app.route('/intermediate_ca', methods=['POST'])
  def intermediate_ca():
    """
    Create Intermediate CA Certificate/Key Pair
    """
    data = request.get_json(force=True)

    if 'name' not in data: return '', 404
    name = data['name']

    run(['bin/intermediate_ca', name], check=True)

    return keypair(name)


  @app.route('/site', methods=['POST'])
  def site():
    """
    Create Leaf Certificate/Key Pair
    """
    data = request.get_json(force=True)

    if 'ca' not in data: return '', 404
    ca   = data['ca']

    if 'site' not in data: return '', 404
    site = data['site']

    run(['bin/site', ca, site], check=True)

    return keypair(name)

  @app.route('/retrieve', methods=['POST'])
  def retrieve():
    """
    Retrieve Certificate/Key Pair
    """
    data = request.get_json(force=True)

    if 'name' not in data: return '', 404
    name = data['name']

    return keypair(name)

  @app.route('/revoke', methods=['POST'])
  def revoke():
    """
    Revoke Certificate
    """
    data = request.get_json(force=True)

    if 'ca' not in data: return '', 404
    ca   = data['ca']

    if 'site' not in data: return '', 404
    site = data['site']

    run(['bin/revoke', ca, site], check=True)

    return keypair(name)

  return app

def start_server(host="0.0.0.0", port=5002, *args, **kwargs):
  # TODO init_ca
  # TODO root_ca
  run(['bin/init_ca'], check=True)
  run(['bin/root_ca'], check=True)
  app = create_app()
  app.run(debug=True, host=host, port=port, *args, **kwargs)

