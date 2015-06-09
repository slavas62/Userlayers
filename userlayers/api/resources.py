import mutant

from django.conf.urls import url
from tastypie.resources import ModelResource, Resource
from tastypie import fields, http
from tastypie.authorization import DjangoAuthorization, Authorization
from tastypie.utils import trailing_slash
from mutant.models import ModelDefinition, FieldDefinition

FIELD_TYPES = (
    ('text', mutant.contrib.text.models.TextFieldDefinition),
    ('integer', mutant.contrib.numeric.models.BigIntegerFieldDefinition),
    ('boolean', mutant.contrib.boolean.models.NullBooleanFieldDefinition),
)

class FieldsResource(ModelResource):
    type = fields.ApiField()
    
    class Meta:
        queryset = FieldDefinition.objects.all()
        authorization = DjangoAuthorization()
        fields = ['name']
    
    def hydrate(self, bundle):
        bundle = super(FieldsResource, self).hydrate(bundle)
        model = dict(FIELD_TYPES)[bundle.data['type']]
        if not isinstance(bundle.obj, model):
            self._meta.object_class = model
            bundle.obj = model()
        return bundle
        
    def dehydrate(self, bundle):
        bundle.data['type'] = bundle.obj.content_type.name
        return bundle
    

class TablesResource(ModelResource):
    fields = fields.ToManyField(FieldsResource, 'fielddefinitions', full=True)
    
    class Meta:
        queryset = ModelDefinition.objects.all()
        authorization = DjangoAuthorization()
        fields = ['name']
        
    def hydrate(self, bundle):
        bundle.obj.app_label = 'dynamic'
        bundle.obj.model = bundle.data['name']
        bundle.obj.object_name = bundle.data['name']
        return super(TablesResource, self).hydrate(bundle)

    def save_m2m(self, bundle):
        for f in bundle.data['fields']:
            f.obj.model_def = bundle.obj
        return super(TablesResource, self).save_m2m(bundle)

class TableProxyResource(Resource):
    pattern = '^tables/(?P<table_pk>)/data'
    
    class Meta:
        pass
    
    def dispatch(self, request_type, request, **kwargs):
        table_pk = kwargs.pop('table_pk')
        try:
            md = ModelDefinition.objects.get(pk=table_pk)
        except ModelDefinition.DoesNotExist:
            return http.HttpNotFound()
        
        class R(ModelResource):
            class Meta:
                queryset = md.model_class().objects.all()
                authorization = Authorization()
        
        return R().dispatch(request_type, request, **kwargs)
    
    def base_urls(self):
        return [
            url(r"^tablesdata/(?P<table_pk>\d+)/data%s$" % trailing_slash(), self.wrap_view('dispatch_list'), name="api_dispatch_list"),
            url(r"^tablesdata/(?P<table_pk>\d+)/data/(?P<%s>.*?)%s$" % (self._meta.detail_uri_name, trailing_slash()), self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
        ]
