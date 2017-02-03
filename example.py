class Create(Handler):
    def post(self):
        post = Post(author = author,
            title = title,
            body = body)
        post.put()

class Update(Handler):
    def post(self, post_id):
        post = post.get_by_id(int(post_id))
        fields = ['author', 'title', 'body']
        data = get_params(self.request, fields)
        for field in fields:
            setattr(post, field, data[field])
        post.put()
