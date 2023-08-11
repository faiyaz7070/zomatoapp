from django.shortcuts import render, redirect
from django.http import HttpResponse
from tabulate import tabulate
from colorama import Fore, Style

# Menu dictionary containing dish information
menu = {
    "1": {"name": "Dhosa", "price": 10, "available": True, "quantity": 5},
    "2": {"name": "Maggie", "price": 15, "available": False, "quantity": 0},
    "3": {"name": "Pizza", "price": 145, "available": True, "quantity": 4},
}

# Orders list
admin_username = "faiyaz"
admin_password = "masai"
orders = []
users = {}

def display_menu(request):
    headers = ["Dish ID", "Name", "Price", "Availability", "Quantity"]
    table_data = []

    for dish_id, dish_info in menu.items():
        availability =  "Available" if dish_info["quantity"] > 0 else "Not Available"
        table_data.append([dish_id, dish_info['name'], dish_info['price'],
                           availability, dish_info['quantity']])

    table = tabulate(table_data, headers=headers, tablefmt="html")
    return HttpResponse(f"<html><body>{table}</body></html>")

def main_page(request):
    return render(request, 'main_page.html')

def user_registration(request):
    if request.method == 'POST':
        email = request.POST['email']
        if email in users:
            return render(request, 'registration.html', {'message': 'Email already registered. Please login or use a different email.'})
        else:
            name = request.POST['name']
            password = request.POST['password']
            users[email] = {
                "name": name,
                "password": password
            }
            return render(request, 'registration.html', {'message': 'Registration successful. You can now log in with your credentials.'})
    return render(request, 'registration.html')

def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        if email in users and users[email]["password"] == password:
            request.session['user_email'] = email
            return redirect('user_section')
        else:
            return render(request, 'login.html', {'message': 'Invalid credentials. Access denied.'})
    return render(request, 'login.html')

def user_section(request):
    user_email = request.session.get('user_email')
    if not user_email:
        return redirect('user_login')
    return render(request, 'user_section.html', {'user_email': user_email})

def take_order(request):
    user_email = request.session.get('user_email')
    if not user_email:
        return redirect('user_login')

    if request.method == 'POST':
        customer_name = request.POST['customer_name']
        order_items = request.POST['order_items'].split(",")
        order_status = "received"
        order_id = len(orders) + 1

        for dish_id in order_items:
            if dish_id in menu:
                dish_info = menu[dish_id]
                if not dish_info["available"]:
                    return render(request, 'take_order.html', {'message': f"{dish_info['name']} is not available. Order cannot be processed."})

                if dish_info["quantity"] <= 0:
                    return render(request, 'take_order.html', {'message': f"{dish_info['name']} is out of stock. Order cannot be processed."})

                orders.append({
                    "order_id": order_id,
                    "customer_name": customer_name,
                    "dish_id": dish_id,
                    "status": order_status
                })

                dish_info["quantity"] -= 1
                return render(request, 'take_order.html', {'message': f"{dish_info['name']} added to the order! Order ID: {order_id}"})
            else:
                return render(request, 'take_order.html', {'message': f"Dish with ID {dish_id} not found in the menu."})
    return render(request, 'take_order.html')
def update_order_status(request):
    # Implement your update order status logic here
    user_email = request.session.get('user_email')
    if not user_email:
        return redirect('user_login')

    if request.method == 'POST':
        order_id = int(request.POST['order_id'])
        new_status = request.POST['new_status']
        for order in orders:
            if order["order_id"] == order_id:
                order["status"] = new_status
                return render(request, 'update_order_status.html', {'message': 'Order status updated successfully!'})
        return render(request, 'update_order_status.html', {'message': 'Order not found.'})
    return render(request, 'update_order_status.html')

def admin_section(request):
    # Implement your admin section logic here
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if username == admin_username and password == admin_password:
            request.session['admin_logged_in'] = True
            return redirect('admin_menu')
        else:
            return render(request, 'admin_login.html', {'message': 'Invalid credentials. Access denied.'})
    return render(request, 'admin_login.html')

def admin_menu(request):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_section')
    return render(request, 'admin_menu.html')

def review_orders(request):
    # Implement your review orders logic here
    if not request.session.get('admin_logged_in'):
        return redirect('admin_section')

    orders_data = []
    for order in orders:
        order_id = order['order_id']
        customer = order['customer_name']
        dish_id = order['dish_id']
        dish = menu.get(dish_id, {}).get('name', 'Unknown')
        status = order['status']
        remaining_quantity = menu.get(dish_id, {}).get('quantity', 0)
        orders_data.append((order_id, customer, dish, status, remaining_quantity))

    return render(request, 'review_orders.html', {'orders_data': orders_data})

def add_dish(request):
    # Implement your add dish logic here
    if not request.session.get('admin_logged_in'):
        return redirect('admin_section')

    if request.method == 'POST':
        dish_id = request.POST['dish_id']
        dish_name = request.POST['dish_name']
        price = float(request.POST['price'])
        available = request.POST['available'] == "yes"
        quantity = int(request.POST['quantity'])

        menu[dish_id] = {
            "name": dish_name,
            "price": price,
            "available": available,
            "quantity": quantity
        }
        
        return render(request, 'add_dish.html', {'message': f"{dish_name} added to the menu!"})
        return redirect('display_menu')
    return render(request, 'add_dish.html')

def remove_dish(request):

    if not request.session.get('admin_logged_in'):
        return redirect('admin_section')

    if request.method == 'POST':
        dish_id = request.POST['dish_id']
        if dish_id in menu:
            dish_name = menu[dish_id]["name"]
            del menu[dish_id]
            return render(request, 'remove_dish.html', {'message': f"{dish_name} removed from the menu!"})
        else:
            return render(request, 'remove_dish.html', {'message': "Dish not found in the menu."})
    return render(request, 'remove_dish.html')

def update_dish_availability(request):
   
    if not request.session.get('admin_logged_in'):
        return redirect('admin_section')

    if request.method == 'POST':
        dish_id = request.POST['dish_id']
        if dish_id in menu:
            available = request.POST['available'] == "yes"
            quantity = int(request.POST['quantity'])
            menu[dish_id]["available"] = available
            menu[dish_id]["quantity"] = quantity
            return render(request, 'update_dish_availability.html', {'message': 'Dish availability and quantity updated successfully!'})
        else:
            return render(request, 'update_dish_availability.html', {'message': "Dish not found in the menu."})
    return render(request, 'update_dish_availability.html')
   
def user_logout(request):
    del request.session['user_email']
    return redirect('main_page') 
    
    def admin_menu(request):
     if not request.session.get('admin_logged_in'):
        return redirect('admin_section')
    return render(request, 'admin_menu.html')
def admin_logout(request):
    if 'admin_logged_in' in request.session:
        del request.session['admin_logged_in']
    return redirect('admin_section')
