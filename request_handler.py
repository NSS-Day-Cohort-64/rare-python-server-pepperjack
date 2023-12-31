from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from views import (create_user, login_user, get_all_users,
                   get_all_categories, create_category,
                   get_all_posts_recent_first, get_single_post, get_posts_by_user_id, create_post, edit_post,
                   get_all_tags_alphabetical, create_tag, get_postTags_by_post_id)


class HandleRequests(BaseHTTPRequestHandler):
    """Handles the requests to this server"""

    def parse_url(self):
        """Parse the url into the resource and id"""
        path_params = self.path.split('/')
        resource = path_params[1]
        if '?' in resource:
            param = resource.split('?')[1]
            resource = resource.split('?')[0]
            pair = param.split('=')
            key = pair[0]
            value = pair[1]
            return (resource, key, value)
        else:
            id = None
            try:
                id = int(path_params[2])
            except (IndexError, ValueError):
                pass
            return (resource, id)

    def _set_headers(self, status):
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        """Sets the OPTIONS headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    def do_GET(self):
        """Handle Get requests to the server"""
        response = {}
        parsed = self.parse_url()

        if len(parsed) == 3:
            resource, key, value = parsed
        else:
            resource, id = parsed

        if resource == 'categories':
            response = get_all_categories()
            self._set_headers(200)

        elif resource == 'tags':
            response = get_all_tags_alphabetical()
            self._set_headers(200)

        elif resource == "posts":
            if len(parsed) == 3 and key == 'user_id':
                response = get_posts_by_user_id(int(value))
                self._set_headers(200)
            elif id is not None:
                response = get_single_post(id)
                self._set_headers(200)
            else:
                response = get_all_posts_recent_first()
                self._set_headers(200)

        elif resource == 'postTags':
            if len(parsed) == 3 and key == 'post_id':
                response = get_postTags_by_post_id(int(value))
                self._set_headers(200)

        elif resource == 'users':
            response = get_all_users()
            self._set_headers(200)

        self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        """Make a post request to the server"""
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = json.loads(self.rfile.read(content_len))
        response = {}
        resource, _ = self.parse_url()

        dumps = False

        if resource == 'login':
            response = login_user(post_body)

        if resource == 'register':
            response = create_user(post_body)

        if resource == 'categories':
            response = create_category(post_body)
            dumps = True
        if resource == 'tags':
            response = create_tag(post_body)
            dumps = True
        if resource == 'posts':
            response = create_post(post_body)
            dumps = True

        if dumps:
            response_data = json.dumps(response).encode()
            self.wfile.write(response_data)
        else:
            self.wfile.write(response.encode())

    def do_PUT(self):
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url()

        success = False

        if resource == "posts":
            success = edit_post(id, post_body)
        # rest of the elif's

        if success:
            self._set_headers(204)
            self.wfile.write("".encode())
        else:
            self._set_headers(404)
            error_message = ""

    def do_DELETE(self):
        """Handle DELETE Requests"""
        pass


def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
