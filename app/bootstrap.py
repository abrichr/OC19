import os
from pprint import pformat

from app import db
from app.models import User, Project


def maybe_bootstrap_db():
    have_admin = bool(User.query.filter_by(is_superadmin=True).count())
    print('maybe_bootstrap_db() have_admin:', have_admin)
    admin_email = os.environ.get('ADMIN_EMAIL')
    admin_password = os.environ.get('ADMIN_PASSWORD')
    if all((not have_admin, admin_email, admin_password)):
        bootstrap_db(admin_email, admin_password)
        return True
    else:
        print('Aborting')
        return False


def bootstrap_db(admin_email, admin_password):
    print('bootstrap_db()')
    user = User(
        email=admin_email,
        first_name='Admin',
        last_name='',
        password=admin_password,
        is_superadmin=True
    )
    db.session.add(user)
    db.session.flush()
    print('Inserted user:', pformat(vars(user)))

    user_by_email = {}
    user_dicts = [
        {'email': 'obenfine@gmail.com',
         'first_name': 'Ben',
         'last_name': 'Fine',
         'password': b'$2b$12$SV.ZQOUZPLwXEGV6VBnqJOpvOMRPd5sf6XXjJPeN/OcL2oCdOq04e'},
        {'email': 'pz.cehn@mail.utoronto.ca',
         'first_name': 'Paul',
         'last_name': 'Chen',
         'password': b'$2b$12$Fkrx9FaeQCbv.5MFDhNyauJbEOUvUe6rNhoocFNjrB.4U3Uh1WEae'},
        {'email': 'awhitehead@klick.com',
         'first_name': 'Alf',
         'last_name': 'Whitehead',
         'password': b'$2b$12$uZo.evBQerTMTzksmSgSJOuYxNrYHrpAaRwJ3vyvdE1E7u5l/qtWm'}
    ]
    for user_dict in user_dicts:
        user = User(**user_dict)
        db.session.add(user)
        db.session.flush()
        user_id = user.id
        print(
            'bootstrap_db() inserted user:',
            pformat(vars(user)),
            'user_id:', user_id
        )
        user_by_email[user.email] = user
    projects = [
        {
            "title": "COVID-19 Data Viz to help flatten the curve",
            "description": "COVID-19 Threatens to overwhelm our healthcare system. We need to act decisively now to #flattenthecurve. Join data scientists, engineers and designers in building visualizations help inform Ontario decision makers. ",
            "needed": "Full stack developers, data scientists, control theory expertise",
            "provided": "Leading local epidemiologist groups are already connected providing guidance. ",
            "created_by_user": user_by_email['obenfine@gmail.com'],
            "users_joined": [user_by_email['obenfine@gmail.com']]
        }
    ]
    for project in projects:
        project = Project(**project)
        db.session.add(project)
        db.session.flush()
        project_id = project.id
        print(
            'bootstrap_db() inserted project:', pformat(vars(project)),
            'project_id:', project_id
        )

    db.session.commit()
