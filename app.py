import streamlit as st
import webbrowser
from collections import Counter

# -------------------- App Configuration --------------------
st.set_page_config(
    page_title="Fast Food Express",
    page_icon="🍔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------- Initialize Session Cart --------------------
if "cart" not in st.session_state:
    st.session_state.cart = []

# -------------------- Sample Menu Data --------------------
menu_items = [
    {"name": "Zinger Burger", "price": 300, "image": "images/burger.jpg"},
    {"name": "Fries", "price": 150, "image": "images/fries.jpg"},
    {"name": "Pizza Slice", "price": 250, "image": "images/pizza.jpg"},
    {"name": "Drink", "price": 80, "image": "images/drink.jpg"},
]

# -------------------- Sidebar Navigation --------------------
page = st.sidebar.radio("Navigate", ["🏠 Home", "🍔 Menu", "🛒 Cart", "ℹ️ About"])

# -------------------- 🏠 Home Page --------------------
if page == "🏠 Home":
    st.title("🍽️ Fast Food Express")
    st.markdown("### Delicious Taste at Your Fingertips")
    st.image("images/homePage-pic.jpg", use_container_width=True)
    st.markdown("""
        Welcome to **Fast Food Express**!  
        We bring you the best fast food experience with a variety of delicious items.  
        Order now and enjoy our quick delivery service!
    """)
    st.success("Click 'Menu' from sidebar to place your order.")

# -------------------- 🍔 Menu Page --------------------
elif page == "🍔 Menu":
    st.markdown("<style>/* custom styling */</style>", unsafe_allow_html=True)
    st.header("🍟 Our Menu")

    for idx, item in enumerate(menu_items):
        cols = st.columns([1, 3, 1])
        with cols[0]:
            st.image(item["image"], width=100)
        with cols[1]:
            st.markdown(f"**{item['name']}**  \nRs. {item['price']}")
        with cols[2]:
            if st.button("Add", key=f"add_{idx}"):
                st.session_state.cart.append(item)
                st.success(f"{item['name']} added to cart.")
        st.markdown("---")

# -------------------- 🛒 Cart Page --------------------
elif page == "🛒 Cart":
    st.header("🛒 Your Cart")

    if st.session_state.cart:
        cart_counter = Counter([item['name'] for item in st.session_state.cart])
        unique_items = {item['name']: item for item in st.session_state.cart}
        total = 0

        for idx, (item_name, qty) in enumerate(cart_counter.items()):
            item = unique_items[item_name]
            item_total = item['price'] * qty

            st.write(f"**{item_name}** — Rs. {item['price']} × {qty} = Rs. {item_total}")
            btn_cols = st.columns([1, 1, 1, 1])
            with btn_cols[0]:
                if st.button("➖", key=f"dec_{idx}"):
                    for i, it in enumerate(st.session_state.cart):
                        if it['name'] == item_name:
                            st.session_state.cart.pop(i)
                            break
                    st.rerun()
            with btn_cols[1]:
                if st.button("➕", key=f"inc_{idx}"):
                    st.session_state.cart.append(item)
                    st.rerun()
            with btn_cols[2]:
                if st.button("🗑️", key=f"del_{idx}"):
                    st.session_state.cart = [it for it in st.session_state.cart if it['name'] != item_name]
                    st.rerun()
            with btn_cols[3]:
                st.write(f"Qty: {qty}")
            st.markdown("---")
            total += item_total

        st.markdown(f"### 🧾 Total Bill: Rs. {total}")
        st.markdown("---")

        # -------------------- Complete Your Order Form --------------------
        with st.form("order_form"):
            st.markdown("### 📤 Complete Your Order")
            name = st.text_input("👤 Your Name", max_chars=50)
            phone = st.text_input("📱 WhatsApp Number", placeholder="e.g., 923001234567", max_chars=15)
            extra_msg = st.text_area("💬 Extra Instructions (optional)", placeholder="e.g., No onions, extra ketchup, etc.")

            submitted = st.form_submit_button("📤 Submit Order to WhatsApp")

            if submitted:
                name = name.strip()
                phone = phone.strip()
                extra_msg = extra_msg.strip()

                if not name or not phone:
                    st.error("⚠️ Please enter both your name and WhatsApp number.")
                elif not phone.isdigit() or not phone.startswith("92") or len(phone) < 11:
                    st.error("⚠️ Please enter a valid WhatsApp number starting with 92 (e.g., 923001234567).")
                elif not cart_counter:
                    st.error("🛒 Your cart is empty. Please add items before placing an order.")
                else:
                    order_lines = ["*Order Summary:*"]
                    for item_name, qty in cart_counter.items():
                        item = unique_items[item_name]
                        price = item["price"] * qty
                        order_lines.append(f"- {item_name} × {qty} = Rs. {price}")
                    order_lines.append(f"\n*Total:* Rs. {total}")
                    order_lines.append(f"*Customer:* {name}")
                    order_lines.append(f"*Contact:* {phone}")
                    if extra_msg:
                        order_lines.append(f"*Instructions:* {extra_msg}")

                    final_msg = "\n".join(order_lines)
                    encoded_msg = final_msg.replace(" ", "%20").replace("\n", "%0A")
                    wa_url = f"https://wa.me/923133850871?text={encoded_msg}"
                    webbrowser.open_new_tab(wa_url)
                    st.success("✅ Your order has been sent to WhatsApp successfully!")

    else:
        st.warning("🛒 Your cart is empty. Please add items from the menu.")

# -------------------- ℹ️ About Page --------------------
elif page == "ℹ️ About":
    st.markdown("""
        <style>
        .about-card {
            padding: 25px;
            border-radius: 16px;
            border: 1px solid #e2e8f0;
            box-shadow: 0 4px 16px rgba(0,0,0,0.05);
        }
        .about-card h1 {
            color: #fffff;
            font-weight: 700;
            font-size: 2rem;
            margin-bottom: 16px;
        }
        .about-card p {
            font-size: 1.1rem;
            color: #374151;
        }
        .about-card a {
            color: #2563eb;
            font-weight: 600;
            text-decoration: none;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="about-card"><h1>ℹ️ About Fast Food Express</h1>', unsafe_allow_html=True)
    st.markdown("""
    <p>Welcome to <strong>Fast Food Express</strong>! We are dedicated to bringing you the best fast food experience with a wide variety of delicious items.</p>
    <p>From sizzling burgers to crispy fries and refreshing drinks — we bring the taste right to your doorstep.</p>
    <p><strong>⏰ Open Hours:</strong> 12:00 PM to 12:00 AM</p>
    <p><strong>📍 Location:</strong> <a href="https://maps.google.com" target="_blank">Visit us on Google Maps</a></p>
    <p><strong>📞 Contact:</strong> <a href="tel:+923133850871">+92 313 3850871</a></p>
    <p>Follow us on <a href="https://www.linkedin.com/in/farooque-malik871" target="_blank">LinkedIn</a></p>
    </div>
    """, unsafe_allow_html=True)

st.markdown(
    """
    <div style="text-align: center; color: gray; margin-top: 50px;">
        © 2025 FastFoodies | Made with ❤️ by Farooque Malik
    </div>
    """,
    unsafe_allow_html=True
)
