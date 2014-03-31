
import flask
from flask.ext import tiedye as flask_tiedye
import tiedye


RequestStash = tiedye.make_interface("RequestStash")


class RequestProviders(tiedye.ProviderSet):

    @tiedye.ProviderSet.provide(
        RequestStash,
        initial=flask_tiedye.Config.INITIAL_REQUEST_STASH,
    )
    def get_request_stash(self, RequestStash, initial):
        return dict(initial)


app = flask.Flask(__name__)
app.config['INITIAL_REQUEST_STASH'] = {"hi": True}
flask_tiedye.init_tiedye(app, request_provider_sets=[RequestProviders()])


@app.route("/")
@app.inject(stash=RequestStash)
def home(stash):
    return "Stash is %r" % stash


if __name__ == "__main__":
    app.run(debug=True)
