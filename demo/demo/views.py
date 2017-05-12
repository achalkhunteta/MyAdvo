from django.views.generic import TemplateView, View, ListView
from django.shortcuts import render_to_response
from .models import GoogleForm
from rest_framework.views import APIView
from django.template import RequestContext
from rest_framework.response import Response
from django.forms import CharField, ChoiceField, BooleanField, RadioSelect, CheckboxInput, Form, TextInput
import json

class CreateForm(TemplateView):
    '''
    Class based view for creating a new Google form
    '''
    template_name = 'create_form.html'


class SaveForm(APIView):
    '''
    Class Based View for saving form structure in Database
    '''

    def post(self, request):
        '''
        Handle post request and Save form structure
        '''
        # Default response structure
        result = {
            'success': 0,
            'message': 'Not saved successfully'
        }

        # Load JSON data to get Form title
        unserialized_form_data = json.loads(self.request.body)
        form_title = unserialized_form_data[0]
        # Dump form structure to save in JSON Field of DB
        json_form_structure = json.dumps(unserialized_form_data[1])

        try:
            # Get or Create GoogleForm object in DB
            obj, created = GoogleForm.objects.get_or_create(title=form_title)
            obj.form_data = json_form_structure
            obj.save()

            result['success'] = 1
            result['message'] = 'Form Saved Successfully'
        except Exception as e:
            result['message'] = e

        return Response(result)


class ViewForm(TemplateView):
    '''
    class Based view to view an saved form
    '''   

    def get(self, request, **kwargs):
        # Get primary key
        form_id = kwargs.get('pk')

        form_obj = GoogleForm.objects.get(id=form_id)
        # Get JSON searialized data from form 
        json_str = form_obj.form_data
        # get Dyanmic django form class
        form_class = get_dynamic_form_class(json_str)

        # Render Dynamic form in given tempelate
        dyna_form = form_class()

        # return render(request, 'dynamic_form.html', {'form': dyna_form})
        return render_to_response( "dynamic_form.html", {
            'form': dyna_form,  'title_of_form': form_obj.title,
        }, RequestContext(request) )


class DeleteForm(APIView):
    '''
    class Based view to Delete a saved form
    '''

    def get(self, request, **kwargs):
        # Default API response
        result = {
            'success': 0,
            'message': 'Form not deleted'
        }
        # Get primary key
        form_id = kwargs.get('pk')

        form_obj = GoogleForm.objects.get(id=form_id)
        
        try:
            form_obj.delete()
            result['success'] = 1
            result['message'] = 'Form deleted Successfully'
        except Exception as e:
            result['message'] = e   

        return Response(result)


class FieldHandler(object):
    '''
    class for handling form structure and
    return respective Django form fields
    '''
    form_fields = {}

    def __init__(self, fields):
        # Loop through fields to return Django Form fields
        for field in fields:
            # get Common options for all fields
            options = self.get_common_options(field)
            # Get Django Form Field according to type
            django_field = getattr(self, "generate_field_"+field['type'] )(field, options)
            self.form_fields[field['name']] = django_field


    def get_common_options(self, field):
        options = {}
        options['label'] = field['label']
        options['help_text'] = field.get("help_text", None)
        options['required'] = bool(field.get("required", 0) )
        return options

    def generate_field_text(self, field, options):
        '''
        Method for creating a Text field
        '''
        options['max_length'] = int(field.get("max_length", "256") )
        return CharField(widget=TextInput(attrs={'type':"text"}), **options)

    def generate_field_radio(self, field, options):
        '''
        Method for creating a Choice Field
        '''
        options['choices'] = [ (c['value'], c['name'] ) for c in field['choices'] ]
        return ChoiceField(widget=RadioSelect,   **options)

    def generate_field_checkbox(self, field, options):
        '''
        Method for creating a CheckBox Field
        '''
        return BooleanField(widget=CheckboxInput, **options)


class ListForm(ListView):
    '''
    Class based view for listing all saved forms
    '''
    model = GoogleForm
    template_name = 'list_forms.html'

def get_dynamic_form_class(json_str):
    '''
    Function returns a Django Form class on basis of given field structure

    @params:
        json_str(str) : form field structure dumped in json string

    @return:
        dynamic_form_class : A Djnago form class {django.forms.form}
    '''
    fields=json.loads(json_str)

    # Get django based fields respective of their html values
    django_based_fields = FieldHandler(fields)

    # Remove Title Field before rendering the saved form.
    del django_based_fields.form_fields['title']

    return type('DynamicForm', (Form,), django_based_fields.form_fields )
