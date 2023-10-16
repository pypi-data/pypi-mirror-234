import json
import uuid

from django.core.paginator import Paginator
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from zippy_form.models import Account, FormField, Form, FormStep, FormSubmission, FormSubmissionData, FormFieldOption
from zippy_form.serializers import FormSerializer, FormStepSerializer, MapFieldToFormStepSerializer, UpdateFieldSettingsSerializer, \
    ReOrderFieldSerializer, AccountSerializer
from zippy_form.utils import FORM_STATUS, FORM_FIELD_STATUS, FIELD_TYPES, FORM_SUBMISSION_STATUS, \
    FORM_SUBMISSION_STATUS_DETAILS, FORM_STEP_STATUS, FIELD_RULES, FORM_FIELD_OPTION_STATUS, FIELD_RULES_FILE_FORMAT_ALLOWED, \
    FORM_STATUS_DETAILS, FORM_FIELD_DETAILS, FORM_STEP_STATUS_DETAILS, ACCOUNT_STATUS, ACCOUNT_STATUS_DETAILS
from zippy_form.validation_rule import validate_is_empty, validate_minlength, validate_maxlength, validate_is_url,\
    validate_is_unique, validate_is_number, validate_min_value, validate_max_value, validate_is_email, validate_is_date,\
    validate_min_max_selection, validate_is_file, validate_file_extension, validate_file_size, validate_is_time
from zippy_form.event_webhook_triggers import after_account_create, after_form_create, after_form_submit
from zippy_form.gsheet import create_gsheet_map_form, send_form_data_to_gsheet, remove_form_data_from_gsheet, \
    add_field_labels_to_gsheet, update_field_label_in_gsheet, remove_field_from_gsheet
from zippy_form.permissions import IsAccountActive

try:
    DEFAULT_PAGE_SIZE = settings.ZF_LIST_PER_PAGE
except:
    DEFAULT_PAGE_SIZE = 6

@api_view(['GET'])
def account_list(req):
    """
    Get list of active accounts
    """
    page_size = DEFAULT_PAGE_SIZE

    response_data = {'list': {}}

    page = req.GET.get('page', 1)

    # Get only non deleted accounts
    accounts = Account.objects.exclude(status=ACCOUNT_STATUS[0][0]).order_by('-created_date')

    paginator = Paginator(accounts, page_size)
    page_obj = paginator.get_page(page)

    if int(page) > page_obj.paginator.num_pages:
        response_data['list']['per_page'] = 0
        response_data['list']['page'] = 0
        response_data['list']['total'] = 0
        response_data['list']['total_pages'] = 0
        response_data['list']['data'] = []
        response_data['list']['msg'] = "Invalid Page."

        return Response({"status": "error", "data": response_data}, status=status.HTTP_400_BAD_REQUEST)
    else:
        data = []
        # Loop each form
        for account in page_obj.object_list:
            active_form_count = Form.objects.filter(account=account).exclude(status=FORM_STATUS[0][0]).count()

            single_row_entry = {}
            single_row_entry['id'] = account.id
            single_row_entry['name'] = account.name
            single_row_entry['admin_email'] = account.admin_email
            single_row_entry['meta_detail'] = account.meta_detail
            single_row_entry['active_form_count'] = active_form_count
            single_row_entry['status'] = account.status
            single_row_entry['status_text'] = ACCOUNT_STATUS_DETAILS[account.status]

            data.append(single_row_entry)

        response_data['list']['per_page'] = page_obj.paginator.per_page
        response_data['list']['page'] = page_obj.number
        response_data['list']['total'] = page_obj.paginator.count
        response_data['list']['total_pages'] = page_obj.paginator.num_pages
        response_data['list']['data'] = data

        return Response({"status": "success", "data": response_data}, status=status.HTTP_200_OK)

@api_view(['POST'])
def create_account(req):
    """
    Create Account
    """
    serializer = AccountSerializer(data=req.data)

    if not serializer.is_valid():
        return Response({"status": "validation_error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    else:
        instance = serializer.save()
        response_data = {'data': {}}
        response_data['data']['id'] = instance.id

        # Event & Webhook - Account Create
        event_data = {"event": "account.created", "account": {"id": str(instance.id), "meta_detail": instance.meta_detail}}
        after_account_create(event_data)

        return Response({"status": "success", "data": response_data, "msg": "Account Created Successfully."},
                        status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAccountActive])
def form_list(req):
    """
    Get list of non deleted forms mapped to the account
    """
    page_size = DEFAULT_PAGE_SIZE
    response_data = {'list': {}}

    page = req.GET.get('page', 1)
    search_by_keyword = req.GET.get('search', None)
    search_by_status = req.GET.get('status', None)

    account_id = req.headers['ZF-SECRET-KEY']

    # Get only non deleted forms
    form_submissions = Form.objects.filter(account_id=account_id).exclude(status=FORM_STATUS[0][0]).order_by('-created_date')

    if search_by_keyword:
        form_submissions = form_submissions.filter(Q(name__icontains=search_by_keyword))
    if search_by_status:
        form_submissions = form_submissions.filter(status=search_by_status)

    paginator = Paginator(form_submissions, page_size)
    page_obj = paginator.get_page(page)

    if int(page) > page_obj.paginator.num_pages:
        response_data['list']['per_page'] = 0
        response_data['list']['page'] = 0
        response_data['list']['total'] = 0
        response_data['list']['total_pages'] = 0
        response_data['list']['data'] = []
        response_data['list']['msg'] = "Invalid Page."

        return Response({"status": "error", "data": response_data}, status=status.HTTP_400_BAD_REQUEST)
    else:
        data = []
        # Loop each form
        for form in page_obj.object_list:
            single_row_entry = {}
            single_row_entry['id'] = form.id
            single_row_entry['name'] = form.name
            single_row_entry['description'] = form.description
            single_row_entry['meta_detail'] = form.meta_detail
            single_row_entry['gsheet_url'] = form.gsheet_url
            single_row_entry['status'] = form.status
            single_row_entry['status_text'] = FORM_STATUS_DETAILS[form.status]

            data.append(single_row_entry)

        response_data['list']['per_page'] = page_obj.paginator.per_page
        response_data['list']['page'] = page_obj.number
        response_data['list']['total'] = page_obj.paginator.count
        response_data['list']['total_pages'] = page_obj.paginator.num_pages
        response_data['list']['data'] = data

        return Response({"status": "success", "data": response_data}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAccountActive])
def create_form(req):
    """
    Create form with status draft with step 1 under an Account - To be used when clicking "Add Form" from the form builder
    """
    meta_detail = req.data.get("meta_detail", "")

    account_id = req.headers['ZF-SECRET-KEY']

    form = Form.objects.create(name="Untitled Form", account_id= account_id, meta_detail=meta_detail)

    form_step = FormStep.objects.create(
        name="Step 1",
        step_order=1,
        form=form,
    )

    # Create Gsheet & map to form - if form submission is allowed to sync on Gsheet
    gsheet = create_gsheet_map_form(form)

    steps = []
    response_data = {'form': {}, 'steps': steps}

    response_data['form']['id'] = str(form.id)
    response_data['form']['name'] = form.name
    response_data['form']['description'] = ''
    response_data['form']['class_name'] = ''
    response_data['form']['meta_detail'] = form.meta_detail
    response_data['form']['success_msg'] = ''
    response_data['form']['status'] = form.status
    response_data['form']['status_text'] = FORM_STATUS_DETAILS[form.status]

    step_details = {'id': form_step.id, 'name': form_step.name, 'description': '', 'is_current_step': True}
    steps.append(step_details)

    # Event & Webhook - Form Create
    event_data = {
        "event": "form.created",
        "account": {"id": str(form.account.id), "meta_detail": form.account.meta_detail},
        "form": response_data['form']
    }
    after_form_create(event_data)

    return Response({"status": "success", "data": response_data, "msg": "Form Created Successfully."},
                    status=status.HTTP_201_CREATED)


@api_view(['PUT'])
def update_form(req, form_id):
    """
    Update form
    * Update form & field status from Draft to Active
    """
    try:
        # Update only for non deleted form
        form = Form.objects.filter(id=form_id).exclude(status=FORM_STATUS[0][0]).get()
    except Form.DoesNotExist:
        msg = "Invalid Form ID."
        return Response({"status": "error", "msg": msg}, status=status.HTTP_400_BAD_REQUEST)

    serializer = FormSerializer(form, data=req.data)

    if not serializer.is_valid():
        return Response({"status": "validation_error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    else:
        form.name = serializer.validated_data['name']
        # Update draft form to active status
        if form.status == FORM_STATUS[3][0]:
            form.status = FORM_STATUS[1][0]
        form.save()

    _draft_fields = []
    # Update draft fields of the form to active status, which has field settings updated
    form_fields = form.form_fields.filter(status=FORM_FIELD_STATUS[3][0]).filter(is_field_settings_updated=True).order_by('field_order')
    for form_field in form_fields:

        temp = {}
        temp['id'] = str(form_field.id)
        temp['label'] = form_field.label
        _draft_fields.append(temp)

        form_field.status = FORM_FIELD_STATUS[1][0]
        form_field.save()

    # Add new field label to gsheet(When field status update from "draft" to "active, sync to gsheet)
    add_field_labels_to_gsheet(_draft_fields, form)

    response_data = {'form': {}}

    response_data['form']['id'] = form.id
    response_data['form']['name'] = form.name
    response_data['form']['description'] = ''
    response_data['form']['class_name'] = ''
    response_data['form']['success_msg'] = ''
    response_data['form']['status'] = form.status
    response_data['form']['status_text'] = FORM_STATUS_DETAILS[form.status]

    return Response({"status": "success", "data": response_data, "msg": "Form Updated Successfully."},
                    status=status.HTTP_200_OK)


@api_view(['PUT'])
def update_form_status(req, form_id):
    """
    Update form status
    * Active to InActive
    * InActive to Active
    """
    try:
        # Update form status only for the non deleted form
        form = Form.objects.filter(id=form_id).exclude(status=FORM_STATUS[0][0]).get()
    except Form.DoesNotExist:
        data = "Invalid Form ID."
        return Response({"status": "error", "data": data}, status=status.HTTP_400_BAD_REQUEST)

    if form.status == FORM_STATUS[1][0]:
        # Update form status from Active to InActive
        form.status = FORM_STATUS[2][0]
        form.save()
    elif form.status == FORM_STATUS[2][0]:
        # Update form status from InActive to Active
        form.status = FORM_STATUS[1][0]
        form.save()

    response_data = {'form': {}}

    response_data['form']['id'] = form.id

    return Response({"status": "success", "data": response_data, "msg": "Form Status Updated Successfully."},
                    status=status.HTTP_200_OK)


@api_view(['DELETE'])
def delete_form(req, form_id):
    """
    Soft delete form
    """
    try:
        form = Form.objects.filter(id=form_id).exclude(status=FORM_STATUS[0][0]).get()
    except Form.DoesNotExist:
        data = "Invalid Form ID."
        return Response({"status": "error", "data": data}, status=status.HTTP_400_BAD_REQUEST)

    # Soft delete form
    form.status = FORM_STATUS[0][0]
    form.save()

    response_data = {'form': {}}

    response_data['form']['id'] = form.id

    return Response({"status": "success", "data": response_data, "msg": "Form Deleted Successfully."},
                    status=status.HTTP_200_OK)


@api_view(['GET'])
def form_submission_list(req, form_id):
    """
    Get list of form submissions
    """
    try:
        # Get submission only for the non deleted form
        form = Form.objects.filter(id=form_id).exclude(status=FORM_STATUS[0][0]).get()
    except Form.DoesNotExist:
        data = "Invalid Form ID."
        return Response({"status": "error", "data": data}, status=status.HTTP_400_BAD_REQUEST)

    page_size = DEFAULT_PAGE_SIZE
    response_data = {'list': {}}

    page = req.GET.get('page', 1)

    # Get only non deleted form submission
    form_submissions = FormSubmission.objects.filter(form=form_id).exclude(status=FORM_SUBMISSION_STATUS[0][0]) \
        .order_by('-modified_date')

    paginator = Paginator(form_submissions, page_size)
    page_obj = paginator.get_page(page)

    if int(page) > page_obj.paginator.num_pages:
        response_data['list']['per_page'] = 0
        response_data['list']['page'] = 0
        response_data['list']['total'] = 0
        response_data['list']['total_pages'] = 0
        response_data['list']['data'] = []
        response_data['list']['msg'] = "Invalid Page."

        return Response({"status": "error", "data": response_data}, status=status.HTTP_400_BAD_REQUEST)
    else:
        column_headers = []
        column_field_id = []

        column_headers.append({"field_type": '_id', "label": 'Id'})

        # Get only active fields which are configured to show on table
        table_form_fields = form.form_fields.filter(status=FORM_FIELD_STATUS[1][0]).filter(show_on_table=True) \
            .order_by('table_field_order')

        # From above queryset - Get the "Column Headers" & "Field ID"
        for table_form_field in table_form_fields:
            column_headers.append({"field_type": table_form_field.field_type, "label": table_form_field.label})
            column_field_id.append(str(table_form_field.id))

        column_headers.append({"field_type": '_status_id', "label": 'Status ID'})
        column_headers.append({"field_type": '_status', "label": 'Status'})

        data = []
        # Loop each form submission
        for form_submission in page_obj.object_list:
            single_row_entry = []

            # default - "ID" at first index for each submission
            single_row_entry.append(form_submission.id)

            # get the submitted data from "FormSubmissionData" - based on the "form submission" & the active fields
            # which are configured to show on table | getting all the values here, to reduce db call
            dynamic_field_values = FormSubmissionData.objects.filter(form_submission=form_submission) \
                .filter(form_field_id__in=column_field_id)

            formatted_dynamic_field_values = {}
            for dynamic_field_value in dynamic_field_values:
                field_type = dynamic_field_value.form_field.field_type
                if field_type == FIELD_TYPES[5][0]:
                    _values = format_string_to_json_array(dynamic_field_value.dropdown_field)
                    _option_values = get_field_option_values(_values)
                    if _values is not None:
                        formatted_dynamic_field_values[str(dynamic_field_value.form_field.id)] = _option_values
                    else:
                        formatted_dynamic_field_values[str(dynamic_field_value.form_field.id)] = []
                elif field_type == FIELD_TYPES[6][0]:
                    _value = dynamic_field_value.radio_field
                    _option_value = get_field_option_value(_value)
                    formatted_dynamic_field_values[str(dynamic_field_value.form_field.id)] = _option_value
                # elif field_type == FIELD_TYPES[7][0]:
                #     formatted_dynamic_field_values[str(dynamic_field_value.form_field.id)] = dynamic_field_value.checkbox_field
                elif field_type == FIELD_TYPES[10][0]:
                    _value = dynamic_field_value.file_field
                    if _value:
                        formatted_dynamic_field_values[str(dynamic_field_value.form_field.id)] = _value.url
                    else:
                        formatted_dynamic_field_values[str(dynamic_field_value.form_field.id)] = ""
                elif field_type == FIELD_TYPES[12][0]:
                    _values = format_string_to_json_array(dynamic_field_value.multiselect_checkbox_field)
                    if _values is not None:
                        _option_values = get_field_option_values(_values)
                        formatted_dynamic_field_values[str(dynamic_field_value.form_field.id)] = _option_values
                    else:
                        formatted_dynamic_field_values[str(dynamic_field_value.form_field.id)] = []
                else:
                    formatted_dynamic_field_values[str(dynamic_field_value.form_field.id)] = dynamic_field_value.text_field

            # loop the active fields which are configured to show on table & get the values added on the submission
            # using "formatted_dynamic_field_values"
            for column_field in column_field_id:
                if formatted_dynamic_field_values.get(column_field):
                    single_row_entry.append(formatted_dynamic_field_values.get(column_field))
                elif formatted_dynamic_field_values.get(column_field) == []:
                    single_row_entry.append([])
                else:
                    single_row_entry.append("")

            # default - "Status ID & Status" at last index for each submission
            single_row_entry.append(form_submission.status)
            single_row_entry.append(FORM_SUBMISSION_STATUS_DETAILS[form_submission.status])

            data.append(single_row_entry)

        response_data['column_headers'] = column_headers
        response_data['list']['per_page'] = page_obj.paginator.per_page
        response_data['list']['page'] = page_obj.number
        response_data['list']['total'] = page_obj.paginator.count
        response_data['list']['total_pages'] = page_obj.paginator.num_pages
        response_data['list']['data'] = data

        return Response({"status": "success", "data": response_data}, status=status.HTTP_200_OK)


@api_view(['GET'])
def form_submission_details(req,form_id, form_submission_id):
    """
    Get form submission details
    """
    try:
        # Get only non deleted form submission
        form_submission = FormSubmission.objects.filter(id=form_submission_id).exclude(status=FORM_SUBMISSION_STATUS[0][0]).get()
    except FormSubmission.DoesNotExist:
        data = "Invalid Form Submission ID."
        return Response({"status": "error", "data": data}, status=status.HTTP_400_BAD_REQUEST)

    column_headers = []
    column_field_id = []

    column_headers.append({"field_type": '_id', "label": 'Id'})

    # Get only active fields which are configured to show on table
    table_form_fields = form_submission.form.form_fields.filter(status=FORM_FIELD_STATUS[1][0]).order_by('table_field_order')

    # From above queryset - Get the "Column Headers" & "Field ID"
    for table_form_field in table_form_fields:
        column_headers.append({"field_type": table_form_field.field_type, "label": table_form_field.label})
        column_field_id.append(str(table_form_field.id))

    column_headers.append({"field_type": '_status_id', "label": 'Status ID'})
    column_headers.append({"field_type": '_status', "label": 'Status'})

    single_row_entry = []

    # default - "ID" at first index for each submission
    single_row_entry.append(form_submission.id)

    # get the submitted data from "FormSubmissionData" - based on the "form submission" & the active fields
    # which are configured to show on table | getting all the values here, to reduce db call
    dynamic_field_values = FormSubmissionData.objects.filter(form_submission=form_submission) \
        .filter(form_field_id__in=column_field_id)

    formatted_dynamic_field_values = {}
    for dynamic_field_value in dynamic_field_values:
        field_type = dynamic_field_value.form_field.field_type
        if field_type == FIELD_TYPES[5][0]:
            _values = format_string_to_json_array(dynamic_field_value.dropdown_field)
            _option_values = get_field_option_values(_values)
            if _value is not None:
                formatted_dynamic_field_values[str(dynamic_field_value.form_field.id)] = _option_values
            else:
                formatted_dynamic_field_values[str(dynamic_field_value.form_field.id)] = []
        elif field_type == FIELD_TYPES[6][0]:
            _value = dynamic_field_value.radio_field
            _option_value = get_field_option_value(_value)
            formatted_dynamic_field_values[str(dynamic_field_value.form_field.id)] = _option_value
        # elif field_type == FIELD_TYPES[7][0]:
        #     formatted_dynamic_field_values[str(dynamic_field_value.form_field.id)] = dynamic_field_value.checkbox_field
        elif field_type == FIELD_TYPES[10][0]:
            _value = dynamic_field_value.file_field
            if _value:
                formatted_dynamic_field_values[str(dynamic_field_value.form_field.id)] = _value.url
            else:
                formatted_dynamic_field_values[str(dynamic_field_value.form_field.id)] = ""
        elif field_type == FIELD_TYPES[12][0]:
            _values = format_string_to_json_array(dynamic_field_value.multiselect_checkbox_field)
            if _values is not None:
                _option_values = get_field_option_values(_values)
                formatted_dynamic_field_values[str(dynamic_field_value.form_field.id)] = _option_values
            else:
                formatted_dynamic_field_values[str(dynamic_field_value.form_field.id)] = []
        else:
            formatted_dynamic_field_values[str(dynamic_field_value.form_field.id)] = dynamic_field_value.text_field

    # loop the active fields which are configured to show on table & get the values added on the submission
    # using "formatted_dynamic_field_values"
    for column_field in column_field_id:
        if formatted_dynamic_field_values.get(column_field):
            single_row_entry.append(formatted_dynamic_field_values.get(column_field))
        elif formatted_dynamic_field_values.get(column_field) == []:
            single_row_entry.append([])
        else:
            single_row_entry.append("")

    # default - "Status ID & Status" at last index for each submission
    single_row_entry.append(form_submission.status)
    single_row_entry.append(FORM_SUBMISSION_STATUS_DETAILS[form_submission.status])

    response_data = {}
    response_data['data'] = single_row_entry
    response_data['column_headers'] = column_headers

    return Response({"status": "success", "data": response_data}, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def delete_form_submission_detail(req,form_id, form_submission_id):
    """
    Delete Form Submission Detail
    """
    try:
        # Get only non deleted form submission
        form_submission = FormSubmission.objects.filter(id=form_submission_id).exclude(status=FORM_SUBMISSION_STATUS[0][0]).get()
    except FormSubmission.DoesNotExist:
        data = "Invalid Form Submission ID."
        return Response({"status": "error", "data": data}, status=status.HTTP_400_BAD_REQUEST)

    form = form_submission.form

    # Todo

    # Remove Form Data From Gsheet
    remove_form_data_from_gsheet(form, form_submission_id)

@api_view(['GET'])
def steps_mapped_to_form(req, form_id):
    """
    Get steps mapped to form
    """
    try:
        # Get form steps only for the non deleted form
        form = Form.objects.filter(id=form_id).exclude(status=FORM_STATUS[0][0]).get()
    except Form.DoesNotExist:
        data = "Invalid Form ID."
        return Response({"status": "error", "data": data}, status=status.HTTP_400_BAD_REQUEST)

    page_size = DEFAULT_PAGE_SIZE
    response_data = {'list': {}}

    page = req.GET.get('page', 1)

    form_steps = form.form_steps.exclude(status=FORM_STEP_STATUS[0][0]).order_by('step_order')

    paginator = Paginator(form_steps, page_size)
    page_obj = paginator.get_page(page)

    if int(page) > page_obj.paginator.num_pages:
        response_data['list']['per_page'] = 0
        response_data['list']['page'] = 0
        response_data['list']['total'] = 0
        response_data['list']['total_pages'] = 0
        response_data['list']['data'] = []
        response_data['list']['msg'] = "Invalid Page."

        return Response({"status": "error", "data": response_data}, status=status.HTTP_400_BAD_REQUEST)
    else:
        data = []
        # Loop each step
        for form_step in page_obj.object_list:
            single_row_entry = {}
            single_row_entry['id'] = form_step.id
            single_row_entry['name'] = form_step.name
            single_row_entry['description'] = form_step.description
            single_row_entry['status'] = form_step.status
            single_row_entry['status_text'] = FORM_STEP_STATUS_DETAILS[form_step.status]

            data.append(single_row_entry)

        response_data['list']['per_page'] = page_obj.paginator.per_page
        response_data['list']['page'] = page_obj.number
        response_data['list']['total'] = page_obj.paginator.count
        response_data['list']['total_pages'] = page_obj.paginator.num_pages
        response_data['list']['data'] = data

        return Response({"status": "success", "data": response_data}, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_form_step(req):
    """
    Create form step & map to form
    """
    serializer = FormStepSerializer(data=req.data)

    if not serializer.is_valid():
        return Response({"status": "validation_error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    else:
        instance = serializer.save()

        response_data = {'step': {}}

        response_data['step']['id'] = instance.id
        response_data['step']['name'] = instance.name

        return Response({"status": "success", "data": response_data, "msg": "Form Step Created Successfully."},
                        status=status.HTTP_201_CREATED)

@api_view(['PUT'])
def update_form_step(req, step_id):
    """
    Update form step
    """
    try:
        form_step = FormStep.objects.filter(id=step_id).exclude(status=FORM_STATUS[0][0]).get()
    except FormStep.DoesNotExist:
        data = "Invalid Form Step ID."
        return Response({"status": "error", "data": data}, status=status.HTTP_400_BAD_REQUEST)

    serializer = FormStepSerializer(form_step, data=req.data)

    if not serializer.is_valid():
        return Response({"status": "validation_error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    else:
        instance = serializer.save()

        response_data = {'step': {}}

        response_data['step']['id'] = instance.id
        response_data['step']['name'] = instance.name

        return Response({"status": "success", "data": response_data, "msg": "Form Step Updated Successfully."},
                        status=status.HTTP_200_OK)

@api_view(['DELETE'])
def delete_form_step(req, step_id):
    """
    Soft delete form step
    """
    try:
        form_step = FormStep.objects.filter(id=step_id).exclude(status=FORM_STATUS[0][0]).get()
    except FormStep.DoesNotExist:
        data = "Invalid Form Step ID."
        return Response({"status": "error", "data": data}, status=status.HTTP_400_BAD_REQUEST)

    #  Soft delete form step
    form_step.status = FORM_STEP_STATUS[0][0]
    form_step.save()

    response_data = {'step': {}}

    response_data['step']['id'] = form_step.id
    response_data['step']['name'] = form_step.name

    return Response({"status": "success", "data": response_data, "msg": "Form Step Deleted Successfully."},
                    status=status.HTTP_200_OK)


@api_view(['GET'])
def fields_mapped_to_form_step(req, form_id, step_id = None):
    """
    Get list of fields mapped to form step
    """
    try:
        form = Form.objects.filter(id=form_id).exclude(status=FORM_STATUS[0][0]).get()
    except Form.DoesNotExist:
        data = "Invalid Form ID."
        return Response({"status": "error", "data": data}, status=status.HTTP_400_BAD_REQUEST)

    # Get all step mapped to form - Query not executed here
    form_steps = form.form_steps.filter(status=FORM_STEP_STATUS[1][0]).order_by('step_order')

    if step_id is None:
        # Query executed here
        first_form_step = form_steps.first()
        if not first_form_step:
            data = "No Form Step Available."
            return Response({"status": "error", "data": data}, status=status.HTTP_400_BAD_REQUEST)
        current_step = str(first_form_step.id)
    else:
        # Check if the "step id" received from request is valid
        try:
            form.form_steps.filter(id=step_id).filter(status=FORM_STEP_STATUS[1][0]).get()
        except FormStep.DoesNotExist:
            data = "Invalid Form Step ID."
            return Response({"status": "error", "data": data}, status=status.HTTP_400_BAD_REQUEST)

        current_step = step_id

    # Get only active fields
    form_fields = FormField.objects.filter(form_id=form_id).filter(form_step=current_step) \
        .exclude(status=FORM_FIELD_STATUS[0][0]).order_by('field_order').prefetch_related('form_field_options')

    steps = []
    fields = []

    response_data = {'action': "#", 'form': {}, 'steps': steps, 'fields': fields}

    response_data['form']['id'] = form.id
    response_data['form']['name'] = form.name
    response_data['form']['description'] = form.description
    response_data['form']['class_name'] = form.class_name
    response_data['form']['success_msg'] = form.success_msg
    response_data['form']['status'] = form.status
    response_data['form']['status_text'] = FORM_STATUS_DETAILS[form.status]

    for form_step in form_steps:
        step = {}
        step['id'] = form_step.id
        step['name'] = form_step.name
        step['description'] = form_step.description

        if current_step == str(form_step.id):
            step['is_current_step'] = True
        else:
            step['is_current_step'] = False

        steps.append(step)

    for form_field in form_fields:
        field_details = {
            'field_id': form_field.id,
            'field_type': form_field.field_type,
            'field_order': form_field.field_order,
            'field_size': form_field.field_size,
            'label': form_field.label,
            'class_name': form_field.custom_class_name,
            'is_mandatory': form_field.is_mandatory,
        }

        field_type = form_field.field_type

        if field_type != FIELD_TYPES[14][0] and field_type != FIELD_TYPES[15][0]:
            field_details['placeholder'] = form_field.placeholder
            field_details['validations'] = form_field.validation_rule

        if field_type == FIELD_TYPES[5][0] or field_type == FIELD_TYPES[6][0] or field_type == FIELD_TYPES[7][0] or \
                field_type == FIELD_TYPES[12][0]:
            # Get Options for Dropdown, Radio, Checkbox, MultiSelect Checkbox fields
            field_options = []

            form_field_options = form_field.form_field_options.filter(status=FORM_FIELD_OPTION_STATUS[1][0]).order_by(
                'option_order').all()
            for form_field_option in form_field_options:
                field_option = {
                    'value': form_field_option.id,
                    'label': form_field_option.label,
                }
                field_options.append(field_option)

            field_details['options'] = field_options

        if field_type == FIELD_TYPES[0][0] or field_type == FIELD_TYPES[1][0] or field_type == FIELD_TYPES[3][0] or \
                field_type == FIELD_TYPES[4][0] or field_type == FIELD_TYPES[5][0]:
            # Text Box, Number, Email, Website URL, Dropdown
            field_details['field_format'] = form_field.field_format

        if field_type == FIELD_TYPES[14][0] or field_type == FIELD_TYPES[15][0]:
            # Heading, Paragraph
            field_details['content'] = form_field.content
            field_details['content_size'] = form_field.content_size
            field_details['content_alignment'] = form_field.content_alignment

        field_details['status'] = form_field.status
        field_details['status_text'] = FORM_FIELD_DETAILS[form_field.status]

        fields.append(field_details)

    response_data['fields'] = fields

    return Response({"status": "success", "data": response_data}, status=status.HTTP_200_OK)


@api_view(['POST'])
def map_field_to_form_step(req):
    """
    Map Field to Form Step with draft status
    """
    serializer = MapFieldToFormStepSerializer(data=req.data)

    if not serializer.is_valid():
        return Response({"status": "validation_error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    else:
        try:
            # Map fields only for the non deleted form
            form = serializer.validated_data['form']
            form_id = form.id
            form = Form.objects.filter(id=form_id).exclude(status=FORM_STATUS[0][0]).get()
        except Form.DoesNotExist:
            data = {}
            msg = []
            data['form'] = msg
            msg.append("Invalid Form ID.")
            return Response({"status": "validation_error", "data": data}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Map fields only for the active step
            form_step = serializer.validated_data['form_step']
            form_step_id = form_step.id
            form_step = form.form_steps.filter(id=form_step_id).filter(status=FORM_STEP_STATUS[1][0]).get()
        except FormStep.DoesNotExist:
            data = {}
            msg = []
            data['form_step'] = msg
            msg.append("Invalid Form Step ID.")
            return Response({"status": "validation_error", "data": data}, status=status.HTTP_400_BAD_REQUEST)

        # Map field to form step
        field_order = serializer.validated_data['field_order']
        instance = serializer.save(table_field_order=field_order)

        response_data = {'field': {}}

        response_data['field']['id'] = instance.id
        response_data['field']['label'] = instance.label
        response_data['field']['type'] = instance.field_type

        return Response({"status": "success", "data": response_data, "msg": "Field Mapped To Form Successfully."},
                        status=status.HTTP_200_OK)


@api_view(['PUT'])
def re_order_field(req, form_id, step_id, field_id):
    """
    ReOrder Form Field
    """
    try:
        # ReOrder field only for non deleted form
        form = Form.objects.filter(id=form_id).exclude(status=FORM_STATUS[0][0]).get()
    except Form.DoesNotExist:
        msg = "Invalid Form ID."
        return Response({"status": "error", "msg": msg}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # ReOrder field only for non deleted field step
        form_steps = form.form_steps.filter(id=step_id).exclude(status=FORM_STEP_STATUS[0][0]).get()
    except FormStep.DoesNotExist:
        msg = "Invalid Form Step ID."
        return Response({"status": "error", "msg": msg}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # ReOrder field only for non deleted field
        field = form_steps.form_step_fields.filter(id=field_id).exclude(status=FORM_FIELD_STATUS[0][0]).get()
    except FormField.DoesNotExist:
        msg = "Invalid Form Field ID."
        return Response({"status": "error", "msg": msg}, status=status.HTTP_400_BAD_REQUEST)

    serializer = ReOrderFieldSerializer(field, data=req.data)

    if not serializer.is_valid():
        return Response({"status": "validation_error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    else:
        new_field_order = int(req.POST.get('field_order'))
        old_field_order = field.field_order

        if old_field_order < new_field_order:
            # Moving field down, update fields between old and new position
            fields_to_update = FormField.objects.filter(form_step__id=step_id).filter(field_order__gt=old_field_order,
                                                        field_order__lte=new_field_order).order_by('field_order')
            for field in fields_to_update:
                field.field_order -= 1
                field.save()
        elif old_field_order > new_field_order:
            # Moving field up, update fields between new and old position
            fields_to_update = FormField.objects.filter(form_step__id=step_id).filter(field_order__gte=new_field_order,
                                                        field_order__lt=old_field_order).order_by('-field_order')
            for field in fields_to_update:
                field.field_order += 1
                field.save()

        instance = serializer.save()

        response_data = {'field': {}}

        response_data['field']['id'] = instance.id

        return Response({"status": "success", "data": response_data, "msg": "Field ReOrdered Successfully."},
                        status=status.HTTP_200_OK)


@api_view(['PUT'])
def update_field_settings(req, form_id, field_id):
    """
    Update Field Settings
    """
    try:
        # Update field settings only for non deleted form
        form = Form.objects.filter(id=form_id).exclude(status=FORM_STATUS[0][0]).get()
    except Form.DoesNotExist:
        msg = "Invalid Form ID."
        return Response({"status": "error", "msg": msg}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Update field settings only for non deleted field
        field = FormField.objects.filter(id=field_id).filter(form_id=form_id).exclude(status=FORM_FIELD_STATUS[0][0]).get()
    except FormField.DoesNotExist:
        msg = "Invalid Form Field ID."
        return Response({"status": "error", "msg": msg}, status=status.HTTP_400_BAD_REQUEST)

    serializer = UpdateFieldSettingsSerializer(field, data=req.data, context={'field_id': field_id, 'form_id': form_id})

    if not serializer.is_valid():
        return Response({"status": "validation_error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    else:
        instance = serializer.save(is_field_settings_updated=True)

        field_type = field.field_type
        if field_type == FIELD_TYPES[5][0] or field_type == FIELD_TYPES[6][0] or field_type == FIELD_TYPES[7][0] or \
                field_type == FIELD_TYPES[12][0]:
            # Save Options for Dropdown, Radio, Checkbox, MultiSelect Checkbox fields
            options = serializer.validated_data.get('options', [])
            create_update_field_options(options, field)

        response_data = {'field': {}}

        response_data['field']['id'] = instance.id

        # Update Field Label In Gsheet
        # update_field_label_in_gsheet(old_field_label, new_field_label, form)
        # Todo

        return Response({"status": "success", "data": response_data, "msg": "Field Settings Updated Successfully."},
                        status=status.HTTP_200_OK)


@api_view(['DELETE'])
def delete_field(req, form_id, field_id):
    """
    Soft delete field
    """
    try:
        form = Form.objects.filter(id=form_id).exclude(status=FORM_STATUS[0][0]).get()
    except Form.DoesNotExist:
        msg = "Invalid Form ID."
        return Response({"status": "error", "msg": msg}, status=status.HTTP_400_BAD_REQUEST)

    try:
        field = form.form_fields.filter(id=field_id).exclude(status=FORM_FIELD_STATUS[0][0]).get()
    except FormField.DoesNotExist:
        msg = "Invalid Form Field ID."
        return Response({"status": "error", "msg": msg}, status=status.HTTP_400_BAD_REQUEST)

    #  Soft delete form field
    field.status = FORM_FIELD_STATUS[0][0]
    field.save()

    # Remove field from Gsheet
    # remove_field_from_gsheet()
    # Todo

    response_data = {'field': {}}

    response_data['field']['id'] = instance.id

    return Response({"status": "success", "data": response_data, "msg": "Form Field Deleted Successfully."},
                    status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAccountActive])
def dynamic_form_list(req):
    """
    Get list of active forms mapped to the account
    """
    page_size = DEFAULT_PAGE_SIZE
    response_data = {'list': {}}

    page = req.GET.get('page', 1)
    search_by_keyword = req.GET.get('search', None)

    account_id = req.headers['ZF-SECRET-KEY']

    # Get only active forms
    form_submissions = Form.objects.filter(account_id=account_id).filter(status=FORM_STATUS[1][0]).order_by('-created_date')

    if search_by_keyword:
        form_submissions = form_submissions.filter(Q(name__icontains=search_by_keyword))

    paginator = Paginator(form_submissions, page_size)
    page_obj = paginator.get_page(page)

    if int(page) > page_obj.paginator.num_pages:
        response_data['list']['per_page'] = 0
        response_data['list']['page'] = 0
        response_data['list']['total'] = 0
        response_data['list']['total_pages'] = 0
        response_data['list']['data'] = []
        response_data['list']['msg'] = "Invalid Page."

        return Response({"status": "error", "data": response_data}, status=status.HTTP_400_BAD_REQUEST)
    else:
        data = []
        # Loop each form
        for form in page_obj.object_list:
            single_row_entry = {}
            single_row_entry['id'] = form.id
            single_row_entry['name'] = form.name
            single_row_entry['description'] = form.description
            single_row_entry['status'] = form.status
            single_row_entry['status_text'] = FORM_STATUS_DETAILS[form.status]

            data.append(single_row_entry)

        response_data['list']['per_page'] = page_obj.paginator.per_page
        response_data['list']['page'] = page_obj.number
        response_data['list']['total'] = page_obj.paginator.count
        response_data['list']['total_pages'] = page_obj.paginator.num_pages
        response_data['list']['data'] = data

        return Response({"status": "success", "data": response_data}, status=status.HTTP_200_OK)



@api_view(['GET'])
def dynamic_form_fields_mapped_to_form_step(req, form_id, step_id=None):
    """
    Frontend(Dynamic Form) - Active Field mapped to Form Step
    """
    try:
        # Get only active Form
        form = Form.objects.filter(id=form_id).filter(status=FORM_STATUS[1][0]).get()
    except Form.DoesNotExist:
        data = "Invalid Form ID."
        return Response({"status": "error", "data": data}, status=status.HTTP_400_BAD_REQUEST)

    # Get all step mapped to form - Query not executed here
    form_steps = form.form_steps.filter(status=FORM_STEP_STATUS[1][0]).order_by('step_order')

    if step_id is None:
        # Query executed here
        first_form_step = form_steps.first()
        if not first_form_step:
            data = "No Form Step Available."
            return Response({"status": "error", "data": data}, status=status.HTTP_400_BAD_REQUEST)
        current_step = str(first_form_step.id)
    else:
        # Check if the "step id" received from request is valid
        try:
            form.form_steps.filter(id=step_id).filter(status=FORM_STEP_STATUS[1][0]).get()
        except FormStep.DoesNotExist:
            data = "Invalid Form Step ID."
            return Response({"status": "error", "data": data}, status=status.HTTP_400_BAD_REQUEST)

        current_step = step_id

    # Get only active fields
    form_fields = FormField.objects.filter(form_id=form_id).filter(form_step=current_step) \
        .filter(status=FORM_FIELD_STATUS[1][0]).order_by('field_order').prefetch_related('form_field_options')

    steps = []
    fields = []

    response_data = {'action': "#", 'form': {}, 'steps': steps, 'fields': fields}

    response_data['form']['id'] = form.id
    response_data['form']['name'] = form.name
    response_data['form']['description'] = form.description
    response_data['form']['class_name'] = form.class_name
    response_data['form']['success_msg'] = form.success_msg

    for form_step in form_steps:
        step = {}
        step['id'] = form_step.id
        step['name'] = form_step.name
        step['description'] = form_step.description

        if current_step == str(form_step.id):
            step['is_current_step'] = True
        else:
            step['is_current_step'] = False

        steps.append(step)

    for form_field in form_fields:
        field_details = {
            'field_id': form_field.id,
            'field_type': form_field.field_type,
            'field_order': form_field.field_order,
            'label': form_field.label,
            'class_name': form_field.field_size + " " + form_field.custom_class_name,
        }

        field_type = form_field.field_type

        if field_type != FIELD_TYPES[14][0] and field_type != FIELD_TYPES[15][0]:
            field_details['placeholder'] = form_field.placeholder
            field_details['validations'] = form_field.validation_rule

        if field_type == FIELD_TYPES[5][0] or field_type == FIELD_TYPES[6][0] or field_type == FIELD_TYPES[7][0] or \
                field_type == FIELD_TYPES[12][0]:
            # Get Options for Dropdown, Radio, Checkbox, MultiSelect Checkbox fields
            field_options = []

            form_field_options = form_field.form_field_options.filter(status=FORM_FIELD_OPTION_STATUS[1][0]).order_by('option_order').all()
            for form_field_option in form_field_options:
                field_option = {
                    'value': form_field_option.id,
                    'label': form_field_option.label,
                }
                field_options.append(field_option)

            field_details['options'] = field_options

        if field_type == FIELD_TYPES[0][0] or field_type == FIELD_TYPES[1][0] or field_type == FIELD_TYPES[3][0] or \
                field_type == FIELD_TYPES[4][0] or field_type == FIELD_TYPES[5][0]:
            # Text Box, Number, Email, Website URL, Dropdown
            field_details['field_format'] = form_field.field_format

        if field_type == FIELD_TYPES[14][0] or field_type == FIELD_TYPES[15][0]:
            # Heading, Paragraph
            field_details['content'] = form_field.content
            field_details['content_size'] = form_field.content_size
            field_details['content_alignment'] = form_field.content_alignment

        fields.append(field_details)

    response_data['fields'] = fields

    return Response({"status": "success", "data": response_data}, status=status.HTTP_200_OK)


@api_view(['POST'])
def submit_form(req, form_id, step_id, submission_id=None):
    """
    Frontend(Dynamic Form) - Submit Form
    """
    try:
        # Allow submit only for active form from frontend
        form = Form.objects.filter(id=form_id).filter(status=FORM_STATUS[1][0]).get()
    except Form.DoesNotExist:
        msg = "Invalid Form ID."
        return Response({"status": "error", "msg": msg}, status=status.HTTP_400_BAD_REQUEST)

    # Check if the "step id" received from request is valid
    try:
        current_step = form.form_steps.filter(id=step_id).filter(status=FORM_STEP_STATUS[1][0]).get()
        current_step_order = current_step.step_order
    except FormStep.DoesNotExist:
        msg = "Invalid Form Step ID."
        return Response({"status": "error", "msg": msg}, status=status.HTTP_400_BAD_REQUEST)

    # If Current Step Order greater than 1, Form Submission ID required
    if current_step_order > 1 and submission_id is None:
        msg = "Form Submission ID Required."
        return Response({"status": "error", "msg": msg}, status=status.HTTP_400_BAD_REQUEST)

    # Get only active fields mapped to the step
    form_fields = FormField.objects.filter(form_id=form_id).filter(form_step=step_id) \
        .filter(status=FORM_FIELD_STATUS[1][0])

    form_field_ids = []
    for form_field in form_fields:
        form_field_ids.append(form_field.id)

    # Validate all active fields mapped to the step
    validation = validate_form_fields(req, form_fields, req.data, step_id, submission_id)

    # Handle validation error & error
    if validation['status'] == 'validation_error' or  validation['status'] == 'error':
        return Response(validation, status=status.HTTP_400_BAD_REQUEST)

    # Handle validation success
    if submission_id is None:
        # Create Form Submission Entry
        form_submission = FormSubmission.objects.create(form=form)
    else:
        # Existing Form Submission Entry
        try:
            form_submission = FormSubmission.objects.filter(id=submission_id).get()
        except FormSubmission.DoesNotExist:
            msg = "Invalid Form Submission ID."
            return Response({"status": "error", "msg": msg}, status=status.HTTP_400_BAD_REQUEST)

    submission_reference = uuid.uuid4()

    form_data_for_gsheet = {}

    # Save form submission data against the form submission entry
    for form_data in req.data:
        form_data_key = form_data
        form_data_value = req.data[form_data]

        field_detail = FormField.objects.filter(id=form_data_key).filter(status=FORM_FIELD_STATUS[1][0]).first()

        # Save form submission data to respective column based on the field type
        if field_detail:
            form_submission_data = FormSubmissionData()
            form_submission_data.form_submission = form_submission
            form_submission_data.form_field = field_detail
            form_submission_data.form_field_type = field_detail.field_type
            form_submission_data.submission_reference = submission_reference

            if field_detail.field_type == FIELD_TYPES[0][0]:
                form_submission_data.text_field = form_data_value
            elif field_detail.field_type == FIELD_TYPES[1][0]:
                form_submission_data.text_field = form_data_value
            elif field_detail.field_type == FIELD_TYPES[2][0]:
                form_submission_data.text_field = form_data_value
            elif field_detail.field_type == FIELD_TYPES[3][0]:
                form_submission_data.text_field = form_data_value
            elif field_detail.field_type == FIELD_TYPES[4][0]:
                form_submission_data.text_field = form_data_value
            elif field_detail.field_type == FIELD_TYPES[5][0]:
                form_submission_data.dropdown_field = form_data_value
            elif field_detail.field_type == FIELD_TYPES[6][0]:
                form_submission_data.radio_field = form_data_value
            # elif field_detail.field_type == FIELD_TYPES[7][0]:
            #     form_submission_data.checkbox_field = form_data_value
            elif field_detail.field_type == FIELD_TYPES[8][0]:
                form_submission_data.text_field = form_data_value
            elif field_detail.field_type == FIELD_TYPES[9][0]:
                form_submission_data.text_field = form_data_value
            elif field_detail.field_type == FIELD_TYPES[10][0]:
                if validate_is_empty(form_data_value):
                    # if empty value provided for file
                    # Todo
                    pass
                else:
                    # if value provided for file
                    form_submission_data.file_field = form_data_value
            elif field_detail.field_type == FIELD_TYPES[11][0]:
                form_submission_data.text_field = form_data_value
            elif field_detail.field_type == FIELD_TYPES[12][0]:
                form_submission_data.multiselect_checkbox_field = form_data_value
            elif field_detail.field_type == FIELD_TYPES[13][0]:
                form_submission_data.text_field = form_data_value

            form_submission_data.save()

            #Gsheet
            if field_detail.field_type == FIELD_TYPES[12][0]:
                # Multi Checkbox
                _values = format_string_to_json_array(form_submission_data.multiselect_checkbox_field)
                if _values is not None:
                    _option_values = get_field_option_values(_values)
                    _option_values = ",".join(_option_values)
                    form_data_for_gsheet[field_detail.label] =  _option_values
                else:
                    form_data_for_gsheet[field_detail.label] = ""
            elif field_detail.field_type == FIELD_TYPES[10][0]:
                # File
                if form_submission_data.file_field:
                    form_data_for_gsheet[field_detail.label] = form_submission_data.file_field.url
                else:
                    form_data_for_gsheet[field_detail.label] = ""
            elif field_detail.field_type == FIELD_TYPES[6][0]:
                # Radio
                _value = form_submission_data.radio_field
                _option_value = get_field_option_value(_value)
                form_data_for_gsheet[field_detail.label] = _option_value
            elif field_detail.field_type == FIELD_TYPES[5][0]:
                    # Dropdown
                    _values = format_string_to_json_array(form_submission_data.dropdown_field)
                    _option_values = get_field_option_values(_values)
                    _option_values = ",".join(_option_values)
                    if _values is not None:
                        form_data_for_gsheet[field_detail.label] = _option_values
                    else:
                        form_data_for_gsheet[field_detail.label] = ""
            else:
                form_data_for_gsheet[field_detail.label] = form_data_value

    # Delete Last Entry Of Form Submission
    if submission_id:
        FormSubmissionData.objects.filter(form_submission=submission_id).filter(form_field__in=form_field_ids).exclude(
            submission_reference=submission_reference).delete()

    form_submission_status = form_submission.status

    if form_submission_status == FORM_SUBMISSION_STATUS[2][0]:
        # If the step is last step & if the status is "draft" update the form_submission_status to "active" & update to entry
        _status = FORM_SUBMISSION_STATUS[1][0]
    else:
        _status = FORM_SUBMISSION_STATUS[1][0]

    next_step_exist = FormStep.objects.filter(form=form_id).filter(step_order__gt=current_step_order).filter(status=FORM_STEP_STATUS[1][0]).exists()
    if not next_step_exist:
        form_submission_last_revision = form_submission.revision

        # Last Step
        form_submission_new_revision = form_submission_last_revision + 1
        form_submission.revision = form_submission_new_revision
        form_submission.status = FORM_SUBMISSION_STATUS[1][0]
        form_submission.save()

        if form_submission_last_revision == 1:
            _method = "save"
        else:
            _method = "update"

        # Event & Webhook - Form Submit
        event_data = {
            "event": "form.submit",
            "method": _method,
            "account": {"id": str(form.account.id), "meta_detail": form.account.meta_detail},
            "form": {"id": str(form.id), "meta_detail": form.meta_detail, "status": form.status, "status_text": FORM_STATUS_DETAILS[form.status]},
            "form_submission": {"id": str(form_submission.id), "revision": form_submission_last_revision, "is_last_step": True, "status": form_submission.status, "status_text": FORM_SUBMISSION_STATUS_DETAILS[form_submission.status]}
        }
        after_form_submit(event_data)

    # Send Form Data To Gsheet - On every form step submission
    send_form_data_to_gsheet(_method, form, str(form_submission.id), form_data_for_gsheet)

    response_data = {'submission_id': form_submission.id}
    return Response({"status": "success", "data": response_data, "msg": "Form Submitted Successfully."},
                    status=status.HTTP_200_OK)


def validate_form_fields(req, form_fields, req_data, step_id, submission_id):
    """
    Validate all fields mapped to the step, when submitting each form step
    """
    form_req_data = {}
    form_missing_fields = []
    field_labels = {}
    field_types = {}
    field_validation_rules = {}
    validation_errors = {}

    # Loop & format the request data
    for form_data in req_data:
        field_key = str(form_data)
        field_req_value = req_data[form_data]

        form_req_data[field_key] = field_req_value

    # Loop & get all the validation rules added for the fields
    for form_field in form_fields:
        field_key = str(form_field.id)
        field_label = form_field.label
        field_type = form_field.field_type
        field_validation_rule = form_field.validation_rule

        # if field is "dropdown, radio, multiselect checkbox"
        if field_type == FIELD_TYPES[5][0]:
            field_validation_rule.update({"dropdown": True})

        if field_type == FIELD_TYPES[6][0]:
            field_validation_rule.update({"radio": True})

        if field_type == FIELD_TYPES[12][0]:
            field_validation_rule.update({"multiselect_checkbox": True})

        field_labels[field_key] = field_label
        field_types[field_key] = field_type
        field_validation_rules[field_key] = field_validation_rule

        # Get list of fields missed on the request
        if field_key not in form_req_data:
            form_missing_fields.append(field_key)

    # Validate fields - Check if all the fields mapped for the step are present on the request
    if len(form_missing_fields) > 0:
        data = {}
        for form_missing_field in form_missing_fields:
            data[form_missing_field] = "This field is required."

        return {"status": "validation_error", "error_on": "current_step", "error_step_id": step_id,
                "data": data,
                "msg": "Some fields missed or wrongly provided on the request."}

    # Validate fields - Loop each request data & validate based on validation rules
    for data in form_req_data:
        field_key = data
        try:
            field_label = field_labels[field_key]
            field_validation_rule = field_validation_rules[field_key]
            field_value = form_req_data[field_key]
            field_type = field_types[field_key]
        except:
            return {"status": "error", "data": {"key": field_key}, "msg": "Invalid Field Key"}

        # Validate single field
        validation = validate_form_field(req, field_key, field_label, field_validation_rule, field_value, field_type, submission_id)
        if len(validation) != 0:
            # If single field has error
            validation_errors.update(validation)

    # Validate fields - If any of the fields mapped for the step has error
    if len(validation_errors) > 0:
        return {"status": "validation_error", "error_on": "current_step", "error_step_id": step_id, "data": validation_errors}

    return {"status": "success"}


def validate_form_field(req, field_key, field_label, field_validation_rule, field_value, field_type, submission_id):
    """
    Validate single field based on the validation rule
    """
    validation_error = {}

    if FIELD_RULES[0][0] in field_validation_rule:
        if field_validation_rule['required']:
            if field_type == FIELD_TYPES[10][0]:
                # If 'field_type' is file
                if submission_id:
                    # If has file already uploaded, skip required validation
                    previous_formsubmission_data = FormSubmissionData.objects.filter(form_submission=submission_id).filter(form_field_id=field_key).first()
                    if not previous_formsubmission_data:
                        error = validate_is_empty(field_value)
                        if error:
                            validation_error[field_key] = f"{field_label} may not be blank."
                            return validation_error
            else:
                # If 'field_type' is not file
                error = validate_is_empty(field_value)
                if error:
                    validation_error[field_key] = f"{field_label} may not be blank."
                    return validation_error


    if FIELD_RULES[10][0] in field_validation_rule:
        if field_value and field_validation_rule['max_selection']:
            max_selection_allowed = field_validation_rule.get('max_selection', 1)
            formatted_input = format_string_to_json_array(field_value)
            if formatted_input is None:
                validation_error[field_key] = f"{field_label} is invalid."
                return validation_error
            else:
                validate_min = field_validation_rule['required']
                validate_max = True
                error = validate_min_max_selection(formatted_input, max_selection_allowed, validate_min, validate_max)
                if error == 1:
                    validation_error[field_key] = f"Please select at least one choice."
                    return validation_error
                elif error == 2:
                    validation_error[field_key] = f"You already reached the maximum number of accepted choices({max_selection_allowed})."
                    return validation_error

    if FIELD_RULES[9][0] in field_validation_rule:
        if field_value and field_validation_rule['number']:
            decimal_places_allowed = field_validation_rule.get('decimal_places', 0)
            if not field_validation_rule['decimal']:
                # if field configured, not to have decimal places
                error = validate_is_number(field_value)
                if error:
                    validation_error[field_key] = f"{field_label} is invalid."
            else:
                formatted_field_value = parse_to_float(field_value)
                # if field configured, to have decimal - allow value with decimal & without decimal
                if formatted_field_value is None:
                    validation_error[field_key] = f"{field_label} is invalid."
                else:
                    if '.' in str(field_value):
                        # if field is decimal, check the decimal place is same as the decimal place configured
                        decimal_places = len(str(field_value).split(".")[1])
                        if decimal_places != decimal_places_allowed:
                            validation_error[field_key] = f"{field_label} should contain {decimal_places_allowed} decimal places."

            if validation_error:
                return validation_error

    if FIELD_RULES[1][0] in field_validation_rule:
        if field_value:
            minlength = field_validation_rule['minlength']
            error = validate_minlength(field_value, minlength)
            if error:
                validation_error[field_key] = f"{field_label} must contain atleast {minlength} characters."
                return validation_error

    if FIELD_RULES[2][0] in field_validation_rule:
        if field_value:
            maxlength = field_validation_rule['maxlength']
            error = validate_maxlength(field_value, maxlength)
            if error:
                validation_error[field_key] = f"{field_label} should not be greater than {maxlength} characters."
                return validation_error

    if FIELD_RULES[3][0] in field_validation_rule:
        if field_value:
            min_value = field_validation_rule['min']
            error = validate_min_value(field_value, min_value)
            if error:
                validation_error[field_key] = f"{field_label} should be equal or greater than {min_value}."
                return validation_error

    if FIELD_RULES[4][0] in field_validation_rule:
        if field_value:
            max_value = field_validation_rule['max']
            error = validate_max_value(field_value, max_value)
            if error:
                validation_error[field_key] = f"{field_label} should be equal or less than {max_value}."
                return validation_error

    if FIELD_RULES[5][0] in field_validation_rule:
        if field_value  and field_validation_rule['email']:
            error = validate_is_email(field_value)
            if error:
                validation_error[field_key] = f"{field_label} is invalid."
                return validation_error

    if FIELD_RULES[6][0] in field_validation_rule:
        if field_value and field_validation_rule['url']:
            error = validate_is_url(field_value)
            if error:
                validation_error[field_key] = f"{field_label} is invalid."
                return validation_error

    if FIELD_RULES[7][0] in field_validation_rule:
        if field_value and field_validation_rule['date']:
            date_format_allowed = field_validation_rule.get('date_format', '')
            error = validate_is_date(field_value, date_format_allowed)
            if error:
                validation_error[field_key] = f"{field_label} is invalid."
                return validation_error

    if FIELD_RULES[8][0] in field_validation_rule:
        if field_value and field_validation_rule['unique']:
            error = validate_is_unique(field_value, field_key, field_type, submission_id)
            if error:
                validation_error[field_key] = f"{field_label} has been already taken."
                return validation_error

    if FIELD_RULES[11][0] in field_validation_rule:
        if field_validation_rule['file']:
            _validate_file = True

            if field_validation_rule['required']:
               # if the field is required - no value submitted but already as a value, skip this validation rule
               if not field_value and submission_id:
                    previous_formsubmission_data = FormSubmissionData.objects.filter(
                            form_submission=submission_id).filter(form_field_id=field_key).first()
                    if previous_formsubmission_data:
                        _validate_file = False
            else:
                # if the field is not required - no value submitted skip this validation rule
                if not field_value:
                    _validate_file = False

            if _validate_file:
                # if the field has value
                error = validate_is_file(field_key, req)
                if error:
                    # if file added is not valid file
                    validation_error[field_key] = "No file uploaded."
                    return validation_error
                else:
                    # if file added is valid file, validate extension
                    file_extensions_allowed = field_validation_rule.get('file_extensions_allowed', [])
                    invalid_file_error = validate_file_extension(field_value, file_extensions_allowed)
                    if invalid_file_error:
                        file_extensions_allowed = FIELD_RULES_FILE_FORMAT_ALLOWED
                        allowed_file_extensions = ", "
                        allowed_file_extensions = allowed_file_extensions.join(file_extensions_allowed)
                        validation_error[field_key] = f"Upload only {allowed_file_extensions} file."
                        return validation_error
                    else:
                        # if file added is with valid extension, validate file size
                        file_max_size_allowed = field_validation_rule.get('file_max_size_mb', 0)
                        invalid_file_size_error = validate_file_size(field_value, file_max_size_allowed)
                        if invalid_file_size_error:
                            # if file's size is greater than the allowed file size
                            validation_error[field_key] = f"Upload file smaller than {file_max_size_allowed}MB."
                            return validation_error

    if FIELD_RULES[12][0] in field_validation_rule:
        if field_value and field_validation_rule['time']:
            time_format_allowed = field_validation_rule.get('time_format', '')
            error = validate_is_time(field_value, time_format_allowed)
            if error:
                validation_error[field_key] = f"{field_label} is invalid."
                return validation_error

    return validation_error

def parse_to_float(value):
    """
    Parse the value to float
    """
    try:
        parsed_value = float(value)
    except:
        parsed_value = None

    return parsed_value

def format_string_to_json_array(string):
    """
    Format string to json array
    """
    formatted_string = None
    try:
        json_value = json.loads(string)
        if type(json_value) is list:
            formatted_string = json_value
        else:
            formatted_string = None
    except:
        formatted_string = None

    return formatted_string

def create_update_field_options(options, field_instance):
    """
    Create or Update Field Options
    """
    options_to_create = []
    options_to_edit = {}
    options_to_edit__id = []

    # loop all the form field options from request
    for option in options:
        id = option.get('value', '')
        label = option.get('label', '')
        order = option.get('order', 0)
        if id:
            options_to_edit[id] = {'label': label, 'order': order}
            options_to_edit__id.append(id)
        else:
            options_to_create.append(option)

    # Edit or Delete - Option

    form_field_options = field_instance.form_field_options.filter(status=FORM_FIELD_OPTION_STATUS[1][0])

    # loop all the form field options from DB with status "active", update or soft delete
    for form_field_option in form_field_options:
        option__id = str(form_field_option.id) # DB - Option ID

        if option__id in options_to_edit__id:
            req__option = options_to_edit[option__id] #get option received from request
            req__option_label = req__option['label']
            req__option_order = req__option['order']
            # Update Label & Order if modified
            if form_field_option.label != req__option_label or form_field_option.option_order != req__option_order:
                form_field_option.label = req__option_label
                form_field_option.option_order = req__option_order
                form_field_option.save()
        else:
            # Soft Delete Option
            form_field_option.status = FORM_FIELD_OPTION_STATUS[0][0]
            form_field_option.save()

    # Bulk Create - Option
    field_option_objects = []

    for option in options_to_create:
        field_option = FormFieldOption(
                            label = option['label'],
                            option_order = option['order'],
                            form_field = field_instance
                        )
        field_option_objects.append(field_option)

    FormFieldOption.objects.bulk_create(field_option_objects)

def get_field_option_values(option_ids = []):
    """
   Get Field Option Values - If option is non deleted
    """
    option_values = []

    field_options = FormFieldOption.objects.filter(id__in=option_ids).filter(status=FORM_FIELD_OPTION_STATUS[1][0])

    if field_options:
        for field_option in field_options:
            option_values.append(field_option.label)

    return option_values

def get_field_option_value(option_id = ""):
    """
   Get Field Option Value - If option is non deleted
    """
    option_value = ""

    field_option = FormFieldOption.objects.filter(id=option_id).filter(status=FORM_FIELD_OPTION_STATUS[1][0]).first()

    if field_option:
        option_value = field_option.label

    return option_value