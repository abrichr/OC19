from flask import (
    Blueprint, flash, redirect, request, url_for
)
from flask_login import current_user, login_required

from app.models import Comment


commentbp = Blueprint('commentbp', __name__, url_prefix='/comment')


@commentbp.route('/submit/', methods=['POST'])
@login_required
def submit():
    content = request.form
    print('comment.submit() content:', content)
    comment = content.get('comment')
    project_id = content.get('project_id')
    parent_id = content.get('parent_id')
    user_id = current_user.id
    if comment and project_id and user_id:
        comment = Comment(
            text=comment,
            project_id=project_id,
            created_by_user_id=user_id,
            parent_id=parent_id
        )
        comment.save()
        flash('Added comment')
    else:
        flash('Unable to add comment', 'error')
    return redirect(url_for('projectbp.view', project_id=project_id))
