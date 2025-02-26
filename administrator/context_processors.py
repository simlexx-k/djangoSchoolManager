from django.urls import reverse

def breadcrumbs(request):
    path = request.path.strip('/').split('/')
    breadcrumbs = [{'name': 'Home', 'url': reverse('admin_dashboard')}]
    url = '/'

    # Define a mapping for specific segments to names and URLs
    segment_mapping = {
        'control': {'name': 'Dashboard', 'url_name': 'admin_dashboard'},
        # Add more mappings as needed
    }

    for part in path:
        url += part + '/'
        if part in segment_mapping:
            name = segment_mapping[part]['name']
            url_name = segment_mapping[part]['url_name']
            breadcrumb_url = reverse(url_name)
        else:
            name = part.replace('-', ' ').title()
            breadcrumb_url = url
        breadcrumbs.append({'name': name, 'url': breadcrumb_url})

    return {'breadcrumbs': breadcrumbs}
