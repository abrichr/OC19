from flask import redirect, url_for

from app.bootstrap import maybe_do_bootstrap
from app.admin import admin_blueprint


@admin_blueprint.route('/bootstrap', methods=['GET', 'POST'])
def bootstrap():
    maybe_do_bootstrap()
    return redirect(url_for('home.main'))
