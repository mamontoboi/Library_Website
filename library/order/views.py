from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

from .models import Order
from .forms import OrderModelFormForAdmin, OrderModelFormForUser, \
    DeleteOrderAdmin, UpdateOrderModelForm

from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from .serializers import OrderModelSerializer


class OrderCRUD(RetrieveUpdateDestroyAPIView):
    """To get a particular order"""
    queryset = Order.objects.all()
    serializer_class = OrderModelSerializer


class OrderList(ListAPIView):
    """To get all orders"""
    queryset = Order.objects.all()
    serializer_class = OrderModelSerializer


class CreateOrder(CreateAPIView):
    """To create a new order"""
    serializer_class = OrderModelSerializer


class UserOrder(APIView):
    """To get particular order of specific user."""
    def get(self, request, user_id, order_id):
        try:
            order = Order.objects.get(id=order_id, user=user_id)
            serializer = OrderModelSerializer(order)
            order_response = {
                'user': user_id,
                'order': serializer.data
            }
            return JsonResponse(order_response)
        except:
            return JsonResponse({'Error': f'Order with id {order_id} does not exist!'})


class UserOrderList(ViewSet):
    """To get all orders of specific user"""

    def list(self, request, user_id=None):
        order = Order.objects.filter(user=user_id)
        serializer = OrderModelSerializer(order, many=True)
        return Response(serializer.data)


def show_all_orders(request):
    if request.user.is_authenticated and request.user.role == 1:
        data = Order.get_all()
        context = {'list_of_order': data}
        return render(request, 'order/order_all.html', context)

    return render(request, 'order/order_all.html', {})


def show_own_orders(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        if user_id:
            try:
                data = list(Order.get_all_by_user_id(user_id))
                context = {'order_by_id': data}
                return render(request, 'order/order_own_list.html', context)
            except:
                return render(request, 'order/order_own_list.html',
                              {'order_by_id': "None order"})

    return render(request, 'order/order_own_list.html', {})


def create_an_order(request):
    form = OrderModelFormForUser()
    if request.user.is_authenticated:
        if request.user.role:
            form = OrderModelFormForAdmin()
            if request.method == 'POST':
                form = OrderModelFormForAdmin(request.POST)
                if form.is_valid():
                    cd = form.cleaned_data
                    order = Order.create(cd['user'], cd['book'], cd['end_at'])
                    return render(request, 'order/order_create.html',
                                  {'resolt': f"Order # {str(order.id)} created",
                                   'form': form})
            else:
                return render(request, 'order/order_create.html',
                              {'form': form})

        else:
            if request.method == 'POST':
                form = OrderModelFormForUser(request.POST)

                if form.is_valid():
                    cd = form.cleaned_data
                    order = Order.create(request.user, cd['book'], cd['end_at'])
                    return render(request, 'order/order_create.html',
                                  {'resolt': f"Order # {order.id} created",
                                   'form': form
                                   })
                return render(request, 'order/order_create.html',{
                    'resoltError': "Error", 'form': form})

    return render(request, 'order/order_create.html', {'form': form})


def del_order_by_root(request, order_id=None):
    if request.user.role:
        if order_id:
            order = Order.objects.get(id=order_id)
            order.delete()
            return redirect(reverse_lazy('order:orders'))

        orders = Order.objects.all()
        form = DeleteOrderAdmin()
        if request.method == 'POST':
            form = DeleteOrderAdmin(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                Order.delete_by_id(cd['orders'].id)
                return render(request, 'order/del_order.html',
                              {'form': form,})

        else:
            return render(request, 'order/del_order.html', {'form': form,
                                                            'orders': orders})


    else:
        if order_id:
            order = Order.objects.filter(id=order_id)
            if order[0].user.id == request.user.id:
                # pass
                order.delete()

        return redirect(reverse_lazy('order:order'))

    return render(request, 'order/del_order.html', {'form': form,
                                                    'orders': orders})


def upd_order(request, order_id=None):
    if order_id:

        order = Order.objects.get(id=order_id)
        form = UpdateOrderModelForm(initial=
                                    {'book': order.book,
                                     'plated_end_at': order.plated_end_at.date()
                                     },
                                    instance=Order
                                    )

        if request.method == 'POST':
            form = UpdateOrderModelForm(request.POST, instance=Order())

            if order.user.id == request.user.id or request.user.role:

                if form.is_valid():
                    ord = form.save(commit=False)
                    ord.user = order.user
                    ord.id = order.id
                    ord.created_at = order.created_at
                    ord.save()

            if request.user.role:
                return redirect(reverse_lazy('order:orders'))
            return redirect(reverse_lazy('order:order'))

        else:
            return render(request, 'order/upd_order.html', {'form': form})

    if request.user.role:
        return redirect(reverse_lazy('order:orders'))
    return redirect(reverse_lazy('order:order'))

