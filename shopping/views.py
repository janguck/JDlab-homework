from django.shortcuts import render
from shopping.models import Photo,Action, Favorite_Photo
from django.views.generic import ListView
from django.shortcuts import redirect

class PhotoLV(ListView):

    model = Photo
    template_name = "seephoto.html"
    context_object_name = "photo_list"
    queryset = Photo.objects.all().values_list()

def buyphoto(request):
    photo_num = request.POST['h_type']
    row = Photo.objects.get(photo_username=photo_num)
    row.count -= 1
    row.save()
    username = request.user.username
    Action.objects.create(action_user_username_id=username,action_type="구매",action_photo_username_id=photo_num)
    return redirect('/shopping/seephoto')

def BuyLV(request):

    row = Photo.objects.order_by('photo_username').values_list()
    reset_value = [num[0] for num in row]
    buy_photo = [Action.objects.all().filter(action_photo_username_id=str(num),action_user_username_id=request.user.username,action_type='구매').count() for num in reset_value]
    refund_photo = [
        Action.objects.all().filter(action_photo_username_id=str(num), action_user_username_id=request.user.username,
                                    action_type='환불').count() for num in reset_value]
    index = 1
    buy_list = {}
    for i,j in zip(buy_photo,refund_photo):
        index = str(index)
        buy_list[index]=i-j
        index = int(index)
        index += 1
    return render(request, 'buy_receipt.html', {'buy_list': buy_list})

def refundphoto(request):

    photo_num = request.POST['h_type']
    Action.objects.create(action_user_username_id=request.user.username,action_type="환불",action_photo_username_id=int(photo_num))
    row = Photo.objects.get(photo_username=(photo_num))
    row.count += 1
    row.save()
    return redirect('/shopping/buy_receipt')

def favorite_photo(request):

    favorite_num = request.POST['g_type']
    print(favorite_num)
    Favorite_Photo.objects.create(favorite_photo_username_id=favorite_num,favorite_user_username_id= request.user.username,boolean='추가')
    return redirect('/shopping/seephoto')

def see_favorite_photo(request):

    photo_src = {}
    fv_p = Favorite_Photo.objects.all().filter(favorite_user_username_id= request.user.username,boolean='추가')
    return_value = set([value[2] for value in fv_p.values_list()])
    total_money = 0
    for photo in return_value:
        total_money += Photo.objects.all().filter(photo_username=photo).values_list()[0][3]
        photo_src[photo] = (Photo.objects.all().filter(photo_username=photo).values_list()[0][2])
    return render(request, 'see_favorite_photo.html', {'favorite_photo': return_value,'total_money':total_money,'photo_src':photo_src})

def cancel_photo(request):

    photo_num = request.POST['h_type']
    Favorite_Photo.objects.all().filter(favorite_user_username_id=request.user.username,favorite_photo_username_id=str(photo_num)).delete()
    return redirect('/shopping/see_favorite_photo')