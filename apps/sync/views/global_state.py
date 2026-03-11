from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse
from rest_framework.response import Response

from bloomofline.global_state import global_state


@extend_schema(tags=['GlobalState'])
@extend_schema_view(
    get=extend_schema(
        summary='Get global state',
        responses={
            200: OpenApiResponse(description='Return global state'),
        },
    ),
)
class GlobalStateView(APIView):
    def get(self, request):
        return Response({'global_state': global_state.set()})


@extend_schema(tags=['GlobalState'])
@extend_schema_view(
    get=extend_schema(
        summary='Set global state False',
        responses={
            200: OpenApiResponse(description='Return global state'),
        },
    ),
)
class GlobalStateSetFalseView(APIView):
    def get(self, request):
        global_state.set_false()
        return Response({'global_state': global_state.set()})
