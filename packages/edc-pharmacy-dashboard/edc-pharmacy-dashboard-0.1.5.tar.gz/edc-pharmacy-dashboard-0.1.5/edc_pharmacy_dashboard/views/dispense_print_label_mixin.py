# from django.contrib import messages
# from edc_label.print_server import PrintServerSelectPrinterError
#
#
# class DispensePrintLabelMixin:
#
#     def prescriptions(self):
#         pass
#
#     def print_labels(self, request, **kwargs):
#         try:
#             dispense_print = self.dispense_cls(
#                 user=request.user,
#                 subject_identifier=kwargs.get('subject_identifier'),
#                 prescriptions=self.prescriptions,
#                 appointment_id=kwargs.get('appointment'))
#         except PrintServerSelectPrinterError as e:
#             messages.error(
#                 self.request,
#                 str(e), extra_tags='PrintServerSelectPrinterError')
#         else:
#             for label in dispense_print.printed_labels or []:
#                 description = label.get('medication')
#                 subject_identifier = label.get('subject_identifier')
#                 messages.success(
#                     self.request,
#                     f'Printed {description} for {subject_identifier}.')
