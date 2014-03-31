
import tiedye
import flask
import weakref
import functools

from tiedye import ProviderSet


config_interfaces = weakref.WeakValueDictionary()


class ConfigType(type):

    def __getattr__(self, key):
        try:
            return config_interfaces[key]
        except KeyError:
            interface = Config()
            interface.key = key
            config_interfaces[key] = interface
            return interface


class Config(object):
    __metaclass__ = ConfigType


class GlobalProviders(ProviderSet):

    def __init__(self, app):
        self.app = app

    @ProviderSet.provide(Config)
    def get_config_setting(self, setting_interface):
        try:
            return self.app.config[setting_interface.key]
        except KeyError:
            raise tiedye.DependencyError(
                "No setting named %r" % setting_interface.key
            )


class RequestProviders(ProviderSet):

    def __init__(self, app):
        self.app = app

    @ProviderSet.provide(flask.Flask)
    def get_application(self, Flask):
        return flask.current_app

    @ProviderSet.provide(flask.Request)
    def get_request(self, Request):
        return flask.request


def init_tiedye(flask_app, global_provider_sets=[], request_provider_sets=[]):
    tiedye_app = tiedye.Application()

    @flask_app.before_first_request
    def init_global_injector():
        global_providers = GlobalProviders(flask.current_app)
        flask.current_app.global_injector = tiedye_app.make_injector(
            global_providers,
            *global_provider_sets
        )

    @flask_app.before_request
    def init_request_injector():
        request_providers = RequestProviders(flask.current_app)
        flask.g.request_injector = flask_app.global_injector.specialize(
            request_providers,
            *request_provider_sets
        )

    def inject(**kwargs):
        def register(func):
            @functools.wraps(func)
            def inject_wrapper(*args, **kwargs):
                # Do partial binding of the function with the global
                # injector, which will cause us to share globally-provided
                # objects between requests.
                bound = flask_app.global_injector.bind(func)
                # Now complete the binding with the request injector and
                # make a call.
                return flask.g.request_injector.call(bound, *args, **kwargs)

            tiedye_app.dependencies(func, **kwargs)

            return inject_wrapper

        return register

    flask_app.inject = inject

    return tiedye_app
