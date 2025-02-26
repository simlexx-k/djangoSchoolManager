class BreadcrumbsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Generate breadcrumb data based on the request path
        path = request.path.strip('/').split('/')
        breadcrumbs = [{'name': 'Home', 'url': '/'}]
        url = '/'
        for part in path:
            url += part + '/'
            breadcrumbs.append({'name': part.replace('-', ' ').title(), 'url': url})

        # Attach breadcrumbs to the request
        request.breadcrumbs = breadcrumbs

        response = self.get_response(request)
        return response