import os

from app import bcrypt, mongo


def maybe_do_bootstrap():
    user = mongo.db.users.find_one({'is_superadmin': True})
    print('maybe_do_bootstrap() existing user:', user)
    admin_email = os.environ.get('ADMIN_EMAIL')
    admin_password = os.environ.get('ADMIN_PASSWORD')
    if all((not user, admin_email, admin_password)):
        do_bootstrap(admin_email, admin_password)


def do_bootstrap(admin_email, admin_password):
    print('do_bootstrap()')
    user = mongo.db.users.insert({
        'email': admin_email,
        'name': 'Admin',
        # XXX TODO: salt
        'password': bcrypt.generate_password_hash(admin_password),
        'authenticated': False,
        'is_superadmin': True
    })
    print('do_bootstrap() inserted user:', user)
    user_id_by_email = {}
    users = [
        {'email': 'obenfine@gmail.com',
         'name': 'Ben Fine',
         'password': b'$2b$12$SV.ZQOUZPLwXEGV6VBnqJOpvOMRPd5sf6XXjJPeN/OcL2oCdOq04e'},
        {'email': 'pz.cehn@mail.utoronto.ca',
         'name': 'Paul Chen',
         'password': b'$2b$12$Fkrx9FaeQCbv.5MFDhNyauJbEOUvUe6rNhoocFNjrB.4U3Uh1WEae'},
        {'email': 'awhitehead@klick.com',
         'name': 'Alf Whitehead',
         'password': b'$2b$12$uZo.evBQerTMTzksmSgSJOuYxNrYHrpAaRwJ3vyvdE1E7u5l/qtWm'}
    ]
    for user in users:
        user_id = mongo.db.users.insert_one(user)
        print('do_bootstrap() inserted user:', user, 'user_id:', user_id)
        user_id_by_email[user['email']] = user['_id']
    projects = [
        {
            "title": "COVID-19 Data Viz to help flatten the curve",
            "description": "COVID-19 Threatens to overwhelm our healthcare system. We need to act decisively now to #flattenthecurve. Join data scientists, engineers and designers in building visualizations help inform Ontario decision makers. ",
            "needed": "Full stack developers, data scientists, control theory expertise",
            "provided": "Leading local epidemiologist groups are already connected providing guidance. ",
            "user_id": user_id_by_email['obenfine@gmail.com'],
            "users": [user_id_by_email['obenfine@gmail.com']]
        }
    ]
    for project in projects:
        project_id = mongo.db.projects.insert_one(project)
        print(
            'do_bootstrap() inserted project:', project,
            'project_id:', project_id
        )
