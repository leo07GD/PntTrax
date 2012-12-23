# Create your views here.
#from vectorformats.Formats import Django, GeoJSON
from GPSTracker.models import Client, Group, Report, Point, Line, Poly
from django.http import HttpResponse
from django.template import Context, RequestContext, loader
from django.shortcuts import render_to_response

# Project Shortcuts
from shortcuts import djangoToExportFormat

def index(request):
    return render_to_response('GPSTracker/index.html',{},context_instance=RequestContext(request))

def about(request):
    return render_to_response('GPSTracker/about.html',{},context_instance=RequestContext(request))

def clients(request):
    """Return a list of clients."""
    client_list = Client.objects.all()
    group_list = Group.objects.all()
    return render_to_response('GPSTracker/clients.html', {'client_list': client_list, 'group_list': group_list}, context_instance=RequestContext(request))

def group(request):
    """Return a list of clients."""
    client_list = Client.objects.all()
    group_list = Group.objects.all()
    return render_to_response('GPSTracker/group.html', {'client_list': client_list, 'group_list': group_list}, context_instance=RequestContext(request))

def group_detail(request, group_id):
    """Return a list of GPS Features for a GPS Group."""
    args = dict()
    args['group'] = Group.objects.get(pk=group_id)
    point_list = Point.objects.filter(group__pk = group_id)
    line_list = Line.objects.filter(group__pk = group_id)
    poly_list = Poly.objects.filter(group__pk = group_id)
    geom_dict = {'point_list':point_list,'line_list':line_list,'poly_list':poly_list}
    # Only send to render_to_response those geoms (point/line/poly) that exist
    for geom_key, geom_value in geom_dict.iteritems():
        if geom_value.exists():
            args[geom_key] = geom_value
    return render_to_response('GPSTracker/group_detail.html', args, context_instance=RequestContext(request))


def geom(request, feat_id, geom_type, geom_format):
    """Return KML object representing requested feature."""
    # Grab appropriate model
    modelMap = {'point':Point,'line':Line,'poly':Poly}
    if geom_type.lower() in modelMap.keys():
        geom_rep = modelMap[geom_type].objects.filter(pk=feat_id)
    geom_out = djangoToExportFormat(request, geom_rep, format=geom_format)
    # Add KML MIME TYPE https://developers.google.com/kml/documentation/kml_tut#kml_server
    if geom_format.lower() == 'kml':
        return HttpResponse(geom_out, content_type="application/vnd.google-earth.kml+xml")
    else:
        return HttpResponse(geom_out)
def geom_group(request, feat_id, geom_type, geom_format):
    """Return KML object representing requested feature."""
    # Grab appropriate model
    modelMap = {'point':Point,'line':Line,'poly':Poly}
    if geom_type.lower() in modelMap.keys():
        geom_rep = modelMap[geom_type].objects.filter(group__pk=feat_id)
    geom_out = djangoToExportFormat(request, geom_rep, format=geom_format)
    # Add KML MIME TYPE https://developers.google.com/kml/documentation/kml_tut#kml_server
    if geom_format.lower() == 'kml':
        return HttpResponse(geom_out, content_type="application/vnd.google-earth.kml+xml")
    else:
        return HttpResponse(geom_out)
