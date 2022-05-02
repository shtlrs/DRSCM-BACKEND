from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.template.loader import render_to_string
from drscm.models import Invoice
from drscm.permissions.model.is_owner import IsSuperUserOrOwner
from drscm.serializers import InvoiceSerializer
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework import generics


@extend_schema_view(
    get=extend_schema(
        description="Returns the list of the available invoices for the user",
        operation_id="List invoices",
    ),
    post=extend_schema(
        description="Creates a new invoice for the user", operation_id="Create invoice"
    ),
)
class CreateAndListInvoicesView(generics.ListCreateAPIView):

    view_name = "create_or_list_invoices_view"
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            queryset = Invoice.objects.all()
        else:
            queryset = Invoice.objects.filter(owner=user)

        return queryset


@extend_schema_view(
    get=extend_schema(
        description="Returns the details of a particular invoice",
        operation_id="Get invoice",
    ),
    delete=extend_schema(
        description="Invoice a particular client", operation_id="Delete invoice"
    ),
    put=extend_schema(
        description="Updates an invoice fully", operation_id="Update invoice"
    ),
    patch=extend_schema(
        description="Patches an invoice by doing a partial update of specific fields",
        operation_id="Patch invoice",
    ),
)
class InvoiceDetailsView(generics.RetrieveUpdateDestroyAPIView):

    view_name = "invoice_details_view"
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = (
        IsAuthenticated,
        IsSuperUserOrOwner,
    )


# class InvoiceReportView(APIView):
#     view_name = "invoice_report_view"
#     model = InvoiceProxy
#     permission_classes = [
#         AllowAny,
#     ]
#     renderer_classes = [TemplateHTMLRenderer]
#     template_name = "invoice/base.html"
#
#     def get(self, request, pk):
#         invoice = InvoiceProxy.objects.get(pk=pk)
#         html_string = render_to_string(
#             template_name=self.template_name,
#             context={"work_sessions": invoice.work_sessions_proxy, "invoice": invoice},
#         )
#         with open(rf"C:\Users\bellaluna\Documents\{pk}.html", "w+") as file:
#             file.write(html_string)
#         # with open(f"{pk}.html", 'rb') as fh:
#         #     response = HttpResponse(fh.read(), content_type="text/html")
#         #     response['Content-Disposition'] = 'inline; filename=' + f"{pk}.html"
#         #     return response
#         return Response(
#             {"work_sessions": invoice.work_sessions_proxy, "invoice": invoice},
#             template_name=self.template_name,
#         )
