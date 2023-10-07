import os
import sys
from pathlib import Path
from typing import List, Dict, Tuple, Callable
import yaml
import eventlet
from loguru import logger
from eventlet import wsgi
from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException
from eventlet.greenio.base import GreenSocket
from eventlet.greenthread import GreenThread


class PonApp:
    """Implements a WSGI application for managing your favorite movies."""

    def __init__(self):
        from pon.web.entrance import url_map
        self.url_map = url_map

    def dispatch_request(self, request: Request):
        """Dispatches the request."""
        # return Response('Hello World!')
        adapter = self.url_map.bind_to_environ(request.environ)
        try:
            endpoint, values = adapter.match()
            return endpoint(request, **values)
            # return getattr(self, endpoint.__name__)(request, **values)
            # return getattr(self, f'on_{endpoint}')(request, **values)
        except HTTPException as error:
            return error

    def wsgi_app(self, environ: Dict, start_response: Callable):
        """WSGI application that processes requests and returns responses."""
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def __call__(self, environ: Dict, start_response: Callable):
        """The WSGI server calls this method as the WSGI application."""
        return self.wsgi_app(environ, start_response)


class EventletAPIRunner:
    def __init__(self) -> None:
        self.put_patch()

    def put_patch(self) -> None:
        import eventlet
        eventlet.monkey_patch()  # noqa (code before rest of imports)

    def load_service_cls_list(self, services: Tuple[str]) -> List[type]:
        cwd: Path = Path(os.getcwd())
        sys.path.append(str(cwd))

        service_cls_list: List[type] = []

        for service in services:
            items: List[str] = service.split(':')
            if len(items) == 1:
                module_name, service_class_name = items[0], None
            elif len(items) == 2:
                module_name, service_class_name = items
            else:
                raise Exception(f'错误的 service 格式: {service}')

            __import__(module_name)

            module = sys.modules[module_name]

            service_cls = getattr(module, service_class_name)

            service_cls_list.append(service_cls)

        return service_cls_list

    def load_config(self, config_filepath: Path):
        with open(config_filepath, 'r', encoding='utf-8') as file:
            config: Dict[str, Dict] = yaml.load(
                file.read(), Loader=yaml.Loader)
        self.amqp_uri = config['AMQP_URI']

    def run(self, services: Tuple[str], config_filepath: Path):
        self.load_config(config_filepath)
        # service_cls_list: List[type] = self.load_service_cls_list(services)
        self.load_service_cls_list(services)

        def create_app():
            """Application factory function that returns an instance of MovieApp."""
            app = PonApp()
            return app

        app = create_app()

        server_socket: GreenSocket = eventlet.listen(("0.0.0.0", 8000))

        # wsgi.server(server_socket, app)

        gt: GreenThread = eventlet.spawn(wsgi.server, server_socket, app)

        # gt.wait()
