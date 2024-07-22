from pyexpat.errors import messages
import random
from django.shortcuts import get_object_or_404, render, redirect
from shop.models import Order, Order_item, Product, Categories, Filter_price, Color, Brand,Contact, Product_Color, Size,Wishlist, Cart1
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_email
from django.core.exceptions import ValidationError




def header_footer(request):
    return render(request, 'main/header_footer.html')

def home(request):
    show_product = Product.objects.filter(condition='New')[:4]
    sale_product = Product.objects.filter(condition='Sale')[:4]
    fifty_product = Product.objects.filter(condition='50% Off')[:4]
    seventy_product = Product.objects.filter(condition='75% Off')[:4]
    
    for i in show_product:
        if i.condition == 'Sale':
            discount = (i.price * 10)/100
            i.discount = i.price - discount
            i.save()
        elif i.condition == '75% Off':
            discount = (i.price * 75)/100
            i.discount = i.price - discount
            i.save() 
        elif i.condition == '50% Off':
            discount = (i.price * 50)/100
            i.discount = i.price - discount
            i.save()

    context = {
        'product' : show_product,
        'sale_products' : sale_product,
        'fifty_products' : fifty_product,
        'seventy_five_products' : seventy_product,
    }
    return render(request, 'main/home.html', context)

# def shop(request):
#     show_product = Product.objects.filter(status='Publish')
#     category = Categories.objects.all()
#     filter_price = Filter_price.objects.all()
#     color = Color.objects.all()
#     brand = Brand.objects.all()

#     CATID = request.GET.get('categories_id')
#     PID = request.GET.get('price_id')
#     CID = request.GET.get('color_id')
#     BID = request.GET.get('brand_id')
#     ATOZ_ID = request.GET.get('ATOZ')
#     ZTOA_ID = request.GET.get('ZTOA')
#     LTOH_ID = request.GET.get('LTOH')
#     HTOL_ID = request.GET.get('HTOL')
#     NEW_ID = request.GET.get('NEW')
#     OLD_ID = request.GET.get('OLD')

#     if CATID:
#         show_product = Product.objects.filter(categories=CATID, status='Publish')
#     elif PID:    
#         show_product = Product.objects.filter(filter_price=PID, status='Publish')
#     elif CID:
#         show_product = Product.objects.filter(color=CID, status='Publish')
#     elif BID:
#         show_product = Product.objects.filter(brand=BID, status='Publish')
#     elif ATOZ_ID:
#         show_product = Product.objects.filter(status='Publish').order_by('name')
#     elif ZTOA_ID:
#         show_product = Product.objects.filter(status='Publish').order_by('-name')
#     elif LTOH_ID:
#         show_product = Product.objects.filter(status='Publish').order_by('price')
#     elif HTOL_ID:
#         show_product = Product.objects.filter(status='Publish').order_by('-price')
#     elif NEW_ID:
#         show_product = Product.objects.filter(status='Publish', condition='New').order_by('-id')
#     elif OLD_ID:
#         show_product = Product.objects.filter(status='Publish', condition='Old').order_by('id')
            
#     context = {
#         'product' : show_product,
#         'category' : category,
#         'price' : filter_price,
#         'color' : color,
#         'brand' : brand
#     }
#     return render(request, 'main/shop.html', context)
def shop(request):
    # Fetch all products initially
    show_product = Product.objects.filter(status='Publish')
    
    # Fetch all categories, price filters, colors, and brands
    category = Categories.objects.all()
    filter_price = Filter_price.objects.all()
    color = Color.objects.all()
    brand = Brand.objects.all()

    # Handle GET parameters for filtering
    CATID = request.GET.get('categories_id')
    PID = request.GET.get('price_id')
    CID = request.GET.get('color_id')
    BID = request.GET.get('brand_id')
    print(BID)
    
    # Handle sorting options
    sort_by = request.GET.get('sort_by')
    
    # Apply filters based on GET parameters
    if CATID:
        show_product = Product.objects.filter(categories=CATID)
    if PID:
        show_product = Product.objects.filter(filter_price=PID)
    if CID:
        show_product = Product.objects.filter(color=CID)
    if BID:
        show_product = Product.objects.filter(brand=BID)
    
    # Apply sorting based on sort_by parameter
    
    if sort_by == 'ATOZ':
        show_product = Product.objects.filter(status='Publish').order_by('name')
    elif sort_by == 'ZTOA':
        show_product = Product.objects.filter(status='Publish').order_by('-name')
    elif sort_by == 'LTOH':
        show_product = Product.objects.filter(status='Publish').order_by('price')
    elif sort_by == 'HTOL':
        show_product = Product.objects.filter(status='Publish').order_by('-price')
    elif sort_by == 'NEW':
        show_product = Product.objects.filter(status='Publish', condition='New').order_by('-id')
    elif sort_by == 'SALE':
        show_product = Product.objects.filter(status='Publish', condition='Sale').order_by('id')
    elif sort_by == '50%OFF':
        show_product = Product.objects.filter(status='Publish', condition='50% Off').order_by('id')
    elif sort_by == '75%OFF':
        show_product = Product.objects.filter(status='Publish', condition='75% Off').order_by('id')


    context = {
        'product': show_product,
        'category': category,
        'price': filter_price,
        'color': color,
        'brand': brand,
    }
    
    return render(request, 'main/shop.html', context)

def search(request):
    query = request.GET.get('query')

    search_product = Product.objects.filter(categories__name__icontains = query )

    context = {
        'search_product' : search_product
    }

    return render(request, 'main/search.html', context)

def shop_view(request):
    categories_id = request.GET.get('categories_id')
    category = Categories.objects.get(id=categories_id)  # Assuming 'id' is the primary key field

    # Retrieve products or data related to the selected category
    # Replace this with your actual logic to fetch and render products
    products = []  # Example placeholder for products
    # Example: products = Product.objects.filter(category=category)

    return render(request, 'shop.html', {'category': category, 'products': products})


def product(request, id):

    prod = Product.objects.filter(status='Publish', id=id).first()
    sizes = Size.objects.all()
    colors = Product_Color.objects.all()
    
    context = {
        'prod' : prod,
        'sizes' : sizes,
        'colors' : colors,
        
    }
    return render(request, 'main/product.html',context)


def contact(request):

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # if not (name and email and subject and message):
        #     return render(request, 'main/contact.html', {'error_message': True})

        error = { }

        if not name:
            error['name'] = "Name is Require"

        if not email:
            error['email'] ="Email is Required"
        else:
            try:
                validate_email(email)
            except ValidationError:
                error['email'] = "Enter a valid email address."

        if not subject:
            error['subject'] = "Subject is Required"
        
        if not message:
            error['message'] = "Message is Required"

        if error:
            return render(request, 'main/contact.html', {'error': error})
        
        contact = Contact(
            name = name,
            email = email,
            subject = subject,
            message = message
            #database_field = form_data_fatch_variable
        )
        subject = subject
        message =  f"""\ You Get Contact From {email} 

Contact For : {subject}

Message is {message}


        """ 
        # email_from = email

        try:
            send_mail(subject,message,{email}, ['streeboutique20@gmail.com'])
            contact.save()
            return redirect('home')
        except:
            return redirect('contact')
        
      
    return render(request, 'main/contact.html', {'error': {}})

def register(request):
    if request.method == 'POST':
        username = request.POST.get('u_name')
        first_name = request.POST.get('f_name')
        last_name = request.POST.get('l_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        c_password = request.POST.get('c_password')

        error = { }

        if not username:
            error['u_name'] = "User Name is Require"
        
        if not first_name:
            error['f_name'] = "First Name is Required"

        if not last_name:
            error['l_name'] = "Last Name is Required"

        if not email:
            error['email'] ="Email is Required"
        else:
            try:
                validate_email(email)
            except ValidationError:
                error['email'] = "Enter a valid email address."
            
        if User.objects.filter(email=email).exists():
            error['email'] = "Email already exists. Please use a different email."

        if not password:
            error['password'] = "Password is Required"
        elif len(password) < 8:
            error['password'] = "The password must be at least 8 characters long."
        elif not any(char.isalpha() for char in password):
            error['password'] = "The password must contain at least one letter."
        elif not any(char.isdigit() for char in password):
            error['password'] = "The password must contain at least one digit."
        elif not any(char in "!@#$%^&*(){}[]" for char in password):
            error['password'] = "The password must contain at least one special character."
        
        if not c_password:
            error['c_password'] = "Confirm Password is required."
        elif password != c_password:
            error['c_password'] = "Passwords do not match."

        if error:
            return render(request, 'auth/register.html', {'error': error})

        data = User.objects.create_user(username,email,password)
        data.first_name = first_name
        data.last_name = last_name
        data.c_password = c_password

        data.save()

        return redirect('login')

    return render(request, 'auth/register.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('u_name')  
        password = request.POST.get('password')

        error = { }

        if not username:
            error['u_name'] = "User Name is Require"

        if not password:
            error['password'] = "Password is Required"

        if error:
            return render(request, 'auth/auth.html', {'error': error})

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  
        else:
            msg = "Invalid username or password."
            return render(request, 'auth/auth.html', {'msg': msg})

    return render(request, 'auth/auth.html',)


def user_logout(request):
    logout(request)
    

    return redirect('home')


@login_required(login_url="/login/")
def cart_details(request):
    cart = Cart1.objects.filter(user = request.user)
    context = {
        'cart' : cart,
    }
        
    return render(request, 'cart/cart_details.html', context)       

@login_required(login_url="/login/")
def cart_add(request, id):
    prod = Product.objects.filter(status='Publish', id=id).first()

    if request.method == 'POST':
        # item = Product.objects.filter(user = request.user)
        selected_id = request.POST.get('size')
        clr_id = request.POST.get('product_color')
        selected_size = None
        selected_clr = None
        if selected_id != 5 and selected_id is not None:
            selected_size = Size.objects.get(id=selected_id)
        else:
            selected_size = Size.objects.get(id=5)
        if clr_id != 4 and clr_id is not None:
            selected_clr = Product_Color.objects.get(id=clr_id)
        else:
            selected_clr = Product_Color.objects.get(id=4)
        image = prod.image
        name = prod.name
        price = prod.price
        
        cart = Cart1()
        cart.item = prod
        cart.user = request.user
        cart.size = selected_size
        cart.clr = selected_clr
        cart.image = image
        cart.name = name
        cart.price = price
        cart.quantity = 1
        cart.sbt = price
        cart.save()
        
        cart = Cart1.objects.filter(user = request.user)
        context = {
        'cart' : cart,
    }
        
        return render(request, 'cart/cart_details.html', context)

    
    cart = Cart1.objects.filter(user = request.user)
    context = {
        'cart' : cart,
    }
    return render(request, 'cart/cart_details.html', context)



@login_required(login_url="/login/")
def item_clear(request, id):
    cart_item = get_object_or_404(Cart1, id=id, user=request.user)
    cart_item.delete()
    return redirect('cart')


@login_required(login_url="/login/")
def item_increment(request, id):
    cart_item = get_object_or_404(Cart1, id=id, user=request.user)
    cart_item.quantity += 1
    cart_item.sbt = cart_item.price * cart_item.quantity
    cart_item.save()
    return redirect('cart')


@login_required(login_url="/login/")
def item_decrement(request, id):
    cart_item = get_object_or_404(Cart1, id=id, user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.sbt = cart_item.price * cart_item.quantity
        cart_item.save()
    return redirect("cart")


@login_required(login_url="/login/")
def cart_clear(request):
    cart_items = Cart1.objects.filter(user=request.user)
    cart_items.delete()
    return redirect('cart')

@login_required(login_url="/login/")
def checkout_view(request):
    cart = Cart1.objects.filter(user=request.user)
    mainSubTotal = 0
    gst = 0
    for cart in cart:
        mainSubTotal += cart.sbt
        gst = (cart.sbt*20)/100
    mainSubTotal = mainSubTotal + gst + 100
    
    cart = Cart1.objects.filter(user=request.user)
    return render(request, 'cart/checkout.html', {'cart' : cart, 'mainSubTotal' : mainSubTotal, 'gst' : gst})


@login_required(login_url="/login/")
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist.products.add(product)
    return redirect('wishlist')


@login_required(login_url="/login/")
def view_wishlist(request):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    context = {
        'wishlist': wishlist
    }
    return render(request, 'main/wishlist.html', context)

@login_required(login_url="/login/")
def remove_from_wishlist(request, product_id):
    wishlist = get_object_or_404(Wishlist, user=request.user)
    product = get_object_or_404(Product, id=product_id)
    
    if product in wishlist.products.all():
        wishlist.products.remove(product)
    
    return redirect('wishlist')


def forget_pwd(request):
    
    if request.method == "POST":
        email = request.POST.get('email')

        error = { }

        if not email:
            error['email'] ="Email is Required"
        elif '@' not in email:
            error['email']= "Enter Valid Email"

        if error:
            return render(request, 'auth/forgot_pwd.html', {'error': error})
        
        try:
            user = User.objects.get(email=email)
            if user:
                OTP = random.randint(100000, 999999)
                request.session['email'] = email
                request.session['otp'] = OTP
                to = email
                subject = "Your One-Time Password (OTP)"
                message = f"""\
Dear {to},
                        
Thank you for verifying your email address. As requested, here is your One-Time Password (OTP) for further authentication:
                        
OTP: {OTP}
                        
If you did not request this OTP or have any questions, please contact us immediately.
                        
Best regards,
streeboutique
"""
                send_mail(subject, message, 'streeboutique20@gmail.com', [to], fail_silently=False)
                return redirect('varify')
        except User.DoesNotExist:
            message = "Enter Correct Email."
            return render(request, 'auth/forgot_pwd.html',{'message':message})
    
    return render(request, 'auth/forgot_pwd.html')

def varify(request):
                      
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')

        error = { }

    
        if not entered_otp:
            error['otp'] = "Otp is required"

        if error:
            return render(request, 'auth/varify.html', {'error': error})

        if entered_otp == str(request.session.get('otp')):
            request.session['otp'] = ''
            return redirect('change_pwd')
        else:
            message = "Invlid OTP, Please Try Again."
            return render(request, 'auth/varify.html',{'message':message})
        
    
    return render(request, 'auth/varify.html')

def change_pwd(request):
    if request.method == 'POST':
        email = request.session.get('email')

        if email:
            pwd = request.POST.get('pwd')
            cpwd = request.POST.get('cpwd')

            error = { }

            if not pwd:
                error['password'] = "Password is Required"
            elif len(pwd) < 8:
                error['password'] = "The password must be at least 8 characters long."
            elif not any(char.isalpha() for char in pwd):
                error['password'] = "The password must contain at least one letter."
            elif not any(char.isdigit() for char in pwd):
                error['password'] = "The password must contain at least one digit."
            elif not any(char in "!@#$%^&*(){}[]" for char in pwd):
                error['password'] = "The password must contain at least one special character."

            if not cpwd:
                error['cpwd'] = "Confirm Password is Required"

            if error:
                return render(request, 'auth/change_pwd.html', {'error': error})

    
            if pwd == cpwd:
                try:
                    user = User.objects.get(email=email)
                    user.set_password(pwd)
                    user.save()
                    request.session['email'] = ''
                    return redirect('login')
                except User.DoesNotExist:
                    messages.error(request, 'User does not exist.')
            else:
                message = "Password Doesn't Match"
                return render(request, 'auth/change_pwd.html',{'message':message})
    
    return render(request, 'auth/change_pwd.html')


@login_required(login_url="/login/")
def place_order(request):
    
    
    mainSubTotal = 0
    gst = 0
    cart = None
    new_order = None
    if request.method == 'POST':
        user = request.user
        cart = Cart1.objects.filter(user=request.user)
        
        # Extract form data
        f_name = user.first_name
        l_name = user.last_name
        country = request.POST.get('country')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        post_code = request.POST.get('zip')
        phone = request.POST.get('phone')
        email = user.email
        additional_info = request.POST.get('message')
        amount = request.POST.get('amount')

        # Create new Order instance with associated user
        new_order = Order(
            
            user=user,  # Assign user object
            f_name=f_name,
            l_name=l_name,
            country=country,
            address=address,
            city=city,
            state=state,
            post_code=post_code,
            phone=phone,
            email = email, 
            additional_info=additional_info,
            amount = amount,
        )
        
        new_order.save()
        # order = Order.objects.filter(user=request.user)
        # oitm = Order_item.objects.filter(order = order)
        # qty = cart.quantity
        # k = 0
        # # Save the order to the database
        # if new_order.save():
        #     for i in oitm:
        #         i.product.totalStock -= qty[k]
        #         k+=1
                

        error = { }
        
        if not f_name:
            error['f_name'] = "First Name is Required"

        if not l_name:
            error['l_name'] = "Last Name is Required"

        if not address:
            error['address'] = "Address is Required"

        if not city:
            error['city'] = "City Name is Required"

        if not state:
            error['state'] = "State Name is Required"

        if not post_code:
            error['zip'] = "Post Code/Zip is Required"
        elif len(post_code) < 6:
            error['zip'] = "Please Enter Valid Post Code/Zip."

        if not phone:
            error['phone'] = "Phone Number is Required"
        elif len(phone) < 10:
            error['phone'] = "Please Enter Valid Phone Number."

        if not email:
            error['email'] ="Email is Required"
        elif '@' not in email:
            error['email']= "Enter Valid Email"


        if error:
            return render(request, 'cart/checkout.html', {'error': error})


        for i in cart:
            mainSubTotal += i.sbt
            gst = (i.sbt*20)/100
            mainSubTotal = mainSubTotal + gst + 100
            item = Order_item(
                order = new_order,
                product = i.name,
                image = i.image,
                quantity = i.quantity,
                price = i.price,
                total = mainSubTotal,
            )
            item.save()

    order = Order.objects.filter(user = request.user).last()
    cart = list(Cart1.objects.filter(user = request.user))
    cart2 = Cart1.objects.filter(user = request.user)
    cart2.delete()
    
    

    try:
            # Send confirmation email to the customer
            subject = f''' 'Order Confirmation - #{order.id}' '''
            message = f'''

Dear {order.f_name} {order.l_name},


Thank you for your order! We are pleased to confirm that your order has been successfully placed.

Thank you again for choosing us. Visit our site again!!.


Best regards,

streeboutique

'''
            send_mail(subject, message, 'streeboutique20@gmail.com', [email], fail_silently=False)
    except Exception as e:
            # Handle email sending errors (optional)
        print(f"Failed to send email: {e}")
            # Redirect to checkout page or handle as needed
        return redirect('checkout')
        # Redirect to a success page or any other view

    return render(request, 'cart/invoice.html', {'order' : new_order, 'cart' : cart, 'mainSubTotal': mainSubTotal, 'gst':gst})



@login_required(login_url="/login/")
def invoice(request, order_id):
    order = get_object_or_404(Order, id=order_id)  # Retrieve order by its id

    context = {
        'order': order,  # Pass the order object to the context
    }
   

    return render(request, 'cart/invoice.html', context)


def term_condition(request):
    return render(request, 'main/term&condition.html')


def faq(request):
    return render(request, 'main/faq.html')


def private_policy(request):
    return render(request, 'main/private_policy.html')

@login_required(login_url="/login/")
def order_page(request):
    # Fetch orders related to the current logged-in user
    orders = Order.objects.filter(user=request.user)
    email = request.user.email
    user = User.objects.filter(email=email)

    context = {
        'orders': orders,
        'user':user
    }
    
    return render(request, 'account/order_page.html', context)

@login_required(login_url="/login/")
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':

        user_email = request.user.email

        subject = f''' 'Order Confirmation - #{order.id}' '''
        message = f'''
Dear streeboutique,

This is to inform you that order number {order.id} has been  cancelled by {order.f_name} {order.l_name}.
 {user_email}

        
Best regards,

streeboutique
        
        '''
        email_from = settings.EMAIL_HOST_USER
        
        # order = Order.objects.filter(user=request.user)
        # cart = Cart1.objects.filter(user = request.user)
        # oitm = Order_item.objects.filter(order = order)
        # qty = cart.quantity
        # k = 0
        # for i in oitm:
        #     i.product.totalStock += qty[k]
        #     k+=1

        try:
            send_mail(subject,message,email_from, ['streeboutique20@gmail.com'])
            order.cancel()
            return redirect('order_page')
        except:
            return redirect('cart')
        # Optionally, you can add a message or redirect to a different page
        
    
    # If method is not POST, render some error or fallback page
    return render(request, 'account/order_page.html', {'message': 'Invalid request'})


# @login_required(login_url="/login/")
# def order_tracking(request):
    
#     if request.method == "POST":
#         user_email = request.user.email

#         user = Order.objects.filter(email = user_email)

#         for order in user:
#             status = order.get_status_display()
#             try:
#                 to = user
#                 subject = "For Tracking Order"
#                 message = f"Your Order in {status}"
#                 send_mail(subject, message, 'streeboutique20@gmail.com', [to], fail_silently=False)
#                 return redirect('varify')
#             except User.DoesNotExist:
#                 messages.error(request, 'User with this email does not exist.')

        

#     return render(request, 'main/order_tracking.html')

def about_us(request):
    return render(request, 'main/about_us.html')


def service(request):
    return render(request, 'main/service.html')
