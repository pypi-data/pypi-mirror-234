from flask            import Flask, jsonify, request
from teamhack_db.sql  import insert
from teamhack_db.util import get_name, get_record_type

def create_app(conn):
  app = Flask(__name__)
  #api = Api(app)

  def dispatch(data, hostname_recordtype_cb, hostname_cb, ip_cb):
    if 'host' in data and 'type' in data:
      host = data['host']
      host = get_name(host)
      rt   = data['type']
      rt   = get_record_type(rt)
      ret  = hostname_recordtype_cb(conn, host, rt)
      return ret
    if 'host' in data and 'type' not in data:
      host = data['host']
      host = get_name(host)
      ret  = hostname_cb(conn, host)
      return ret
    if 'inet' in data:
      addr = data['inet']
      ret  = ip_cb(conn, addr)
      return ret
    return '', 404

  @app.route('/create', methods=['POST'])
  def add():
    data = request.get_json(force=True)
    if 'host' not in data: return '', 404
    host = data['host']
    host = get_name(host)
    if 'type' not in data: return '', 404
    rt   = data['type']
    rt   = get_record_type(rt)
    if 'inet' not in data: return '', 404
    addr = data['inet']
    insert(conn, host, rt, addr)
    conn.commit()
    return '', 204

  @app.route('/retrieve', methods=['POST'])
  def retrieve():
    data = request.get_json(force=True)
    return dispatch(data, select_hostname_recordtype, select_hostname, select_ip)

  @app.route('/update', methods=['POST'])
  def update():
    # TODO
    return '', 404

  @app.route('/delete', methods=['POST'])
  def delete():
    data = request.get_json(force=True)
    return dispatch(data, drop_row_hostname_recordtype, drop_row_hostname, drop_row_ip)

  return app

def start_server(conn, host="0.0.0.0", port=5001, *args, **kwargs):
  app = create_app(conn)
  app.run(debug=True, host=host, port=port, *args, **kwargs)

