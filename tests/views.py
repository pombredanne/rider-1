from testtools import TestCase
import json
import falcon
from tests.utils import request_factory, text_data_factory, json_data_factory

from rider.views import DataView, StreamView, TextView, HtmlView, JsonView, ViewSet
from rider.http import Http404, HttpRedirect, HttpPermanentRedirect


def get_text_views(text_data):
    class TestTextView(TextView):
        def get(self, request):
            return text_data

    class TestTextView404(TextView):
        def get(self, request):
            raise Http404(text_data)

    @TextView
    def test_text_view(request):
        return text_data

    @TextView
    def test_text_view_404(request):
        raise Http404(text_data)

    return TestTextView, TestTextView404, test_text_view, test_text_view_404


def get_html_views(html_data):
    class TestHtmlView(HtmlView):
        def get(self, request):
            return html_data

    class TestHtmlView404(HtmlView):
        def get(self, request):
            raise Http404(html_data)

    @HtmlView
    def test_html_view(request):
        return html_data

    @HtmlView
    def test_html_view_404(request):
        raise Http404(html_data)

    return TestHtmlView, TestHtmlView404, test_html_view, test_html_view_404


def get_json_views(json_data):

    class TestJsonView404(JsonView):
        def get(self, request):
            raise Http404(json_data)

    class TestJsonView(JsonView):
        def get(self, request):
            return json_data

    @JsonView
    def test_json_view(request):
        return json_data

    @JsonView
    def test_json_view_404(request):
        raise Http404(json_data)

    return TestJsonView, TestJsonView404, test_json_view, test_json_view_404

#def get_stream_views(location):
     #class TestStreamView404(JsonView):
        #def get(self, request):
            #raise Http404(json_data)

    #class TestStreamView(JsonView):
        #def get(self, request):
            #return json_data

    #@JsonView
    #def test_stream_view(request):
        #return json_data

    #@JsonView
    #def test_stream_view_404(request):
        #raise Http404(json_data)

    #return TestJsonView404, TestJsonView, test_json_view, test_json_view_404


def get_redirect_views(location):
    result = []
    for view_cls in (DataView, StreamView, TextView, HtmlView, JsonView):
        class TestRedirectView(view_cls):
            def get(self, request):
                raise HttpRedirect(location)
        yield TestRedirectView, falcon.HTTP_302

        class TestPermanentRedirectView(view_cls):
            def get(self, request):
                raise HttpPermanentRedirect(location)
        yield TestPermanentRedirectView, falcon.HTTP_301


def get_viewsets(text_data, html_data, json_data):
    class TestViewSet(ViewSet):
        @route('a')
        @TextView
        def text(self, request):
            return text_data

        @route('b')
        @HtmlView
        def html(self, request):
            return html_data

        @route('c')
        @JsonView
        def json(self, request):
            return json_data

    return TestViewSet


class TestViews(TestCase):
    """Tests for views"""

    def _test_view(self, test_view_cls, request, expected_result, expected_content_type):
        view = test_view_cls()
        response = falcon.Response()
        view.on_get(request, response)
        result = falcon.api_helpers.get_body(response)
        self.assertEqual(expected_result, result[0].decode('utf-8'))
        self.assertEqual(response.content_type, expected_content_type)

    def test_text_views(self):
        text_data = text_data_factory()
        request = request_factory(url='/')
        for text_view_cls in get_text_views(text_data):
            self._test_view(text_view_cls, request, text_data, 'text/plain')

    def test_html_views(self):
        text_data = text_data_factory()
        request = request_factory(url='/')
        for html_view_cls in get_html_views(text_data):
            self._test_view(html_view_cls, request, text_data, 'text/html')

    def test_json_views(self):
        json_data = json_data_factory()
        string_json_data = json_data_factory.as_string()
        request = request_factory(url='/')
        for json_view_cls in get_json_views(json_data):
            self._test_view(json_view_cls, request, string_json_data, 'application/json')

    def test_redirect_views(self):
        location = '/new_location'
        request = request_factory(url='/')
        for redirect_view_cls, status  in get_redirect_views(location):
            redirect_view = redirect_view_cls()
            response = falcon.Response()
            redirect_view.on_get(request, response)

            self.assertEqual(location, response.location)
            self.assertEqual(response.status, status)


