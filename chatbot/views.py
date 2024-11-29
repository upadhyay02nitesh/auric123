from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from .models import Chat
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
from app.models import Cart, Customer, OrderPlaced, OrderItem,Product
from django.contrib.auth.models import User
# Load environment variables
load_dotenv()

# Get Google Gemini API key from environment
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("Google Gemini API key is missing. Please set it in your environment.")

# Configure Google Gemini
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro")


def generate_response(query, user):
    print(user)
    # Define the role of the AI chatbot as an eCommerce support agent for AuricMart
    system_message = """You are an AI support agent for AuricMart, an eCommerce platform.  
    Your primary responsibility is to assist customers with the following:  

    ### Areas of Support:
    1. **Product Inquiries**  
    - Availability of products.  
    - Product specifications, features, and recommendations.  

    2. **Order Placement**  
    - How to browse and select products.  
    - Adding items to the cart and proceeding to checkout.  
    - Payment methods supported.  

    3. **Order Status and Tracking**  
    - Providing order status updates.  
    - Sharing tracking information for shipped orders.  

    4. **Shipping Information**  
    - Delivery timelines based on customer location.  
    - Modifying delivery addresses if applicable.  

    5. **Return, Refund, and Exchange Policies**  
    - Assisting with the process to initiate returns or exchanges.  
    - Explaining refund timelines and methods.  

    6. **Downloading Invoices**  
    - Guide customers to log into their AuricMart account.  
    - Navigate to the “Orders” section, select the relevant order, and click “Download Invoice.”  

    7. **Technical Issues**  
    - Resolving login or account-related issues.  
    - Addressing payment processing problems.  
    - Assisting with website navigation.  

    ### Response Guidelines:
    - **Stay Relevant**: Only answer the specific question asked by the customer. Avoid providing additional or unrelated information.  
    - **Escalate If Needed**: If the query cannot be resolved or does not match your available data, respond with: **"Contact the support team for assistance."**  
    - Support Contact: Email at **auricmart@gmail.com** or call **+91-6268944329 / +91-6264534556.**  
    - **Tone and Clarity**: Always maintain a professional, friendly, and concise tone. Ensure responses are clear and directly address the customer’s concern.  

    ### Prohibited Actions:
    - Do not provide speculative or uncertain information.  
    - Do not include details not explicitly requested by the customer.  

    Your goal is to ensure a seamless and satisfying customer experience by addressing their concerns accurately and efficiently.
    """


    # Fetch customer profile information
    customer = Customer.objects.filter(user=user).first()
    customer_info = f"Customer Profile: Name: {customer.name if User else 'No profile found'}, Location: {customer.city if customer else 'Unknown'},Gmail: {customer.Gmail if customer else 'Unknown'},mobile_number: {customer.mobile_number if customer else 'Unknown'}"
    products = Product.objects.all()
    product_list = []

    for product in products:
        product_details = f"""
        Product Title: {product.title if product.title else 'Not available'}
        Selling Price: ₹{product.selling_price if product.selling_price else 'Not available'}
        Discounted Price: ₹{product.discounted_price if product.discounted_price else 'Not available'}
        Description: {product.description if product.description else 'No description provided'}
        Brand: {product.brand if product.brand else 'Not specified'}
        Category: {product.category if product.category else 'Uncategorized'}
        FAQ: {product.FAQ if product.FAQ else 'No FAQ available'}
        Product Analysis: <a href="{product.Product_Analysis}" target="_blank">{product.Product_Analysis if product.Product_Analysis else 'No analysis available'}</a>
        Product Image: <a href="{product.product_image.url}" target="_blank">View Image</a>
        Created At: {product.created_at if product.created_at else 'Unknown'}
        Updated At: {product.updated_at if product.updated_at else 'Unknown'}
        """
        product_list.append(product_details.strip())

    # Combine all product information
    product_info_one = "\n\n".join(product_list)

    # User = User.objects.filter(user=user).first()
    # Userr_info = f"Customer Profile: Name: {User.name if User else 'No profile found'}, Email: {User.email if User else 'Unknown'}"

    # Fetch the user's most recent order
    recent_order = OrderPlaced.objects.filter(user=user).order_by('-ordered_date').first()
    order_info = None
    if recent_order:
        order_info = f"Recent Order ID: {recent_order.id}, Status: {recent_order.status}, Total Cost: {recent_order.total_cost}"
    else:
        order_info = "No recent orders found."

    # Fetch items in the user's cart
    cart_items = Cart.objects.filter(user=user)
    cart_info = "Cart Items: "
    if cart_items.exists():
        cart_info += ", ".join([f"{item.product.title} (Qty: {item.quantity}, Price: {item.total_cost})" for item in cart_items])
    else:
        cart_info = "No items in your cart."

    # Fetch product information related to the recent order
    product_info = None
    if recent_order:
        order_items = OrderItem.objects.filter(order=recent_order)
        if order_items.exists():
            product_info = f"Product in Recent Order: {order_items.first().product.title}"
        else:
            product_info = "No product information available for this order."

    # Custom message if data is missing or unavailable
    support_message = (
        "If you need any further assistance or if we could not find the information you're looking for, "
        "please contact our support team: \n\n"
        "Email: auricmart@gmail.com \n"
        "Telephone: +91-6268944329 / +91-6264534556"
    )

    # Combine all the data into a single response message
    response_data = [
        system_message,
        customer_info,
        product_info_one,
        order_info,
        cart_info,
        product_info,
        support_message  # Always include support message if data is missing
    ]

    # Add the user’s query to the messages for context
    user_message = f"User's Query: {query}"
    response_data.append(user_message)

    print(f"Sending messages to Google Gemini: {response_data}")  # Log for debugging

    try:
        # Check if the query matches any of the available data and return a response
        if not any(query.lower() in info.lower() for info in response_data):
            return "For further assistance, please contact our support team:\n\nEmail: auricmart@gmail.com\nTelephone: +91-6268944329 / +91-6264534556"

        # Send the combined message to Google Gemini for response generation
        response = llm.invoke(response_data)

        # Ensure the response has content
        response_content = response.content if hasattr(response, 'content') else "Sorry, I couldn't understand your question. Could you please clarify?"

        # Log the response for debugging purposes
        print(f"Received response: {response_content}")

        return response_content

    except Exception as e:
        print(f"Error with Google Gemini: {e}")
        return f"Error: {e}"  # Return the actual error message for debugging

def chatbot(request):
    """
    Handle the chatbot interface and queries.
    """
    if not request.user.is_authenticated:
        return render(request, 'chatbot/chatbot.html', {'chats': []})

    # Get the chat history for the authenticated user
    chats = Chat.objects.filter(user=request.user).order_by('-created_at')

    if request.method == 'POST':
        message = request.POST.get('message', '').strip()

        if not message:
            response = "Please enter a message to proceed."
        else:
            # Get response from Google Gemini with custom data about the user and their orders
            response = generate_response(message, request.user)

        # Save the chat to the database
        chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now())
        chat.save()

        # Return the response as JSON
        return JsonResponse({'message': message, 'response': response})

    return render(request, 'chatbot/chatbot.html', {'chats': chats})
