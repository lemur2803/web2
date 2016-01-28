from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.template import Template, Context
from django.utils import timezone
from django.conf import settings
import xml.etree.ElementTree as ET

from home_page.models import Comment, Like
from visits.models import Visit

COMMENT_TEMPLATE = """
                    <div style="margin-bottom: 10px;">
                        {% if created_at != updated_at %}
                            <div  style="background-color: #ADC1E6; padding: 0px 4px; height: 38px;">
                                <div style="float: left;"><b>{{ author }}</b></div>
                                <div style="float: right; font-size: xx-small; line-height: 19px;">{{ created_at }}</div>
                                <br>
                                <div style="float: right; font-size: xx-small;line-height: 19px;">{{ updated_at }}</div>
                            </div>
                        {% else %}
                            <div  style="background-color: #ADC1E6; padding: 0px 4px; height: 19px;">
                                <div style="float: left;"><b>{{ author }}</b></div>
                                <div style="float: right; font-size: xx-small; line-height: 19px;">{{ created_at }}</div>
                            </div>
                        {% endif %}
                        {% if edit_or_delete %}
                            <div style="height: 19px; background-color: #CDE1F5;">
                                <div style="float: right;">
                                    <a onclick="historyComment({{ id }}); return false;" href="#">H</a>
                                    <a onclick="editComment({{ id }}); return false;" href="#">R</a>
                                    <a onclick="deleteComment({{ id }}); return false;" href="delete_comment/">D</a>
                                </div>
                            </div>
                        {% endif %}
                        <div id="comment_{{ id }}" style="word-break: break-all;">{{ text }}</div>
                    </div>
                    """


def index(request):
    args = {}
    user_visits = Visit.objects.filter(uri='/', ip_address=request.META.get('REMOTE_ADDR', ''))
    if user_visits:
        args['user_visits'] = user_visits[0].visits
        args['last_visit'] = user_visits[0].last_visit
        for visit in user_visits:
            if args['last_visit'] < visit.last_visit:
                args['last_visit'] = visit.last_visit
    else:
        args['user_visits'] = 1
        args['last_visit'] = 'never'
    return render(request, 'index.html', args)


def signup(request):
    if request.method == "POST":
        nickname = request.POST['signup_nickname']
        email = request.POST['signup_email']
        password = request.POST['signup_password']
        confirm = request.POST['signup_password_2']
        if not all([nickname, email, password, confirm]) or (password != confirm):
            return render(request, 'sign.html', {'error': 'Something goes wrong!'})
        try:
            user = User.objects.create_user(
                username=nickname,
                email=email,
                password=password)
            user.save()
            return render(request, 'sign.html', {'message': 'Welcome!'})
        except Exception as ex:
            return render(request, 'sign.html', {'message': 'Sorry, your Nickname or E-mail is occupied! '})


def signin(request):
    if request.method == "POST":
        username = request.POST['signin_name']
        password = request.POST['signin_password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, 'sign.html', {'message': 'Hello again!'})
            else:
                return render(request, 'sign.html', {'error': 'Wrong e-mail or password!'})
        else:
            return render(request, 'sign.html', {'error': 'User doesn\'t exists'})


def signout(request):
    logout(request)
    return render(request, 'sign.html', {'message': 'Goodbye!'})


def users(request):
    users = User.objects.all()
    return render(request, 'users.html', {'users': users})


def about(request):
    return render(request, 'about.html', {})


def gallery(request):
    return render(request, 'gallery.html', {})


def comments(request, id_image):
    comments = Comment.objects.filter(id_image=id_image)
    return render(request, 'comments.html', {'comments': comments})


def send_comment(request):
    if request.method == "POST":
        if request.is_ajax():
            if request.user.is_authenticated():
                if request.POST['ifEdit'] == 'true':
                    comment = get_object_or_404(Comment, id=request.POST['editId'])
                    text = request.POST['text']
                    if text != "":
                        comment.text = text
                        comment.updated_at = timezone.now()
                        comment.history += str(comment.updated_at) + '\n' + comment.text + '\n\n\n\n'
                        comment.save()
                        return HttpResponse('editOK')
                    else:
                        return HttpResponse('Empty comment!')
                else:
                    author = User.objects.get(username=request.user.username)
                    text = request.POST['text']
                    picture_id = request.POST['id']
                    if text != "":
                        comment = Comment.objects.create(id_image=picture_id, user=author, text=text)
                        comment.save()
                        comment.history = str(comment.created_at) + '\n' + comment.text + '\n\n\n\n'
                        comment.save()
                        response_comment = get_comment_item(comment, author)
                        return JsonResponse({'comment': response_comment})
                    else:
                        return HttpResponse('Empty comment!')
    return HttpResponse(request.META['HTTP_REFERER'])


def get_comments(request):
    if request.method == 'GET':
        if request.is_ajax():
            image = request.GET['id']
            response = {}
            counter = 0
            for comment in Comment.objects.filter(id_image=image):
                comment_item = get_comment_item(comment, request.user.username)
                response[counter] = comment_item
                counter += 1
            return JsonResponse(response)
    return HttpResponse(request.META['HTTP_REFERER'])


def get_comment_item(comment, request_user):
    comment_item = {}
    comment_item['author'] = comment.user.username
    comment_item['text'] = comment.text
    comment_item['created_at'] = comment.created_at
    comment_item['updated_at'] = comment.updated_at
    comment_item['id'] = comment.id
    if comment_item['author'] == request_user:
        comment_item['edit_or_delete'] = True
    else:
        comment_item['edit_or_delete'] = False
    comment_template = Template(COMMENT_TEMPLATE)
    context = Context(comment_item)
    return comment_template.render(context)


def delete_comment(request, id_comment):
    if request.method == 'POST':
        if request.is_ajax():
            if request.user.is_authenticated():
                    comment = get_object_or_404(Comment, id=id_comment)
                    if comment:
                        if comment.user.username == request.user.username:
                            comment.delete()
                            return HttpResponse('OK')
    return HttpResponse(request.META['HTTP_REFERER'])


def get_history(request):
    if request.method == 'GET':
        if request.is_ajax():
            id_comment = request.GET['id']
            if request.user.is_authenticated():
                    comment = get_object_or_404(Comment, id=id_comment)
                    if comment:
                        if comment.user.username == request.user.username:
                            return HttpResponse(comment.history)
    return HttpResponse(request.META['HTTP_REFERER'])


def visits(request):
    hits_by_ip = {}
    final_list_by_ip = []
    all_hits = Visit.objects.all()
    ip_addrs = set([visitor.ip_address for visitor in all_hits])
    for ip_addr in ip_addrs:
        visits_by_ip = Visit.objects.filter(ip_address=ip_addr)
        num_hits = 0
        for visit_by_ip in visits_by_ip:
            num_hits += visit_by_ip.visits
        last_visit = timezone.localtime(visits_by_ip.order_by('-last_visit')[0].last_visit)
        #if ip_addr in settings.ADMIN_IP:
        #    ip_addr = "ADMIN IP"
        hits_by_ip[ip_addr] = [last_visit, num_hits]
    for key in sorted(hits_by_ip, key=lambda k: hits_by_ip[k][0], reverse=True):
        final_list_by_ip.append([key, hits_by_ip[key][0], hits_by_ip[key][1]])
    return render(request, 'visits.html', {'hits_by_ip': final_list_by_ip})


def details_page(request, ip_address):
    #if ip_address in settings.ADMIN_IP:
    #    return Http404
    all_visits_by_ip = Visit.objects.filter(ip_address=ip_address).order_by('-last_visit')
    for visit_by_ip in all_visits_by_ip:
        if visit_by_ip.last_visit:
            visit_by_ip.last_visit = timezone.localtime(visit_by_ip.last_visit)
    return render(request, 'details.html', {'all_visits_by_ip': all_visits_by_ip})


def send_like(request):
    if request.method == "POST":
        if request.is_ajax():
            if request.user.is_authenticated():
                author = User.objects.get(username=request.user.username)
                picture_id = request.POST['id']
                like_exists = Like.objects.filter(id_image=picture_id, user=author)
                if not like_exists:
                    like = Like.objects.create(id_image=picture_id, user=author)
                    like.save()
                else:
                    like_exists.delete()
                count = Like.objects.filter(id_image=picture_id).count()
                return HttpResponse(count)
    return HttpResponse(request.META['HTTP_REFERER'])


def get_likes_count(request):
    if request.method == "GET":
        if request.is_ajax():
            picture_id = request.GET['id']
            count = Like.objects.filter(id_image=picture_id).count()
            return HttpResponse(count)
    return HttpResponse(request.META['HTTP_REFERER'])


def statistic(request):
    xml_header = b'<?xml version="1.0" encoding="UTF-8"?>\n'
    root = ET.Element('Gallery')
    for image in range(1, 44):
        image_node = ET.SubElement(root, 'Image')
        ET.SubElement(image_node, 'Name').text = str(image)
        ET.SubElement(image_node, 'Likes').text = str(Like.objects.filter(id_image=image).count())
        ET.SubElement(image_node, 'Comments').text = str(Comment.objects.filter(id_image=image).count())
    return HttpResponse(xml_header + ET.tostring(root), content_type='text/xml')
