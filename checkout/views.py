from django.shortcuts import (
    render, redirect,
    reverse, get_object_or_404,
    HttpResponse
)
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm
from .models import Order, OrderLineItem

from products.models import Product, ProductSelect, ProductOption
from bag.contexts import bag_content

from accounts.models import Account

import stripe
import json


@require_POST
def cache_checkout_data(request):
    """
    Determines whether user has save info box checked
    Returns this to the webhook
    Adapted from Boutique Ado
    """
    try:
        # POST request with client secret and payment intent
        # payment intent id
        pid = request.POST.get('client_secret').split('_secret')[0]

        # stipe keys is used to modify payment intent
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'current_bag': json.dumps(request.session.get('current_bag', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })

        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be \
            processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)


@login_required
def checkout(request):
    """
    Begins checkout process.
    Directs user to Order Review page.
    """
    current_bag = request.session.get('current_bag', {})
    if not current_bag:
        messages.error(request, "There is nothing in your bag")
        return redirect(reverse('all_products'))

    return redirect(reverse('order_review'))


@login_required
def order_review(request):
    """
    Crispy form allowing user to enter their information.
    Removes navbar and footer from page to follow eCommerce conventions.
    Hide Elements ref: https://tinyurl.com/yp2buee3
    """

    current_bag = request.session.get('current_bag', {})
    if not current_bag:
        messages.error(request, "There is nothing in your bag")
        return redirect(reverse('shop'))

    context = {
        'active_page': 'order_review',
        'navbar': False,
        'footer': False,
    }

    return render(request, 'checkout/order_review.html', context)

@login_required
def order_details(request):
    """
    Crispy form allowing user to enter their information.
    Removes navbar and footer from page to follow eCommerce conventions.
    Hide Elements ref: https://tinyurl.com/yp2buee3
    Code for this function all adapted from Boutique Ado Mini Project
    """
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        current_bag = request.session.get('current_bag', {})

        form_data = {
            'first_name': request.POST['first_name'],
            'last_name': request.POST['first_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
        }
        order_form = OrderForm(form_data)

        if order_form.is_valid():
            # Get payment intent id if order is valid
            # false commit prevents multiple save events being executed
            order = order_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid

            # dump shopping bag in json string
            order.original_bag = json.dumps(current_bag)

            # save order
            order.save()

            # get products
            for item_id, item_data in current_bag.items():
                try:
                    # get product id out of bag
                    product = Product.objects.get(id=item_id)
                    for select, quantity in item_data[
                                'items_by_select'].items():

                        # get selected option (size or class)
                        product_options = ProductOption.objects.get(
                            product_option=select)

                        # create relationship between option and product
                        product_select = ProductSelect.objects.filter(
                            product_select=product_options,
                            product=product)

                        # assign it to the order
                        product_selected = product_select[0]

                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            quantity=quantity,
                            product_select=product_selected,
                        )
                        order_line_item.save()

                        # reduces selected option stock count
                        # by quantity ordered
                        product_selected.stock_count -= (
                                order_line_item.quantity
                            )
                        product_selected.save()

                except Product.DoesNotExist:
                    # if product is not found
                    messages.error(request, (
                        "One of the items wasn't found in our database."
                        "Call the boxing club for assistance!")
                    )
                    order.delete()
                    return redirect(reverse('shopping_bag'))
            # whether user wants to save produle info to session
            request.session['save_info'] = 'save-info' in request.POST
            
             # Email Order Confirmation
            msg_content = {
                "order": order,
                "items": [item for item in order.lineitems.all()],
                "contact_email": os.environ["EMAIL_USER"],
            }
            msg_plain = render_to_string(
                "checkout/order_confirmation_email.txt",
                msg_content,
            )
            msg_html = render_to_string(
                "checkout/order_confirmation_email.html",
                msg_content,
            )
            subject = f"Saviours Order Confirmation: #{order.order_number}"
            from_email = os.environ["EMAIL_USER"]
            try:
                send_mail(
                    subject,
                    msg_plain,
                    from_email,
                    [order.user.email],
                    fail_silently=True,
                    html_message=msg_html,
                )
            except BadHeaderError:
                return HttpResponse("Invalid header found.")

            # redirect to success page
            return redirect(
                reverse('order_complete', args=[order.order_number]))

        else:
            messages.error(request, 'There was an error with your order form. \
            Please double check your information.')
            context["order_form"] = form

    else: # GET request
        # Add user name to form by default
        details = {
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
        }
        try:
            # add user address (if exists)
            details.update(model_to_dict(request.user.address))
        except Address.DoesNotExist:
            pass
        finally:
            order_form = OrderForm(initial=details)
        # Load bag
        current_bag = request.session.get('current_bag', {})
        if not current_bag:
            messages.error(request, "There is nothing in your bag")
            return redirect(reverse('shopping_bag'))

        # get order bag dictionary
        order_bag = bag_content(request)

        # get bag total key
        total = order_bag['grand_total']

        # x100 and rounded to 0.00 (gets integer)
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

    if not stripe_public_key:
        messages.warning(request, 'Stripe Public Key is missing, \
            Did you forget to set it in your environment?')

    context = {
        'order_form': order_form,
        'active_page': 'order_details',
        'navbar': False,
        'footer': False,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, 'checkout/order_details.html', context)


@login_required
def order_complete(request, order_number):
    """
    Handle successful checkouts
    """
    # check if user wanted to save info
    save_info = request.session.get('save_info')

    # get order to send to template
    order = get_object_or_404(Order, order_number=order_number)

    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        # Attach the user's profile to the order
        order.user_profile = profile
        order.save()

        # Save the user's info
        if save_info:
            profile_data = {
                'default_full_name': order.full_name,
                'default_phone_number': order.phone_number,
                'default_street_address1': order.street_address1,
                'default_street_address2': order.street_address2,
                'default_county': order.county,
                'default_town_or_city': order.town_or_city,
                'default_postcode': order.postcode,
                'defalt_country': order.country,
            }

            # update profile info updated above
            user_profile_form = ProfileForm(profile_data, instance=profile)
            if user_profile_form.is_valid():
                user_profile_form.save()

    # delete session bag
    if 'current_bag' in request.session:
        del request.session['current_bag']

    context = {
        'order': order,
        'active_page': 'order_complete',
    }

    return render(request, 'checkout/order_complete.html', context)
