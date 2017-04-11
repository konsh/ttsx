#coding=utf-8
from django.shortcuts import render,redirect
from django.http import JsonResponse
from df_user import user_decorator
from models import *

@user_decorator.login
def cart(request):
    uid = request.session['user_id']
    carts = CartInfo.objects.filter(user_id=uid)
    context = {'title':'购物车',
               'page_num':1,
               'carts':carts,}
    print context
    return render(request, 'df_cart/cart.html', context)

@user_decorator.login
def add(request, gid, count):
    #用户uid购买了gid商品，数量为count
    uid = request.session['user_id']
    gid = int(gid)
    count = int(count)
    # print uid,gid
    #查询购物车中是否已经有此商品，若有则数量增加，没有则新增
    carts = CartInfo.objects.filter(user_id=uid, goods_id=gid)
    # print carts
    if len(carts)>=1:
        cart = carts[0]
        cart.count = cart.count+count
    else:
        cart = CartInfo()
        cart.user_id = uid
        cart.goods_id = gid
        cart.count = count
    cart.save()
    #若是ａｊａｘ请求则返回ｊｓｏｎ，否则转向购物车
    if request.is_ajax():
        count = CartInfo.objects.filter(user_id=request.session['user_id']).count()
        print count
        return JsonResponse({'cart_id':cart.id, 'count':count})
    else:
        return redirect('/cart/')

@user_decorator.login
def edit(request, cart_id, count):
    count1 = 1
    try:
        cart = CartInfo.objects.get(pk=int(cart_id))
        count1 = cart.count
        cart.count = int(count)
        cart.save()
        data = {'ok':0}
    except Exception as e:
        date = {'ok':count1}
    return JsonResponse(data)

@user_decorator.login
def delete(request, cart_id):
    try:
        cart = CartInfo.objects.get(pk=int(cart_id))
        cart.delete()
        data = {'ok':1}
    except Exception as e:
        data = {'ok':0}
    return JsonResponse(data)






