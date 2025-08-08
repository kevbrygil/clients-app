import falcon


def validate_scope_admin(req, resp, resource, params):
    try:
        try:

            role = req.context['user'].get('role_name', '')
            if role.lower() != "admin":
                raise Exception("You must be a admin.")
        except Exception as exc:
            raise exc
    except Exception as exc:
        challenges = ['Token type="jwt"']
        description = ('{}'.format(exc),
                       'Please, contact the administrator.')
        raise falcon.HTTPUnauthorized('Authentication required',
                                      description,
                                      challenges,
                                      href='http://docs.example.com/auth')


def validate_scope_viewer(req, resp, resource, params):
    try:
        try:

            role = req.context['user'].get('role_name', '')
            if role.lower() != "viewer":
                raise Exception("You must be a viewer.")
        except Exception as exc:
            raise exc
    except Exception as exc:
        challenges = ['Token type="jwt"']
        description = ('{}'.format(exc),
                       'Please, contact the administrator.')
        raise falcon.HTTPUnauthorized('Authentication required',
                                      description,
                                      challenges,
                                      href='http://docs.example.com/auth')


def validate_scope_both(req, resp, resource, params):
    try:
        try:

            role = req.context['user'].get('role_name', '')
            if role.lower() != "viewer" and role.lower() != "admin":
                raise Exception("You must be a admin or viewer.")
        except Exception as exc:
            raise exc
    except Exception as exc:
        challenges = ['Token type="jwt"']
        description = ('{}'.format(exc),
                       'Please, contact the administrator.')
        raise falcon.HTTPUnauthorized('Authentication required',
                                      description,
                                      challenges,
                                      href='http://docs.example.com/auth')