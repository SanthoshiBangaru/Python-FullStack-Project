import streamlit as st
from src.logic import (
    signup_user, login_user,
    create_recipe, get_recipes, update_recipe, delete_recipe,
    save_recipe, get_saved_recipes
)

st.set_page_config(page_title="Recipe Finder", page_icon="🍳", layout="wide")

if "user" not in st.session_state:
    st.session_state.user = None

# ------------------- Authentication -------------------
def show_login():
    st.subheader("🔑 Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = login_user(email, password)
        if user:
            st.session_state.user = user
            st.success(f"✅ Welcome back {user['first_name']}!")
            st.experimental_rerun()
        else:
            st.error("❌ Invalid credentials")

def show_signup():
    st.subheader("📝 Signup")
    first = st.text_input("First Name")
    last = st.text_input("Last Name")
    email = st.text_input("Email")
    mobile = st.text_input("Mobile")
    password = st.text_input("Password", type="password")
    if st.button("Create Account"):
        if first and last and email and mobile and password:
            try:
                signup_user(first, last, email, mobile, password)
                st.success("✅ Account created! Please login now.")
            except ValueError as e:
                st.error(f"⚠️ {str(e)}")
        else:
            st.error("⚠️ All fields are required")

# ------------------- Main App -------------------
if not st.session_state.user:
    choice = st.radio("Choose an option", ["Login", "Signup"])
    if choice == "Login":
        show_login()
    else:
        show_signup()
else:
    user = st.session_state.user
    st.title(f"🍳 Recipe Finder - Welcome {user['first_name']}!")

    if st.button("Logout"):
        st.session_state.user = None
        st.experimental_rerun()

    # ----- Add Recipe -----
    st.header("➕ Create a New Recipe")
    title = st.text_input("Recipe Title")
    desc = st.text_area("Description")
    instructions = st.text_area("Instructions")
    image_url = st.text_input("Image URL")
    prep_time = st.text_input("Prep Time")
    ingredients = st.text_area("Ingredients")
    allergens = st.text_input("Allergens")

    if st.button("Add Recipe"):
        if title and desc:
            create_recipe(
                user["user_id"], title, desc, instructions,
                image_url, prep_time, ingredients, allergens
            )
            st.success("✅ Recipe added!")
            st.experimental_rerun()
        else:
            st.error("⚠️ Title and Description are required")

    # ----- My Recipes -----
    st.header("📖 My Recipes")
    search = st.text_input("Search by name")
    recipes = get_recipes(user["user_id"])
    if search:
        recipes = [r for r in recipes if search.lower() in r["title"].lower()]

    if recipes:
        cols = st.columns(2)
        for idx, r in enumerate(recipes):
            with cols[idx % 2]:
                st.image(r.get("image_url", ""), width=250)
                st.subheader(r["title"])
                st.write(f"⏱️ Prep Time: {r.get('prep_time','N/A')}")
                st.write(f"📝 {r['description']}")
                st.write(f"🥦 Ingredients: {r.get('ingredients','N/A')}")
                st.write(f"⚠️ Allergens: {r.get('allergens','None')}")
                if r.get("instructions"):
                    with st.expander("📖 Instructions"):
                        st.code(r["instructions"])

                c1, c2, c3 = st.columns(3)
                with c1:
                    if st.button(f"📝 Update {r['recipe_id']}"):
                        new_title = st.text_input(f"New title {r['recipe_id']}", r["title"])
                        new_desc = st.text_area(f"New desc {r['recipe_id']}", r["description"])
                        update_recipe(r["recipe_id"], {"title": new_title, "description": new_desc})
                        st.success("✅ Updated!")
                        st.experimental_rerun()
                with c2:
                    if st.button(f"❌ Delete {r['recipe_id']}"):
                        delete_recipe(r["recipe_id"])
                        st.warning("🗑️ Deleted!")
                        st.experimental_rerun()
                with c3:
                    if st.button(f"📌 Save {r['recipe_id']}"):
                        save_recipe(user["user_id"], r["recipe_id"])
                        st.success("✅ Saved!")

    else:
        st.info("No recipes found. Add some!")

    # ----- Saved Recipes -----
    st.header("📌 Saved Recipes")
    saved = get_saved_recipes(user["user_id"])
    if saved:
        for s in saved:
            st.write(f"✅ Recipe ID: {s['recipe_id']}")
    else:
        st.info("No saved recipes yet.")