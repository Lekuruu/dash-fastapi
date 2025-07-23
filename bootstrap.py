
import argparse
import uvicorn
import os

def main() -> None:
    parser = argparse.ArgumentParser(description='Boot a Dash server')
    parser.add_argument('-a', '--address', action='store', default='0.0.0.0', help='Dash address')
    parser.add_argument('-p', '--port', action='store', help='Dash port', default=3000, type=int)
    parser.add_argument('-c', '--config', action='store', help='Config file path')
    parser.add_argument('-r', '--reload', action='store_true', help='Enable auto-reload')
    args = parser.parse_args()

    os.environ['DASH_CONFIG'] = args.config or 'config.py'
    os.environ['DASH_HOST'] = args.address
    os.environ['DASH_PORT'] = f'{args.port}'

    uvicorn.run(
        'dash.server:api',
        host=args.address,
        port=args.port,
        reload=args.reload,
        server_header=False,
        log_config=None
    )

if __name__ == '__main__':
    main()
