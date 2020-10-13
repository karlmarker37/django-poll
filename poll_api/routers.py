from rest_framework.routers import SimpleRouter


class OptionalTrailingSlashRouter(SimpleRouter):
    def __init__(self):
        super().__init__()
        self.trailing_slash = '/?'

    def get_urls(self):
        urls = super().get_urls()
        for url in urls:
            if url.pattern._regex == '^?$':
                url.pattern._regex = '^$'
        return urls
