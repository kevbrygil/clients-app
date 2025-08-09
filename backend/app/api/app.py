import falcon

from falcon_cors import CORS

from app.api.controllers.v1.auth import AuthResource, AuthenticationRefresh
from app.api.middlewares.token_auth import AuthMiddleware
from app.model import db_init, Session
from app.api.middlewares.session_db_manager import SQLAlchemySessionManager
from app.api.middlewares.json_translator import JSONTranslator
from app.api.middlewares.require_json import RequireJSON
from app.api.controllers.v1.user import User
from app.api.controllers.v1.ping import Ping
from app.api.controllers.v1.role import Role
from app.api.controllers.v1.customer import Customer, CustomerResource


def init_app():
    # Database initialization
    db_init()

    # Middlewares
    public_cors = CORS(
        allow_all_origins=True,
        allow_all_headers=True,
        allow_all_methods=True
    )
    middleware = [
        public_cors.middleware,
        RequireJSON(),
        JSONTranslator(),
        SQLAlchemySessionManager(Session)
    ]
    app = falcon.API(middleware=middleware)

    # API V1
    user = User()
    ping = Ping()
    auth = AuthResource()
    refresh = AuthenticationRefresh()
    role = Role()
    customer = Customer()
    customer_id = CustomerResource()

    # Routes

    app.add_route('/v1/users', user)
    app.add_route('/v1/ping', ping)
    app.add_route('/v1/roles', role)
    app.add_route('/v1/oauth/token', auth)
    app.add_route('/v1/oauth/token/refresh', refresh)
    app.add_route('/v1/customers', customer)
    app.add_route('/v1/customers/{uuid}', customer_id)

    return app
