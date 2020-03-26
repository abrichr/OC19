from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property

from flask_login import UserMixin

from app import db, bcrypt


user_project_table = db.Table(
    'user_project',
    db.Column(
        'user_id',
        db.Integer,
        db.ForeignKey('project.id'),
        primary_key=True
    ),
    db.Column(
        'project_id',
        db.Integer,
        db.ForeignKey('user.id'),
        primary_key=True
    )
)


class User(db.Model, UserMixin):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    confirmation = db.Column(db.Boolean)
    is_superadmin = db.Column(db.Boolean)
    _password = db.Column(db.String)
    projects_created = db.relationship('Project', cascade='all,delete')
    projects_joined = db.relationship(
        'Project',
        secondary=user_project_table,
        #back_populates="users_joined"
        backref=db.backref('users_joined'),
        cascade='all,delete'
    )

    @property
    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, plaintext):
        self._password = (
            bcrypt.generate_password_hash(plaintext).decode('utf-8')
        )

    def check_password(self, plaintext):
        return bcrypt.check_password_hash(self.password, plaintext)

    def get_id(self):
        return self.email

    def __repr__(self):
        return 'User {}: {}'.format(self.id, self.full_name)


def info(label, description=None):
    return {'label': label, 'description': description}


class Project(db.Model):

    __tablename__ = 'project'

    id = db.Column(db.Integer, primary_key=True)
    created_by_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by_user = db.relationship(
        'User', back_populates='projects_created'
    )
    # users_joined created by backref in User
    title = db.Column(
        db.String,
        info=info('Title'),
        nullable=False
    )
    description = db.Column(
        db.Text,
        info=info(
            'Description',
            'Write a few sentences about the problem you are trying to solve'
        ),
        nullable=False
    )
    needed = db.Column(
        db.Text,
        info=info(
            'What is Needed',
            'What do you need from the community to solve this problem?'
        )
    )
    provided = db.Column(
        db.Text,
        info=info(
            'What is Provided',
            (
                'What can you provide to the community to help solve this '
                'problem? (e.g. equipment, knowledge, time...)'
            )
        )
    )
    contact = db.Column(
        db.Text,
        info=info(
            'Contact Information',
            (
                'How should people contact you? '
                '(e.g. email address, slack, discord...)'
            )
        )
    )
    budget = db.Column(
        db.Text,
        info=info(
            'Budget',
            'If there is a budget allocated for this, what is it?'
        )
    )
    decision_making = db.Column(
        db.Text,
        info=info(
            'Decision Making',
            (
                'Do you have the authority to make a decision to execute on a '
                'solution to this problem? If not, do you know who does?'
            )
        )
    )
    '''
    datetime_created = db.Column(
        db.DateTime,
        info=info('Modified At')
    )
    datetime_modified = db.Column(
        db.DateTime,
        info=info('Created At')
    )
    '''
    def __repr__(self):
        return 'Project {}: {}'.format(self.id, self.title)
