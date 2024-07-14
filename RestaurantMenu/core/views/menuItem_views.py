from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser 

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from core.models import MenuItem, Category, Table
from core.serializers import MenuItemSerializer, TableSerializer

from rest_framework import status



@api_view(['PUT'])
# @permission_classes([IsAdminUser])
def update_card_type_setting(request):
    data = request.data
    card_type = data.get('card_type') 
    # print(card_type) 
    menuItems = MenuItem.objects.all()
    for menuItem in menuItems:
        menuItem.card_type = card_type  
        menuItem.save()
        

    return Response('CardType Updated')



@api_view(['GET'])
def getMenuItems(request):
    menuItems = MenuItem.objects.all()
    serializer = MenuItemSerializer(menuItems, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getMenuItem(request, pk):
    menuItem = MenuItem.objects.get(_id=pk)
    serializer = MenuItemSerializer(menuItem, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def createMenuItem(request):
    if request.method == 'POST':
        data = request.data
        serializer = MenuItemSerializer(data=data)
        if serializer.is_valid():
            category_name = data.get('category', None)
            if category_name:
                try:
                    category = Category.objects.get(name=category_name)
                    serializer.save(category=category)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                except Category.DoesNotExist:
                    return Response({'error': 'Category does not exist'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['PUT'])
# @permission_classes([IsAdminUser])
def updateMenuItem(request, pk):
    data = request.data
    menuItem = MenuItem.objects.get(_id=pk)

    menuItem.name = data['name']
    menuItem.price = data['price']
    menuItem.description = data['description']
    menuItem.cooking_duration = data['cooking_duration']

    category_name = data.get('category', None)
    if category_name:
        try:
            category = Category.objects.get(name=category_name)
            menuItem.category = category
        except Category.DoesNotExist:
            return Response({'error': 'Category does not exist'}, status=status.HTTP_400_BAD_REQUEST)

    menuItem.save()

    serializer = MenuItemSerializer(menuItem, many=False)
    return Response(serializer.data)


@api_view(['DELETE'])
# @permission_classes([IsAdminUser])
def deleteMenuItem(request, pk):
    menuItem = MenuItem.objects.get(_id=pk)
    menuItem.delete()
    return Response('Product Deleted')


@api_view(['POST'])
def uploadImage(request):
    data = request.data

    try:
        menuItem_id = data['menuItem_id']
        menuItem = MenuItem.objects.get(_id=menuItem_id)
    except MenuItem.DoesNotExist:
        return Response({'error': 'Menu item does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
    menuItem.image = request.FILES.get('image')
    menuItem.save()

    return Response('Image was uploaded successfully')


@api_view(['GET'])
def getTables(request):
    tables = Table.objects.all()
    serializer = TableSerializer(tables, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getTable(request, pk):
    table = Table.objects.get(_id=pk)
    serializer = TableSerializer(table, many=False)
    return Response(serializer.data)


@api_view(['POST'])
# @permission_classes([IsAdminUser])
def createTable(request):
    if request.method == 'POST':
            serializer = TableSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PUT'])
# @permission_classes([IsAdminUser])
def updateTable(request, pk):
    data = request.data
    table = Table.objects.get(_id=pk)

    table.name = data['name']

    table.save()

    serializer = TableSerializer(table, many=False)
    return Response(serializer.data)

@api_view(['DELETE'])
# @permission_classes([IsAdminUser])
def deleteTable(request, pk):
    table = Table.objects.get(_id=pk)
    table.delete()
    return Response('Table Deleted')