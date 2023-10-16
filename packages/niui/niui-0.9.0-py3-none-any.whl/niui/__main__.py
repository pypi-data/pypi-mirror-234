import argparse
from pathlib import Path
from flask import Flask, make_response, render_template, request, Response
from logging.config import dictConfig
from typing import List, Any, Dict
from .api.types import Setup, ProjectInfo, ConfigJson, Project, ConfigWithMeta, Config, FirmwareInfo, BoxInfo
from .api.files.json import find_json_files
from .api.can.bus import open_bus

app = Flask(__name__)

#
# Configre logger.
#
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '%(levelname)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

#
# Global setup.
#
SETUP: Setup = {
    "non_public": False,
    "json_files": [],
    "workdir": Path.home() / 'NIMU',
    "port": 8402,
    "debug": False,
    "channel": 'PCAN_USBBUS1',
    "interface": 'pcan',
    "bitrate": 1000000,
    "logger": None,
}

def setup() -> None:
    open_bus(SETUP)
    app.logger.info("Scanning for configuration definition JSON-files...")
    SETUP["json_files"] = find_json_files(SETUP["workdir"] / 'Configurations')
    app.logger.info(f'Found {len(SETUP["json_files"])} JSON-files.')
    SETUP["workdir"].mkdir(parents=True, exist_ok=True)
    SETUP["logger"] = app.logger
    app.logger.info(f'Nimu UI is now available in \033[1;33mhttp://localhost:{SETUP["port"]}\033[0m')

#
# Define routes.
#
@app.route('/index.css', methods=['GET'])
def index_css() -> Response:
    response = make_response(render_template('index.css'))
    response.headers['Content-Type'] = 'text/css; charset=utf-8'
    return response


@app.route('/index.js', methods=['GET'])
def index_js() -> Response:
    response = make_response(render_template('index.js'))
    response.headers['Content-Type'] = 'text/javascript; charset=utf-8'
    return response


@app.route('/api/boxes', methods=['GET'])
def boxes() -> List[BoxInfo]:
    from .api.routes.boxes import index
    return index(SETUP)


@app.route('/api/firmwares', methods=['GET'])
def firmwares() -> List[FirmwareInfo]:
    from .api.routes.firmwares import index
    return index(SETUP)


@app.route('/api/firmwares/<id>', methods=['GET', 'POST'])
def firmware(**args: str) -> FirmwareInfo:
    from .api.routes.firmwares import get, write
    if request.method == 'POST':
        return write(SETUP, int(args['id']), request.get_json().get('box_id'))
    return get(SETUP, int(args['id']))


@app.route('/api/firmwares', methods=['POST'])
def upload_firmware() -> Dict[str, ConfigJson]:
    from .api.routes.firmwares import create
    return create(SETUP, request.get_json())


@app.route('/api/configurables', methods=['GET'])
def configurables() -> Dict[str, ConfigJson]:
    from .api.routes.configurables import index
    return index(SETUP)


@app.route('/api/projects', methods=['GET', 'POST'])
def projects() -> List[ProjectInfo]:
    from .api.routes.projects import index, create
    if request.method == 'POST':
        return create(SETUP, request.get_json())
    return index(SETUP)


@app.route('/api/projects/<id>', methods=['GET'])
def project(**args: str) -> Project:
    from .api.routes.projects import get
    return get(SETUP, int(args['id']))


@app.route('/api/configurations/scan', methods=['POST'])
def configuration_scan(**args: str) -> Dict[int, Any]:
    from .api.routes.configurations import scan
    json = request.get_json()
    return scan(SETUP, json.get('box_id'), json.get('item_ids'))


@app.route('/api/configurations/<id>', methods=['GET', 'POST'])
def configuration(**args: str) -> List[ConfigWithMeta]:
    from .api.routes.configurations import index, create
    if request.method == 'POST':
        return create(SETUP, int(args['id']), request.get_json())
    return index(SETUP, int(args['id']))


@app.route('/api/configurations/<id>/<version>/write', methods=['POST'])
def configuration_version_write(**args: str) -> Config:
    from .api.routes.configurations import write
    json = request.get_json()
    return write(SETUP, json.get('box_id'), json.get('config'))


@app.route('/api/configurations/<id>/<version>', methods=['GET', 'PUT'])
def configuration_version(**args: str) -> Config:
    from .api.routes.configurations import get, update
    if request.method == 'PUT':
        return update(SETUP, int(args['id']), int(args['version']),
                      request.get_json())
    return get(SETUP, int(args['id']), int(args['version']))


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(**args: List[Any]) -> str:
    return render_template('index.html')


#
# Argument parser.
#
def parse_args() -> None:
    parser = argparse.ArgumentParser(
        prog="python3 server.py",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="NIMU configuration server",
        argument_default=argparse.SUPPRESS
    )
    parser.add_argument('--non-public', action='store_true', default=False,
                        help='Show also non-public configuartion items.')
    parser.add_argument('--debug', action='store_true', default=False,
                        help='Run in development mode.')
    parser.add_argument('--quiet', action='store_true', default=False,
                        help='Do not display individual packets.')
    parser.add_argument('--interface', default='pcan',
                        help='CAN bus interface to use for communication.')
    parser.add_argument('--channel', default='PCAN_USBBUS1',
                        help='CAN bus channel to use for communication.')
    parser.add_argument('--bitrate', type=int, default=1000000,
                        help='CAN bus bitrate.')
    parser.add_argument('--project-dir', type=str, default=Path.home() / 'NIMU',
                        help='Project directory where to find configurations and firmwares.')
    parsed = parser.parse_args()

    SETUP["non_public"] = parsed.non_public
    SETUP["quiet"] = parsed.quiet
    SETUP["debug"] = parsed.debug
    SETUP["interface"] = parsed.interface
    SETUP["channel"] = parsed.channel
    SETUP["bitrate"] = parsed.bitrate
    SETUP["workdir"] = Path(parsed.project_dir)


#
# Launch the server.
#
if __name__ == '__main__':
    parse_args()
    setup()
    app.run(debug=True, use_debugger=False, use_reloader=False, port=SETUP["port"])
# debug purposes
#else:
#    setup()
