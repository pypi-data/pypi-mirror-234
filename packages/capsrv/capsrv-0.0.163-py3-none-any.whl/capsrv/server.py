#from tempfile import NamedTemporaryFile
from flask import Flask, request
from subprocess import check_output
#from os import unlink

#def portscan_daemon(file):
def capsrv_daemon(cap):
  # /usr/bin/env
  #p = run(['nmap', '-A', '-sV', '--script=vulners/vulners.nse', '-p-', '-iL', '-', '-oX', '-'], stdin=file, stdout=PIPE)
  #p = run(['nmap', '-A', '-sV', '--script=vulners/vulners.nse', '-p-', '-iL', '-', '-oX', '-'], stdin=hosts.decode(), stdout=PIPE)
  #p = check_output(['nmap', '-A', '-sV', '--script=vulners/vulners.nse', '-p-', '-iL', '-', '-oX', '-'], input=hosts)
  p = check_output(['bin/recv-cap.sh'], input=cap)
  #p.check_returncode()
  #return p.stdout
  return p

def create_app():
  app = Flask(__name__)

  @app.route('/upload', methods=['PUT'])
  def upload():
    #file = NamedTemporaryFile()
    #try:
    #  file.write(request.get_data())
    #  file.flush()
    #  file.seek(0)
    #  return capsrv_daemon(file), 200
    #finally:
    #  file.close()
    #  #unlink(file.name)
    #data = request.get_data()
    #print(f'data: {data}')
    return capsrv_daemon(request.get_data())#, 200

  return app

def start_server(host="0.0.0.0", port=43415, *args, **kwargs):
  app = create_app(**kwargs)
  app.run(debug=True, host=host, port=port, *args)

# https://www.easydevguide.com/posts/curl_upload_flask

