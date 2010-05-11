import dselector

parser = dselector.Parser()

urlpatterns = parser.patterns('zojax.django.harvestrss.views',
    (r'{id:digits}-{slug:chunk}', 'view_article', {}, "view_article")
)

