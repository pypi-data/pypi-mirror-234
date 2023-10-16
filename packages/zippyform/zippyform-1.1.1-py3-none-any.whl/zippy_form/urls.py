from django.urls import path

from zippy_form.views import form_list, create_form, update_form, delete_form, \
    form_submission_list, steps_mapped_to_form, create_form_step, delete_form_step, fields_mapped_to_form_step, \
    map_field_to_form_step, re_order_field, delete_field, update_field_settings, \
    dynamic_form_fields_mapped_to_form_step, submit_form, update_form_status, update_form_step, dynamic_form_list, \
    create_account, account_list, form_submission_details, delete_form_submission_detail

urlpatterns = [
    path('builder/account/list', account_list),
    path('builder/account/create', create_account),
    path('builder/form/list', form_list),
    path('builder/form/create', create_form),
    path('builder/step/create', create_form_step),
    path('builder/map-field', map_field_to_form_step),
    path('builder/<uuid:form_id>/update', update_form),
    path('builder/<uuid:form_id>/update-form-status', update_form_status),
    path('builder/<uuid:form_id>/delete', delete_form),
    path('builder/<uuid:form_id>/submission/list', form_submission_list),
    path('builder/<uuid:form_id>/submission/<uuid:form_submission_id>', form_submission_details),
    path('builder/<uuid:form_id>/submission/<uuid:form_submission_id>/delete', delete_form_submission_detail),
    path('builder/<uuid:form_id>/steps', steps_mapped_to_form),
    path('builder/<uuid:form_id>/fields', fields_mapped_to_form_step),
    path('builder/<uuid:step_id>/update-form-step', update_form_step),
    path('builder/<uuid:step_id>/delete-form-step', delete_form_step),
    path('builder/<uuid:form_id>/fields/<uuid:step_id>', fields_mapped_to_form_step),
    path('builder/<uuid:form_id>/<uuid:step_id>/<uuid:field_id>/re-order-field', re_order_field),
    path('builder/<uuid:form_id>/<uuid:field_id>/delete-field', delete_field),
    path('builder/<uuid:form_id>/<uuid:field_id>/update-field-settings', update_field_settings),
    path('dynamic-form/list', dynamic_form_list),
    path('dynamic-form/<uuid:form_id>/fields', dynamic_form_fields_mapped_to_form_step),
    path('dynamic-form/<uuid:form_id>/fields/<uuid:step_id>', dynamic_form_fields_mapped_to_form_step),
    path('dynamic-form/<uuid:form_id>/submit/<uuid:step_id>', submit_form),
    path('dynamic-form/<uuid:form_id>/submit/<uuid:step_id>/<uuid:submission_id>', submit_form),
]
