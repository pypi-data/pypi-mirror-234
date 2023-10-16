from unitgrade.version import __version__
import argparse
import os
import logging
import sys
from unitgrade.dashboard.app import mkapp


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Unitgrade dashboard"
            "https://lab.compute.dtu.dk/tuhe/unitgrade"
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument('dir', nargs='?', default=os.getcwd(), help="Directory to listen in (default to current directory)")
    parser.add_argument("-p", "--port", default=5000, help="port to run server on")
    parser.add_argument("--host",default="127.0.0.1", help="host to run server on (use 0.0.0.0 to allow access from other hosts)",)
    parser.add_argument("--debug", action="store_true", help="debug the server")
    parser.add_argument("--version", action="store_true", help="print version and exit")

    args = parser.parse_args()
    if args.version:
        print(__version__)
        exit(0)

    app, socketio, closeables = mkapp(base_dir=args.dir)

    green = "\033[92m"
    end = "\033[0m"
    log_format = green + "pyxtermjs > " + end + "%(levelname)s (%(funcName)s:%(lineno)s) %(message)s"
    logging.basicConfig(
        format=log_format,
        stream=sys.stdout,
        level=logging.DEBUG if args.debug else logging.INFO,
    )
    url = f"http://{args.host}:{args.port}"
    logging.info(f"Starting unitgrade dashboard version {__version__}")
    logging.info(f"Serving dashboard on: {url}")

    debug = False
    os.environ["WERKZEUG_DEBUG_PIN"] = "off"

    import webbrowser
    webbrowser.open(url)
    socketio.run(app, debug=debug, port=args.port, host=args.host) # , allow_unsafe_werkzeug=True )
    for c in closeables:
        c.close()
    sys.exit()

if __name__ == "__main__":
    main()