from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.views import View
from bloodapp.models import Bloodsell,Blooddonate,Bloodorder,Confirmbuydetails,SliderImage
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A5
from reportlab.lib import colors
from django.utils import timezone
from datetime import timedelta
from datetime import datetime
from django.core.mail import send_mail
import razorpay


blood_type=Bloodsell.objects.values('type').distinct()


# Create your views here.
def home(request):
    context = {}
    # Fetch available blood types from the Bloodsell model
    data = Bloodsell.objects.all()
    images = SliderImage.objects.all()
    context['types'] = data 
    context={'images': images}
    return render(request,'index.html',context)

def register(request):
    if request.method=='GET':
        return render(request,'register.html')
    else:
        context={}
        u = request.POST['username']   #username entered by user must be unique.
        e= request.POST['email']
        p= request.POST['password']
        cp= request.POST['confirmpassword']
        print(u,e,p,cp)
        if u=='' or e=='' or p=='' or cp=='':
            context['error']='Please fill all the details'
            return render(request,'register.html',context)
        elif p != cp:
            context['error']='Password & Confirm Password must be same'
            return render(request,'register.html',context)
        elif User.objects.filter(username=u).exists():
            context['error']='Username already exist. Enter unique username'
            return render(request,'register.html',context)
        else: 
            user=User.objects.create(username=u,email=e) #add the data in db
            user.set_password(p)  # password encryption
            user.save()
            # context['success']='Registration Successfully!!! Please Login'
            # return render(request,'login.html',context)
            messages.success(request,'Registration Successfully!!! Please Login')
            return redirect('/login')

def userLogin(request):  # name can't be login
    if request.method=='GET':
        return render(request,'login.html')
    else:
        # user login code
        context={}
        u = request.POST['username']   #username entered by user must be unique.
        p= request.POST['password']
        user=authenticate(username=u,password=p)
        if user is None:
            context['error']='Invalid Credentials!!!'
            return render(request,'login.html',context)
        else:
            print('successfully authenticated')
            print(request.user.is_authenticated)
            login(request,user)  # session login
            messages.success(request,'Login Successfully!!')
            return redirect('/')

def userLogout(request):
    logout(request)
    messages.warning(request,'Logout Successfully')
    return redirect('/')




# def bloodDonate(request):
    if request.method == 'GET':
        return render(request, 'blooddonate.html')
    else:
        # Retrieve form data
        n = request.POST['name']
        e = request.POST['email']
        t = request.POST['type']
        m = request.POST['mobile']
        a = request.POST['address']
        
        # Save the data to the database
        b = Blooddonate.objects.create(name=n, email=e, type=t, mobile=m, address=a)
        b.save()

        # Blood bank address and future date/time (1 day ahead)
        blood_bank_address = "123 Blood Bank Avenue, Lifesaver City, LS 12345"
        future_date = (timezone.now() + timedelta(days=1)).strftime("%Y-%m-%d")

        # Generate PDF
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=A5)
        width, height = A5

        # Draw border
        pdf.setStrokeColor(colors.black)
        pdf.setLineWidth(2)
        pdf.rect(50, 50, width - 100, height - 100)  # Border with padding around edges

        # Add header
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(100, 350, "-----*** Blood Donation Receipt ***-----")
        
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(100, 330, "Please Donate Blood at following Date and Address:")
        # Add blood bank address and future date/time
        pdf.setFont("Helvetica", 12)
        pdf.drawString(100, 315, f"Blood Bank Address: {blood_bank_address}")
        pdf.drawString(100, 300, f"Blood Donation - Date: {future_date}")

        pdf.drawString(100, 270, "--------------------------------------------")
        # Add donor details
        pdf.setFont("Helvetica", 12)
        pdf.drawString(100, 250, f"Donar Details:")
        pdf.setFont("Helvetica", 10)
        pdf.drawString(100, 230, f"Name: {n}")
        pdf.drawString(100, 210, f"Email: {e}")
        pdf.drawString(100, 190, f"Blood Type: {t}")
        pdf.drawString(100, 170, f"Mobile: {m}")
        pdf.drawString(100, 150, f"Address: {a}")

        pdf.showPage()
        pdf.save()

        # Move to the beginning of the BytesIO buffer
        buffer.seek(0)
        
        # Create email with attachment
        email = EmailMessage(
            'Blood Donation Confirmation',
            'Thank you for donating blood! Please find your donation receipt attached.',
            'your_email@gmail.com',
            [e]
        )
        email.attach('Blood_Donation_Receipt.pdf', buffer.getvalue(), 'application/pdf')
        
        # Send the email
        email.send()

        return redirect('/')

def bloodDonate(request):
    if request.method == 'GET':
        return render(request, 'blooddonate.html')
    else:
        # Retrieve form data
        n = request.POST['name']
        e = request.POST['email']
        t = request.POST['type']
        m = request.POST['mobile']
        a = request.POST['address']
        
        # Save the data to the database
        b = Blooddonate.objects.create(name=n, email=e, type=t, mobile=m, address=a)
        b.save()

        messages.success(request, 'Thank you for your donation! Your details have been saved successfully. Please check your email for donation receipt.')

        # Blood bank address and future date (1 day ahead, only date part)
        blood_bank_address = "123 Blood Bank Avenue, Lifesaver City, LS 12345"
        future_date = (timezone.now() + timedelta(days=1)).strftime("%Y-%m-%d")

        # Generate PDF for A5 page size
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=A5)
        width, height = A5

        # Draw border with adjusted dimensions for A5
        margin = 20
        pdf.setStrokeColor(colors.black)
        pdf.setLineWidth(1.5)
        pdf.rect(margin, margin, width - 2 * margin, height - 2 * margin)

        # Position strings within the border, adjusting y-coordinates for A5 size
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(margin + 20, height - margin - 30, "-------------*** Blood Donation Receipt ***-------------")
        
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(margin + 20, height - margin - 55, "Please Donate Blood at the Following Date and Address:")

        # Blood bank address and future date
        pdf.setFont("Helvetica", 10)
        pdf.drawString(margin + 20, height - margin - 75, f"Blood Bank Address: {blood_bank_address}")
        pdf.drawString(margin + 20, height - margin - 90, f"Blood Donation - Date: {future_date}")

        pdf.drawString(margin + 20, height - margin - 110, "--------------------------------------------------------------------------------------------------")
        
        # Donor details
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(margin + 20, height - margin - 130, "Donor Details:")
        pdf.setFont("Helvetica", 10)
        pdf.drawString(margin + 20, height - margin - 150, f"Name: {n}")
        pdf.drawString(margin + 20, height - margin - 170, f"Email: {e}")
        pdf.drawString(margin + 20, height - margin - 190, f"Blood Type: {t}")
        pdf.drawString(margin + 20, height - margin - 210, f"Mobile: {m}")
        pdf.drawString(margin + 20, height - margin - 230, f"Address: {a}")

        pdf.showPage()
        pdf.save()

        # Move to the beginning of the BytesIO buffer
        buffer.seek(0)
        
        # Create email with attachment
        email = EmailMessage(
            'Blood Donation Confirmation',
            'Thank you for donating blood! Please find your donation receipt attached.',
            'your_email@gmail.com',
            [e]
        )
        email.attach('Blood_Donation_Receipt.pdf', buffer.getvalue(), 'application/pdf')
        
        # Send the email
        email.send()

        return redirect('/')
    


# def blood_buy_view(request):
#     context = {}
#     # Fetch available blood types from the Bloodsell model
#     data = Bloodsell.objects.all()
#     context['types'] = data  # Assigning data to 'types' to use in the template

#     if request.method == 'POST':
#         # Collect form data
#         blood_type = request.POST.get('buyerBloodType')
#         quantity = request.POST.get('buyerQuantity')
#         email = request.POST.get('donorEmail')
#         mobile = request.POST.get('buyerContact')

#         # Validate that all fields are filled
#         if not all([blood_type, quantity, email, mobile]):
#             messages.error(request, "Please fill all required fields.")
#             return redirect('blood_buy')

#         # Assuming `request.user` is the logged-in user
#         userid = request.user
#         current_date = timezone.now().strftime('%Y%m%d-%H%M%S')

#         # Generate a unique order ID
#         order_id = f'ORD{current_date}-{userid.id}-{blood_type}-{quantity}'
        
#         # Save order to the database
#         Bloodorder.objects.create(
#             orderid=order_id,
#             userid=userid,
#             type=blood_type,
#             quantity=quantity,
#             mobile=mobile,
#             email=email
#         )

#         # Send a success message to the user
#         messages.success(request, "Your blood purchase request has been submitted successfully!")

#         # Send an email to the user with the order details
#         send_mail(
#             subject="Blood Purchase Request Submitted",
#             message=f"Dear {userid.username},\n\nYour blood purchase request has been successfully submitted."
#                     f"\nOrder ID: {order_id}"
#                     f"\nBlood Group: {blood_type}"
#                     f"\nQuantity: {quantity} Units(450ml-500ml)"
#                     f"\nThank you for using our service!",
#             from_email="support@example.com",  # Replace with your "from" email address
#             recipient_list=[email],
#             fail_silently=False,
#         )

#         return redirect('/')  # Redirect to the homepage or a success page

#     # Render the template with available blood types
#     return render(request, 'index.html', context)



def generate_pdf_receipt(order_id, blood_type, quantity, username, email):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A5)
    width, height = A5
    blood_bank_address = "123 Blood Bank Avenue, Lifesaver City, LS 12345"

    # Define margins
    margin = 30

    # Draw border rectangle
    c.setStrokeColor(colors.black)
    c.setLineWidth(2)
    c.rect(margin, margin, width - 2 * margin, height - 2 * margin)

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, height - 70, "Blood Purchase Receipt")

    # Order Details
    c.setFont("Helvetica", 12)
    text_y_start = height - 120
    line_spacing = 20

    c.drawString(margin + 20, text_y_start, f"Order ID: {order_id}")
    c.drawString(margin + 20, text_y_start - line_spacing, f"Name: {username}")
    c.drawString(margin + 20, text_y_start - 2 * line_spacing, f"Email: {email}")
    c.drawString(margin + 20, text_y_start - 3 * line_spacing, f"Blood Group: {blood_type}")
    c.drawString(margin + 20, text_y_start - 4 * line_spacing, f"Quantity: {quantity} Units (450ml-500ml)")
    

    c.setFont("Helvetica-Bold", 12)
    # Thank you note
    c.drawString(margin + 20, text_y_start - 6 * line_spacing, "Thank you for using our service!")


    # Collection Address
    c.drawString(margin + 20, text_y_start - 8 * line_spacing, "Kindly collect your blood from the address below:")
    
    c.setFont("Helvetica", 12)
    c.drawString(margin + 20, text_y_start - 9 * line_spacing, blood_bank_address)

    c.setFont("Helvetica", 8)
    c.drawString(margin + 20, text_y_start - 11 * line_spacing, "[Note: Please show this receipt while collecting the blood.]")

    # Save the PDF
    c.showPage()
    c.save()

    buffer.seek(0)
    return buffer

def blood_buy_view(request):
    if request.method == 'GET':
        context = {}
    
    # Fetch available blood types from the Bloodsell model
        data = Bloodsell.objects.all()
        context['types'] = data
        return render(request, 'bloodbuy.html', context)

    elif request.method == 'POST':
        # Collect form data
        blood_type = request.POST.get('buyerBloodType')
        quantity = request.POST.get('buyerQuantity')
        email = request.POST.get('donorEmail')
        mobile = request.POST.get('buyerContact')

        # Validate that all fields are filled
        # if not all([blood_type, quantity, email, mobile]):
        #     messages.error(request, "Please fill all required fields.")
        #     return redirect('blood_buy')

        userid = request.user
        current_date = timezone.now().strftime('%Y%m%d-%H%M%S')
        order_id = f'ORD{current_date}-{userid.id}-{blood_type}-{quantity}'

        # Save order to the database
        Bloodorder.objects.create(
            orderid=order_id,
            userid=userid,
            type=blood_type,
            quantity=quantity,
            mobile=mobile,
            email=email
        )

        messages.success(request, "Your blood purchase request has been submitted successfully!")

        # Generate PDF receipt
        pdf_buffer = generate_pdf_receipt(order_id, blood_type, quantity, userid.username, email)

        # Email with PDF attachment
        email_message = EmailMessage(
            subject="Blood Purchase Request Submitted",
            body=f"Dear {userid.username},\n\nYour blood purchase request has been successfully submitted."
                 f"\nOrder ID: {order_id}"
                 f"\nBlood Group: {blood_type}"
                 f"\nQuantity: {quantity} Units (450ml-500ml)"
                 f"\nThank you for using our service!",
            from_email="support@example.com",  # Replace with your "from" email address
            to=[email]
        )

        # Attach the PDF
        email_message.attach(f"Receipt_{order_id}.pdf", pdf_buffer.getvalue(), "application/pdf")
        email_message.send(fail_silently=False)

        return redirect('/')  # Redirect to the homepage or a success page

    # Render the template with available blood types

# def confirmBuyDetails(request):
#     if request.method == 'GET':
#         context = {}
    
#     # Fetch available blood types from the Bloodsell model
#         data = Bloodsell.objects.all()
#         context['types'] = data
#         return render(request, 'bloodbuy.html', context)

#     elif request.method == 'POST':
#         # Collect form data
#         blood_type = request.POST.get('buyerBloodType')
#         quantity = request.POST.get('buyerQuantity')
#         email = request.POST.get('donorEmail')
#         mobile = request.POST.get('buyerContact')

#         if not all([blood_type, quantity, email, mobile]):
#             messages.error(request, "Please fill all required fields.")
#             return redirect('bloodbuy')

#         try:
#             # Get price for the selected blood type
#             bloodsell_entry = Bloodsell.objects.get(type=blood_type)
#             price_per_unit = bloodsell_entry.price
#             total_prices = price_per_unit * int(quantity)
#         except Bloodsell.DoesNotExist:
#             messages.error(request, "Selected blood type is not available.")
#             return redirect('bloodbuy')

#         # Save the order details to the Confirmorder model
#         uid = request.user
#         confirm_order = Confirmbuydetails.objects.create(
#             userid=uid,
#             type=blood_type,
#             quantity=quantity,
#             price=bloodsell_entry, # ForeignKey reference to the Bloodsell model
#             total_price= total_prices, 
#             mobile=mobile,
#             email=email
#         )
#         confirm_order.save()

#         messages.success(request, "Your blood purchase request has been confirmed successfully!")
#         return redirect('confirmorder')  # Redirect to a success page or homepage
    

def confirmBuyDetails(request):
    if request.method == 'POST':
        # Collect form data
        blood_type = request.POST.get('buyerBloodType')
        quantity = request.POST.get('buyerQuantity')
        email = request.POST.get('donorEmail')
        mobile = request.POST.get('buyerContact')

        # Validate the form data
        if not all([blood_type, quantity, email, mobile]):
            messages.error(request, "Please fill all required fields.")
            return redirect('bloodbuy')

        try:
            # Get the price for the selected blood type
            bloodsell_entry = Bloodsell.objects.get(type=blood_type)
            price_per_unit = bloodsell_entry.price
            total_price = price_per_unit * int(quantity)
        except Bloodsell.DoesNotExist:
            messages.error(request, "Selected blood type is not available.")
            return redirect('bloodbuy')

        # Save the order details to the Confirmbuydetails model
        user = request.user
        confirm_order = Confirmbuydetails.objects.create(
            userid=user,
            type=blood_type,
            quantity=quantity,
            price=bloodsell_entry,  # ForeignKey reference to Bloodsell
            total_price=total_price,
            mobile=mobile,
            email=email
        )
        confirm_order.save()

        # Redirect to the confirmorder page
        messages.success(request, "Your blood purchase request has been confirmed successfully!")
        return redirect('confirmorder')

    else:
        # If accessed via GET, redirect to bloodbuy page
        return redirect('bloodbuy')

def contact(request):
    return render(request,'contactus.html')

# def confirmOrder(request):
#     userid=request.user
#     data = Confirmbuydetails.objects.filter(userid = userid)
#     context={}
#     context['cartlist']=data
#     total=0
#     gst=(18/100)
#     for cart in data:
#         total+=cart.total_price+gst
#     context['total']=total
#     return render(request,'confirmorder.html',context)

def confirmOrder(request):
    user = request.user
    # Fetch order details for the logged-in user
    orders = Confirmbuydetails.objects.filter(userid=user)
    context = {
        'cartlist': orders,
    }

    # Calculate total amount
    total = sum(order.total_price for order in orders)
    gst = total * 0.18  # 18% GST
    grand_total = total + gst

    context['total'] = total
    context['gst'] = gst
    context['grand_total'] = grand_total

    return render(request, 'confirmorder.html', context)

def makePayment(request):
    userid=request.user.id
    data = Confirmbuydetails.objects.filter(userid = userid)
    total=0
    gst=(18/100)
    for cart in data:
        total+=cart.total_price+gst
    client = razorpay.Client(auth=("rzp_test_HvIGtSTMlJFiX8", "DBCOWH1HZktdTqlBVBCLm6gX"))
    data = { "amount": total*100, "currency": "INR", "receipt": "" }
    payment = client.order.create(data=data)
    print(payment)
    context={}
    context['data']=payment
    return render(request,'pay.html',context)


def placeOrder(request,oid):
    userid = request.user
    # current_date = timezone.now().strftime('%Y%m%d-%H%M%S')
    # order_id = f'ORD{current_date}-{userid.id}-{blood_type}-{quantity}'
    cartlist = Confirmbuydetails.objects.filter(userid=userid)
    for cart in cartlist:
        order=Bloodorder.objects.create(
            orderid=oid,
            userid=cart.userid,
            type=cart.type,
            quantity=cart.quantity,
            mobile=cart.mobile,
            email=cart.email
        )
        order.save()
    cartlist.delete()

    messages.success(request, "Your blood purchase request has been submitted successfully!")

        # Generate PDF receipt
    pdf_buffer = generate_pdf_receipt(oid, cart.type, cart.quantity, cart.userid, cart.email)

        # Email with PDF attachment
    email_message = EmailMessage(
            subject="Blood Purchase Request Submitted",
            body=f"Dear {cart.userid},\n\nYour blood purchase request has been successfully submitted."
                 f"\nOrder ID: {oid}"
                 f"\nBlood Group: {cart.type}"
                 f"\nQuantity: {cart.quantity} Units (450ml-500ml)"
                 f"\nThank you for using our service!",
            from_email="support@example.com",  # Replace with your "from" email address
            to=[cart.email]
        )

        # Attach the PDF
    email_message.attach(f"Receipt_{oid}.pdf", pdf_buffer.getvalue(), "application/pdf")
    email_message.send(fail_silently=False)

    return redirect('/')  # Redirect to the homepage or a success page

    # Render the template with available blood types
