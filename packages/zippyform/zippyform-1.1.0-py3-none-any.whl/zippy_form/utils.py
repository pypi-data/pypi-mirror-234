ACCOUNT_STATUS = (
    ('deleted', 'Deleted'),
    ('active', 'Active'),
)

ACCOUNT_STATUS_DETAILS = {
    'deleted': 'Deleted',
    'active': 'Active',
}

FORM_STATUS = (
    ('deleted', 'Deleted'),
    ('active', 'Active'),
    ('in_active', 'InActive'),
    ('draft', 'Draft'),
)

FORM_STATUS_DETAILS = {
    'deleted': 'Deleted',
    'active': 'Active',
    'in_active': 'InActive',
    'draft': 'Draft',
}

FORM_STEP_STATUS = (
    ('deleted', 'Deleted'),
    ('active', 'Active'),
)

FORM_STEP_STATUS_DETAILS = {
    'deleted': 'Deleted',
    'active': 'Active',
}


FORM_FIELD_STATUS = (
    ('deleted', 'Deleted'),
    ('active', 'Active'),
    ('in_active', 'InActive'),
    ('draft', 'Draft'),
)

FORM_FIELD_DETAILS = {
    'deleted': 'Deleted',
    'active': 'Active',
    'in_active': 'InActive',
    'draft': 'Draft',
}

FORM_FIELD_OPTION_STATUS = (
    ('deleted', 'Deleted'),
    ('active', 'Active'),
)


FORM_SUBMISSION_STATUS = (
    ('deleted', 'Deleted'),
    ('active', 'Active'),
    ('draft', 'Draft'),
)

FORM_SUBMISSION_STATUS_DETAILS = {
    'deleted': 'Deleted',
    'active': 'Active',
    'draft': 'Draft',
}

FIELD_SIZE = (
    ('col-md-12', 'Large'),
    ('col-md-6', 'Medium'),
    ('col-md-4', 'Small'),
)

FIELD_TYPES = (
    ('text_box', 'Text Box'),
    ('website_url', 'Website URL'),
    ('text_area', 'TextArea'),
    ('number', 'Number'),
    ('email', 'Email'),
    ('dropdown', 'Dropdown'),
    ('radio', 'Radio'),
    ('checkbox', 'Checkbox'),
    ('date', 'Date'),
    ('time', 'Time'),
    ('file', 'File Upload'),
    ('short_text_area', 'Short TextArea'),
    ('multiselect_checkbox', 'MultiSelect Checkbox'),
    ('hidden', 'Hidden'),
    ('heading', 'Heading'),
    ('paragraph', 'Paragraph'),
)

FIELD_RULES = (
    ('required', 'Required'),
    ('minlength', 'MinLength'),
    ('maxlength', 'MaxLength'),
    ('min', 'Min'),
    ('max', 'Max'),
    ('email', 'Email'),
    ('url', 'URL'),
    ('date', 'Date'),
    ('unique', 'Unique'),
    ('number', 'Number'),
    ('max_selection', 'Max Selection'),
    ('file', 'File'),
    ('time', 'Time'),
)

FIELD_RULES_DATE_FORMAT_ALLOWED = {
    'm-d-Y': '%m-%d-%Y',
    'd-m-Y': '%d-%m-%Y'
}

FIELD_RULES_TIME_FORMAT_ALLOWED = {
    '12': '%I:%M %p',
    '24': '%H:%M'
}

FIELD_RULES_FILE_FORMAT_ALLOWED = ["jpg", "jpeg", "png", "doc", "pdf"]