from rest_framework import serializers
from jsonschema import validate, ValidationError
from django.conf import settings

from zippy_form.models import FormStep, FormField, Form, Account
from zippy_form.utils import FIELD_TYPES, FIELD_RULES_DATE_FORMAT_ALLOWED, FIELD_RULES_TIME_FORMAT_ALLOWED, FORM_STATUS, \
    FORM_FIELD_STATUS
from zippy_form.validation_rule_schema import get_text_box_field_validation_rule_schema, \
    get_textarea_field_validation_rule_schema, get_website_url_field_validation_rule_schema, \
    get_short_textarea_field_validation_rule_schema, get_number_field_validation_rule_schema, \
    get_email_field_validation_rule_schema, get_date_field_validation_rule_schema, \
    get_time_field_validation_rule_schema, get_dropdown_field_validation_rule_schema, \
    get_radio_field_validation_rule_schema, get_multiselect_checkbox_field_validation_rule_schema, \
    get_file_field_validation_rule_schema, get_hidden_field_validation_rule_schema


class AccountSerializer(serializers.ModelSerializer):
    def validate_admin_email(self, value):
        if not value:
            raise serializers.ValidationError("This field may not be blank.")
        return value

    def validate(self, attrs):
        admin_email_field = attrs.get('admin_email', None)

        if admin_email_field is None:
            raise serializers.ValidationError({"admin_email": ["This field is required."]})

        return attrs

    class Meta:
        model = Account
        fields = ['id', 'name', 'admin_email', 'meta_detail']


class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form
        fields = ['id', 'name', 'meta_detail']


class FormStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormStep
        fields = ['id', 'name', 'form']

    def validate_form(self, attrs):
        if attrs.status == FORM_STATUS[0][0]:
            raise serializers.ValidationError('Invalid Form ID.')

        return attrs

    def create(self, validated_data):
        step_order = 1
        last_form_step = FormStep.objects.filter(form_id=validated_data['form']).order_by('-step_order').first()
        if last_form_step:
            last_form_step_order = last_form_step.step_order
            step_order = last_form_step_order + 1

        validated_data['step_order'] = step_order
        return FormStep.objects.create(**validated_data)


class MapFieldToFormStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormField
        fields = ['id', 'field_type', 'form', 'form_step', 'field_order']


class ReOrderFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormField
        fields = ['id', 'field_order']


class UpdateFieldSettingsSerializer(serializers.ModelSerializer):
    def validate_validation_rule(self, value):
        if not value:
            raise serializers.ValidationError("Invalid Validation Rule.")

        filed_type = self.instance.field_type
        # print(filed_type)

        schema = None

        if filed_type == FIELD_TYPES[0][0]:
            schema = get_text_box_field_validation_rule_schema()
        elif filed_type == FIELD_TYPES[1][0]:
            schema = get_website_url_field_validation_rule_schema()
        elif filed_type == FIELD_TYPES[2][0]:
            schema = get_textarea_field_validation_rule_schema()
        elif filed_type == FIELD_TYPES[3][0]:
            schema = get_number_field_validation_rule_schema()
        elif filed_type == FIELD_TYPES[4][0]:
            schema = get_email_field_validation_rule_schema()
        elif filed_type == FIELD_TYPES[5][0]:
            schema = get_dropdown_field_validation_rule_schema()
        elif filed_type == FIELD_TYPES[6][0]:
            schema = get_radio_field_validation_rule_schema()
        # elif filed_type == FIELD_TYPES[7][0]:
        #     schema = get_radio_field_validation_rule_schema()
        elif filed_type == FIELD_TYPES[8][0]:
            schema = get_date_field_validation_rule_schema()
        elif filed_type == FIELD_TYPES[9][0]:
            schema = get_time_field_validation_rule_schema()
        elif filed_type == FIELD_TYPES[10][0]:
            schema = get_file_field_validation_rule_schema()
        elif filed_type == FIELD_TYPES[11][0]:
            schema = get_short_textarea_field_validation_rule_schema()
        elif filed_type == FIELD_TYPES[12][0]:
            schema = get_multiselect_checkbox_field_validation_rule_schema()
        elif filed_type == FIELD_TYPES[13][0]:
            schema = get_hidden_field_validation_rule_schema()

        if schema:
            try:
                validate(value, schema)
            except ValidationError as e:
                # print("Schema Error: ", e)
                raise serializers.ValidationError("Invalid Validation Rule.")

            if filed_type == FIELD_TYPES[8][0]:
                # additional validation for date field
                if value['date']:
                    date_format = value['date_format']
                    field_rules_date_format_allowed = FIELD_RULES_DATE_FORMAT_ALLOWED.keys()
                    if date_format not in field_rules_date_format_allowed:
                        allowed_date_format = ", "
                        allowed_date_format = allowed_date_format.join(field_rules_date_format_allowed)
                        msg = f"Only {allowed_date_format} allowed for date format"
                        raise serializers.ValidationError(msg)
            elif filed_type == FIELD_TYPES[9][0]:
                # additional validation for time field
                if value['time']:
                    time_format = value['time_format']
                    field_rules_time_format_allowed = FIELD_RULES_TIME_FORMAT_ALLOWED.keys()
                    if time_format not in field_rules_time_format_allowed:
                        allowed_time_format = ", "
                        allowed_time_format = allowed_time_format.join(field_rules_time_format_allowed)
                        msg = f"Only {allowed_time_format} hrs allowed for time format"
                        raise serializers.ValidationError(msg)

        return value

    def validate_field_format(self, value):
        if not value:
            raise serializers.ValidationError("This field may not be blank.")

        # input_group_icon = []
        # if hasattr(settings, 'ZF_INPUT_GROUP_ICONS'):
        #     _input_group_icon = settings.ZF_INPUT_GROUP_ICONS
        #     if type(_input_group_icon) == list:
        #         input_group_icon = _input_group_icon

        schema = {
            "type": "object",
            "properties": {
                "field_format": {
                    "type": "string",
                    "enum": ["default", "input_group"]
                },
                "input_group_icon": {
                    "type": "string",
                },
                "input_group_icon_position": {
                    "type": "string",
                    "enum": ["start", "end"]
                },
            },
            "required": ["field_format"],
            "additionalProperties": False
        }

        try:
            validate(value, schema)
        except ValidationError as e:
            # print("Schema Error: ", e)
            raise serializers.ValidationError("Invalid Format.")

        return value

    def validate_options(self, value):
        if not value:
            raise serializers.ValidationError("This field may not be blank.")

        schema = {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "value": {"type": "string"},
                    "label": {"type": "string"},
                    "order": {"type": "integer", "minimum": 0}
                },
                "required": ["value", "label", "order"],
                "additionalProperties": False
            }
        }

        try:
            validate(value, schema)
        except ValidationError as e:
            # print("Schema Error: ", e)
            raise serializers.ValidationError("Invalid Format.")

        return value

    def validate_content(self, value):
        if not value:
            raise serializers.ValidationError("This field may not be blank.")

        return value

    def validate_content_size(self, value):
        if not value:
            raise serializers.ValidationError("This field may not be blank.")

        allowed_content_size = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p']

        if value not in allowed_content_size:
            allowed_content_size_msg = ", "
            allowed_content_size_msg = allowed_content_size_msg.join(allowed_content_size)
            raise serializers.ValidationError("Only " + allowed_content_size_msg + " allowed.")

        return value

    def validate_content_alignment(self, value):
        if not value:
            raise serializers.ValidationError("This field may not be blank.")

        allowed_content_alignment = ['start', 'center', 'end']

        if value not in allowed_content_alignment:
            allowed_content_alignment_msg = ", "
            allowed_content_alignment_msg = allowed_content_alignment_msg.join(allowed_content_alignment)
            raise serializers.ValidationError("Only " + allowed_content_alignment_msg + " allowed.")

        return value

    def validate_label(self, value):
        try:
            unique_validation = settings.ZF_IS_FIELD_LABEL_UNIQUE
        except:
            unique_validation = True
        if unique_validation:
            is_duplicate = FormField.objects.filter(label=value, form__id=self.context.get('form_id')).exclude(
                id=self.context.get('field_id')).exclude(status=FORM_FIELD_STATUS[0][0]).exists()
            if is_duplicate:
                raise serializers.ValidationError("This field must be unique.")
        return value

    def validate(self, attrs):
        label_field = attrs.get('label', None)
        field_size_field = attrs.get('field_size', None)
        placeholder_field = attrs.get('placeholder', None)
        custom_class_name_field = attrs.get('custom_class_name', None)
        validation_rule_field = attrs.get('validation_rule', None)
        field_format_field = attrs.get('field_format', None)
        is_mandatory_field = attrs.get('is_mandatory', None)
        options_field = attrs.get('options', None)
        is_unique_field = attrs.get('is_unique', None)
        content_field = attrs.get('content', None)
        content_size_field = attrs.get('content_size', None)
        content_alignment_field = attrs.get('content_alignment', None)

        errors = {}

        field_type = self.instance.field_type

        if field_size_field is None:
            errors["field_size"] = ["This field is required."]
        if custom_class_name_field is None:
            errors["custom_class_name"] = ["This field is required."]
        if is_mandatory_field is None:
            errors["is_mandatory"] = ["This field is required."]

        if field_type == FIELD_TYPES[0][0]:
            if label_field is None:
                errors["label"] = ["This field is required"]
            if placeholder_field is None:
                errors["placeholder"] = ["This field is required."]
            if validation_rule_field is None:
                errors["validation_rule"] = ["This field is required."]
            if field_format_field is None:
                errors["field_format"] = ["This field is required."]
            if options_field is not None:
                errors["options"] = ["Options not allowed for this field type."]
            if content_field is not None:
                errors["content"] = ["Content not allowed for this field type."]
            if content_size_field is not None:
                errors["content_size"] = ["Content Size not allowed for this field type."]
            if content_alignment_field is not None:
                errors["content_alignment"] = ["Content Alignment not allowed for this field type."]

        if field_type == FIELD_TYPES[1][0]:
            if label_field is None:
                errors["label"] = ["This field is required"]
            if placeholder_field is None:
                errors["placeholder"] = ["This field is required."]
            if validation_rule_field is None:
                errors["validation_rule"] = ["This field is required."]
            if field_format_field is None:
                errors["field_format"] = ["This field is required."]
            if options_field is not None:
                errors["options"] = ["Options not allowed for this field type."]
            if content_field is not None:
                errors["content"] = ["Content not allowed for this field type."]
            if content_size_field is not None:
                errors["content_size"] = ["Content Size not allowed for this field type."]
            if content_alignment_field is not None:
                errors["content_alignment"] = ["Content Alignment not allowed for this field type."]

        if field_type == FIELD_TYPES[2][0]:
            if label_field is None:
                errors["label"] = ["This field is required"]
            if placeholder_field is None:
                errors["placeholder"] = ["This field is required."]
            if validation_rule_field is None:
                errors["validation_rule"] = ["This field is required."]
            if field_format_field is not None:
                errors["field_format"] = ["Field Format not allowed for this field type."]
            if options_field is not None:
                errors["options"] = ["Options not allowed for this field type."]
            if content_field is not None:
                errors["content"] = ["Content not allowed for this field type."]
            if content_size_field is not None:
                errors["content_size"] = ["Content Size not allowed for this field type."]
            if content_alignment_field is not None:
                errors["content_alignment"] = ["Content Alignment not allowed for this field type."]

        if field_type == FIELD_TYPES[3][0]:
            if label_field is None:
                errors["label"] = ["This field is required"]
            if placeholder_field is None:
                errors["placeholder"] = ["This field is required."]
            if validation_rule_field is None:
                errors["validation_rule"] = ["This field is required."]
            if field_format_field is None:
                errors["field_format"] = ["This field is required."]
            if options_field is not None:
                errors["options"] = ["Options not allowed for this field type."]
            if content_field is not None:
                errors["content"] = ["Content not allowed for this field type."]
            if content_size_field is not None:
                errors["content_size"] = ["Content Size not allowed for this field type."]
            if content_alignment_field is not None:
                errors["content_alignment"] = ["Content Alignment not allowed for this field type."]

        if field_type == FIELD_TYPES[4][0]:
            if label_field is None:
                errors["label"] = ["This field is required"]
            if placeholder_field is None:
                errors["placeholder"] = ["This field is required."]
            if validation_rule_field is None:
                errors["validation_rule"] = ["This field is required."]
            if field_format_field is None:
                errors["field_format"] = ["This field is required."]
            if options_field is not None:
                errors["options"] = ["Options not allowed for this field type."]
            if content_field is not None:
                errors["content"] = ["Content not allowed for this field type."]
            if content_size_field is not None:
                errors["content_size"] = ["Content Size not allowed for this field type."]
            if content_alignment_field is not None:
                errors["content_alignment"] = ["Content Alignment not allowed for this field type."]

        if field_type == FIELD_TYPES[5][0]:
            if label_field is None:
                errors["label"] = ["This field is required"]
            if placeholder_field is None:
                errors["placeholder"] = ["This field is required."]
            if validation_rule_field is None:
                errors["validation_rule"] = ["This field is required."]
            if field_format_field is None:
                errors["field_format"] = ["This field is required."]
            if options_field is None:
                errors["options"] = ["This field is required."]
            if is_unique_field:
                errors["is_unique"] = ["Unique Validation not allowed for this field type."]
            if content_field is not None:
                errors["content"] = ["Content not allowed for this field type."]
            if content_size_field is not None:
                errors["content_size"] = ["Content Size not allowed for this field type."]
            if content_alignment_field is not None:
                errors["content_alignment"] = ["Content Alignment not allowed for this field type."]

        if field_type == FIELD_TYPES[6][0]:
            if label_field is None:
                errors["label"] = ["This field is required"]
            if placeholder_field is None:
                errors["placeholder"] = ["This field is required."]
            if validation_rule_field is None:
                errors["validation_rule"] = ["This field is required."]
            if field_format_field is not None:
                errors["field_format"] = ["Field Format not allowed for this field type."]
            if options_field is None:
                errors["options"] = ["This field is required."]
            if content_field is not None:
                errors["content"] = ["Content not allowed for this field type."]
            if content_size_field is not None:
                errors["content_size"] = ["Content Size not allowed for this field type."]
            if content_alignment_field is not None:
                errors["content_alignment"] = ["Content Alignment not allowed for this field type."]

        if field_type == FIELD_TYPES[7][0]:
            if label_field is None:
                errors["label"] = ["This field is required"]
            if placeholder_field is None:
                errors["placeholder"] = ["This field is required."]
            if validation_rule_field is None:
                errors["validation_rule"] = ["This field is required."]
            if field_format_field is not None:
                errors["field_format"] = ["Field Format not allowed for this field type."]
            if options_field is None:
                errors["options"] = ["This field is required."]
            if content_field is not None:
                errors["content"] = ["Content not allowed for this field type."]
            if content_size_field is not None:
                errors["content_size"] = ["Content Size not allowed for this field type."]
            if content_alignment_field is not None:
                errors["content_alignment"] = ["Content Alignment not allowed for this field type."]

        if field_type == FIELD_TYPES[8][0]:
            if label_field is None:
                errors["label"] = ["This field is required"]
            if placeholder_field is None:
                errors["placeholder"] = ["This field is required."]
            if validation_rule_field is None:
                errors["validation_rule"] = ["This field is required."]
            if field_format_field is not None:
                errors["field_format"] = ["Field Format not allowed for this field type."]
            if options_field is not None:
                errors["options"] = ["Options not allowed for this field type."]
            if content_field is not None:
                errors["content"] = ["Content not allowed for this field type."]
            if content_size_field is not None:
                errors["content_size"] = ["Content Size not allowed for this field type."]
            if content_alignment_field is not None:
                errors["content_alignment"] = ["Content Alignment not allowed for this field type."]

        if field_type == FIELD_TYPES[9][0]:
            if label_field is None:
                errors["label"] = ["This field is required"]
            if placeholder_field is None:
                errors["placeholder"] = ["This field is required."]
            if validation_rule_field is None:
                errors["validation_rule"] = ["This field is required."]
            if field_format_field is not None:
                errors["field_format"] = ["Field Format not allowed for this field type."]
            if options_field is not None:
                errors["options"] = ["Options not allowed for this field type."]
            if content_field is not None:
                errors["content"] = ["Content not allowed for this field type."]
            if content_size_field is not None:
                errors["content_size"] = ["Content Size not allowed for this field type."]
            if content_alignment_field is not None:
                errors["content_alignment"] = ["Content Alignment not allowed for this field type."]

        if field_type == FIELD_TYPES[10][0]:
            if label_field is None:
                errors["label"] = ["This field is required"]
            if placeholder_field is None:
                errors["placeholder"] = ["This field is required."]
            if validation_rule_field is None:
                errors["validation_rule"] = ["This field is required."]
            if field_format_field is not None:
                errors["field_format"] = ["Field Format not allowed for this field type."]
            if options_field is not None:
                errors["options"] = ["Options not allowed for this field type."]
            if is_unique_field:
                errors["is_unique"] = ["Unique Validation not allowed for this field type."]
            if content_field is not None:
                errors["content"] = ["Content not allowed for this field type."]
            if content_size_field is not None:
                errors["content_size"] = ["Content Size not allowed for this field type."]
            if content_alignment_field is not None:
                errors["content_alignment"] = ["Content Alignment not allowed for this field type."]

        if field_type == FIELD_TYPES[11][0]:
            if label_field is None:
                errors["label"] = ["This field is required"]
            if placeholder_field is None:
                errors["placeholder"] = ["This field is required."]
            if validation_rule_field is None:
                errors["validation_rule"] = ["This field is required."]
            if field_format_field is not None:
                errors["field_format"] = ["Field Format not allowed for this field type."]
            if options_field is not None:
                errors["options"] = ["Options not allowed for this field type."]
            if content_field is not None:
                errors["content"] = ["Content not allowed for this field type."]
            if content_size_field is not None:
                errors["content_size"] = ["Content Size not allowed for this field type."]
            if content_alignment_field is not None:
                errors["content_alignment"] = ["Content Alignment not allowed for this field type."]

        if field_type == FIELD_TYPES[12][0]:
            if label_field is None:
                errors["label"] = ["This field is required"]
            if placeholder_field is None:
                errors["placeholder"] = ["This field is required."]
            if validation_rule_field is None:
                errors["validation_rule"] = ["This field is required."]
            if field_format_field is not None:
                errors["field_format"] = ["Field Format not allowed for this field type."]
            if options_field is None:
                errors["options"] = ["This field is required."]
            if is_unique_field:
                errors["is_unique"] = ["Unique Validation not allowed for this field type."]
            if content_field is not None:
                errors["content"] = ["Content not allowed for this field type."]
            if content_size_field is not None:
                errors["content_size"] = ["Content Size not allowed for this field type."]
            if content_alignment_field is not None:
                errors["content_alignment"] = ["Content Alignment not allowed for this field type."]

        if field_type == FIELD_TYPES[13][0]:
            if label_field is None:
                errors["label"] = ["This field is required"]
            if placeholder_field is None:
                errors["placeholder"] = ["This field is required."]
            if validation_rule_field is None:
                errors["validation_rule"] = ["This field is required."]
            if field_format_field is not None:
                errors["field_format"] = ["Field Format not allowed for this field type."]
            if options_field is not None:
                errors["options"] = ["Options not allowed for this field type."]
            if content_field is not None:
                errors["content"] = ["Content not allowed for this field type."]
            if content_size_field is not None:
                errors["content_size"] = ["Content Size not allowed for this field type."]
            if content_alignment_field is not None:
                errors["content_alignment"] = ["Content Alignment not allowed for this field type."]

        if field_type == FIELD_TYPES[14][0]:
            if label_field is None:
                errors["label"] = ["This field is required"]
            if placeholder_field is not None:
                errors["placeholder"] = ["Placeholder not allowed for this field type."]
            if validation_rule_field is not None:
                errors["validation_rule"] = ["Validation Rule not allowed for this field type."]
            if field_format_field is not None:
                errors["field_format"] = ["Field Format not allowed for this field type."]
            if options_field is not None:
                errors["options"] = ["Options not allowed for this field type."]
            if is_unique_field:
                errors["is_unique"] = ["Unique Validation not allowed for this field type."]
            if content_field is None:
                errors["content"] = ["This field is required"]
            if content_size_field is None:
                errors["content_size"] = ["This field is required"]
            if content_alignment_field is None:
                errors["content_alignment"] = ["This field is required"]

        if field_type == FIELD_TYPES[15][0]:
            if label_field is None:
                errors["label"] = ["This field is required"]
            if placeholder_field is not None:
                errors["placeholder"] = ["Placeholder not allowed for this field type."]
            if validation_rule_field is not None:
                errors["validation_rule"] = ["Validation Rule not allowed for this field type."]
            if field_format_field is not None:
                errors["field_format"] = ["Field Format not allowed for this field type."]
            if options_field is not None:
                errors["options"] = ["Options not allowed for this field type."]
            if is_unique_field:
                errors["is_unique"] = ["Unique Validation not allowed for this field type."]
            if content_field is None:
                errors["content"] = ["This field is required"]
            if content_size_field is None:
                errors["content_size"] = ["This field is required"]
            if content_alignment_field is None:
                errors["content_alignment"] = ["This field is required"]

        if errors:
            raise serializers.ValidationError(errors)

        return attrs

    options = serializers.JSONField(required=False)

    class Meta:
        model = FormField
        fields = ['id', 'label', 'field_size', 'placeholder', 'custom_class_name', 'validation_rule', 'is_mandatory',
                  'is_unique', 'options', 'field_format', 'content', 'content_size', 'content_alignment']
        extra_kwargs = {
            "label": {"required": False},
            "field_size": {"required": False},
            "placeholder": {"required": False, "allow_blank": True},
            "custom_class_name": {"required": False},
            "validation_rule": {"required": False},
            "is_mandatory": {"required": False},
            "is_unique": {"required": False},
        }
