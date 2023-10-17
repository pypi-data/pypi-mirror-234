#from tempfile import NamedTemporaryFile
from flask      import Flask, request
from subprocess import check_output

from docker     import errors, from_env

def cis_daemon(dc, url, rec):
  # Create a Docker container within the container
  cont = dc.containers.create('innovanon/cis-build', command='/bin/sh')
  try:
    # Run git clone command within the container
    git_cmd = f'git clone{"--recursive" if rec else ""} {url} repo'
    cis_cmd = f'if [ -f .cis/run ] ; then .cis/run ; else cis ; fi'
    all_cmd = f'{git_cmd} && cd repo && {cis_cmd}'

    output = cont.exec_run(all_cmd)
    status = output.exit_code
    status = 200 if status == 0 else 204

    return output.output.decode('utf-8'), status
  except errors.APIError as e:
    # Handle Docker API errors
    return str(e), 500
  except Exception as e:
    # Handle other excpetions (e.g., command execution errors)
    return str(e), 400

  finally: cont.remove()

def create_app(dc):
  app = Flask(__name__)

  @app.route('/git', methods=['GET'])
  def upload():
    url  = request.args.get('url')
    rec  = request.args.get('recursive', True)
    print(f'url: {url}, rec: {rec}')
    return cis_daemon(dc, url, rec)#, 200

  return app

def start_server(host="0.0.0.0", port=34567, *args, **kwargs):
  dc  = from_env()
  app = create_app(dc, **kwargs)
  app.run(debug=True, host=host, port=port, *args)

# https://www.easydevguide.com/posts/curl_upload_flask

