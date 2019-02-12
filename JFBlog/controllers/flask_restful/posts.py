from flask import abort
from flask_restful import Resource, fields, marshal_with

from JFBlog.controllers.flask_restful import parsers, fields as jf_fields

from ...models import db, User, Post, Tag


# String format output of tag
nested_tag_fields = {
    'id': fields.String(),
    'name': fields.String()
}

# String format output of post
post_fields = {
    'author': fields.String(attribute=str(lambda x: x.user.username)),
    'title': fields.String(),
    'text': jf_fields.HTMLField(),
    'tags': fields.List(fields.Nested(nested_tag_fields)),
    'publish_date': fields.DateTime(dt_format='iso8601')
}


class PostApi(Resource):
    """Restful API of posts resource"""

    @marshal_with(post_fields)
    def get(self, post_id=None):
        """Can be execute when receive HTTP Method 'GET'.
        Will be return the Dict object as post_fields.
        """

        if post_id:
            post = Post.query.filter_by(id=post_id).first()
            if not post:
                abort(404)
            return post
        else:
            args = parsers.post_get_parser.parse_args()
            page = args['page'] or 1

            # Return the posts with user.
            if args['user']:
                user = User.query.filter_by(username=args['user']).first()
                if not user:
                    abort(404)
                posts = user.posts.order_by(
                    Post.publish_date.desc()).paginate(page, 30)
            # Return the posts
            else:
                posts = Post.query.order_by(
                    Post.publish_date.desc()).paginate(page, 30)

            return posts.items

    def post(self, post_id=None):
        """Can be execute when receive HTTP Method 'POST'."""

        if post_id:
            abort(400)
        else:
            args = parsers.post_post_parser.parse_args(strict=True)

            new_post = Post(args['title'])
            new_post.text = args['text']
            # new_post.user = user

            if args['tags']:
                for item in args['tags']:
                    tag = Tag.query.filter_by(name=item).first()
                    # If the tag already exist, append.
                    if tag:
                        new_post.tags.append(tag)
                    # If the tag not exist, create the new one.
                    # Will be write into DB with session do.
                    else:
                        new_tag = Tag(item)
                        new_post.tags.append(new_tag)
        db.session.add(new_post)
        db.session.commit()
        return (new_post.id, 201)
