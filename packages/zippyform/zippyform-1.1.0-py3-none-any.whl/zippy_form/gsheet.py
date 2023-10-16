from django.conf import settings

import gspread
from oauth2client.service_account import ServiceAccountCredentials

gsheet_perm_type = "user"
gsheet_role = "writer"


def gsheet_init():
    """
    Gsheet - Initialize
    """
    try:
        # Check if form submission is allowed to sync on Gsheet
        sync_form_submission_to_gsheet = settings.ZF_GSHEET_SYNC_FORM_SUBMISSION
    except:
        sync_form_submission_to_gsheet = False

    if sync_form_submission_to_gsheet:
        try:
            # Check if user provided Gsheet credentials in settings file
            gsheet_credentials = settings.ZF_GSHEET_CREDENTIALS
        except:
            gsheet_credentials = None

        if gsheet_credentials:
            try:
                # Check if user provided Gsheet credentials in settings file are valid
                credentials = ServiceAccountCredentials.from_json_keyfile_dict(gsheet_credentials)

                # Authenticate with Google Sheets API
                gc = gspread.authorize(credentials)

                return gc
            except:
                pass

    return None


def create_gsheet_map_form(form):
    """
    Create Gsheet & map to form
    """
    gc = gsheet_init()

    if gc:
        # Name of the Google Sheet to create
        sheet_name = str(form.id)

        try:
            # Create Gsheet
            if form.account.admin_email:
                spreadsheet = gc.create(sheet_name)
                spreadsheet.share(form.account.admin_email, perm_type=gsheet_perm_type, role=gsheet_role)

                # Save Gsheet URL to the form
                if spreadsheet.url:
                    form.gsheet_url = spreadsheet.url
                    form.save()
        except gspread.exceptions.APIError:
            pass


def open_gsheet(form):
    """
    Open Gsheet
    """
    spreadsheet = None

    gc = gsheet_init()
    if gc:
        try:
            # Try to open the Google Sheet by its url
            spreadsheet = gc.open_by_url(form.gsheet_url)
        except gspread.exceptions.SpreadsheetNotFound as e:
            # If the sheet doesn't exist
            spreadsheet = None

    return spreadsheet


def add_field_labels_to_gsheet(fields, form):
    """
    Add fields labels to Gsheet
    """
    gsheet_url = form.gsheet_url
    if gsheet_url and len(fields) > 0:
        spreadsheet = open_gsheet(form)
        if spreadsheet:
            # Select the worksheet where you want to send data (by default, the first sheet)
            worksheet = spreadsheet.get_worksheet(0)

            # Define the row index where you want to add the column
            heading_label_row_index = 1

            # ---- Heading Label ---- #
            # Get the current headers from the worksheet
            current_headers = worksheet.row_values(heading_label_row_index)
            current_headers_count = len(current_headers)

            heading_label_new_column_start_index = current_headers_count

            # Insert new columns
            if current_headers_count == 0:
                # If no headers present
                start_column = 0

                new_column_values = ['Submission ID']

                worksheet.format('A1:ZZZ1', {'textFormat': {'bold': True}})
            else:
                # If headers already present
                start_column = heading_label_new_column_start_index

                new_column_values = []

            # form the fields & save to "new_column_values"
            for field in fields:
                new_column_values.append(field['label'])

            for i, value in enumerate(new_column_values, start=start_column):
                worksheet.update_cell(heading_label_row_index, i + 1, value)


def update_field_label_in_gsheet(old_field_label, new_field_label, form):
    """
    Update field label in Gsheet
    """
    pass


def remove_field_from_gsheet(field_label, form):
    """
    Remove field from Gsheet
    """
    pass


def send_form_data_to_gsheet(method, form, form_submission_id, form_submission_data):
    """
    Send form data to Gsheet
    """
    gsheet_url = form.gsheet_url
    if gsheet_url:
        spreadsheet = open_gsheet(form)
        if spreadsheet:
            # Select the worksheet where you want to send data (by default, the first sheet)
            worksheet = spreadsheet.get_worksheet(0)

            # Get the header row from the worksheet
            header_row_values = worksheet.row_values(1)

            if header_row_values:
                # If it has Header Row

                if method == "save":
                    form_submission_data['Submission ID'] = form_submission_id

                    new_row = [form_submission_data.get(header, "") for header in header_row_values]
                    worksheet.append_row(new_row)
                else:
                    # Get all the submission id from column 1
                    submission_id_column_values = worksheet.col_values(1)

                    if form_submission_id in submission_id_column_values:
                        # Get row index which we need to update
                        row_index = submission_id_column_values.index(form_submission_id) + 1
                        for key, value in form_submission_data.items():
                            worksheet.update_cell(row_index, header_row_values.index(key) + 1, value)


def remove_form_data_from_gsheet(form, form_submission_id):
    """
    Remove form data from Gsheet
    """
    pass
