import streamlit as st
from src.logic import RecipeManager

st.set_page_config(page_title="Recipe Finder & Manager", page_icon="🍽️", layout="wide")
st.title("🍽️ Recipe Finder & Manager")

# ----------------- Initialize Manager -----------------
manager = RecipeManager()

# ----------------- Default user -----------------
DEFAULT_USER_ID = 1  # Ensure this user exists in your users table

# ----------------- Sidebar navigation -----------------
page = st.sidebar.radio("Go to", ["All Recipes", "Saved Recipes"])

# ----------------- ALL RECIPES PAGE -----------------
if page == "All Recipes":
    # Show/Hide Add Recipe Form
    if "show_form" not in st.session_state:
        st.session_state.show_form = False

    if st.button("➕ Add Recipe"):
        st.session_state.show_form = not st.session_state.show_form

    if st.session_state.show_form:
        st.header("Add New Recipe")
        with st.form("add_recipe_form"):
            title = st.text_input("Title")
            desc = st.text_area("Description")
            instructions = st.text_area("Instructions")
            image_url = st.text_input("Image URL")
            prep_time = st.text_input("Prep Time")
            ingredients = st.text_area("Ingredients")
            allergens = st.text_input("Allergens")
            submitted = st.form_submit_button("Submit Recipe")
            if submitted:
                resp = manager.add_recipe({
                    "user_id": DEFAULT_USER_ID,
                    "title": title,
                    "description": desc,
                    "instructions": instructions,
                    "image_url": image_url,
                    "prep_time": prep_time,
                    "ingredients": ingredients,
                    "allergens": allergens
                })
                if resp["success"]:
                    st.success("✅ Recipe added!")
                    st.session_state.show_form = False
                else:
                    st.error(f"⚠️ {resp['Message']}")

    # Search Recipes
    st.header("🔍 Search Recipes")
    search_query = st.text_input("Search by title")

    # Fetch all recipes
    if search_query:
        resp = manager.search_recipes_by_title(search_query)
    else:
        resp = manager.fetch_all_recipes()
    recipes = resp.get("data", [])

    # Get saved recipes
    saved_resp = manager.fetch_saved_recipes(DEFAULT_USER_ID)
    saved_recipe_ids = [r["recipe_id"] for r in saved_resp.get("data", [])]

    # Display recipes
    if recipes:
        for r in recipes:
            st.divider()
            col_img, col_info = st.columns([1, 3])

            with col_img:
                if r.get("image_url"):
                    st.image(r["image_url"], use_container_width=True)

            with col_info:
                st.subheader(r["title"])
                st.write(f"⏱️ Prep Time: {r.get('prep_time','N/A')}")
                st.write(f"📝 {r['description']}")
                st.write(f"🥦 Ingredients: {r.get('ingredients','N/A')}")
                st.write(f"⚠️ Allergens: {r.get('allergens','None')}")
                if r.get("instructions"):
                    with st.expander("📖 Instructions"):
                        st.code(r["instructions"])

                # Action buttons
                action_col1, action_col2, action_col3 = st.columns(3)

                # Edit
                with action_col1:
                    with st.form(f"edit_form_{r['recipe_id']}"):
                        new_title = st.text_input(f"Title {r['recipe_id']}", r["title"])
                        new_desc = st.text_area(f"Description {r['recipe_id']}", r["description"])
                        submitted = st.form_submit_button(f"📝 Update {r['recipe_id']}")
                        if submitted:
                            update_resp = manager.modify_recipe(
                                r["recipe_id"],
                                {"title": new_title, "description": new_desc}
                            )
                            if update_resp["success"]:
                                st.success("✅ Updated!")
                            else:
                                st.error(f"⚠️ {update_resp['Message']}")

                # Delete
                #with action_col2:
                #    if st.button(f"❌ Delete {r['recipe_id']}", key=f"delete_{r['recipe_id']}"):
                 #       delete_resp = manager.remove_recipe(r["recipe_id"])
                  #      if delete_resp["success"]:
                   #         st.warning("🗑️ Deleted!")
                    #    else:
                     #       st.error(f"⚠️ {delete_resp['Message']}")

                # Save / Unsave toggle
                with action_col3:
                    if r["recipe_id"] in saved_recipe_ids:
                        if st.button(f"❌ Unsave", key=f"unsave_{r['recipe_id']}"):
                            unsave_resp = manager.unsave_user_recipe(DEFAULT_USER_ID, r["recipe_id"])
                            if unsave_resp["success"]:
                                st.warning("🗑️ Unsaved!")
                            else:
                                st.error(f"⚠️ {unsave_resp['Message']}")
                    else:
                        if st.button(f"📌 Save", key=f"save_{r['recipe_id']}"):
                            save_resp = manager.save_user_recipe(DEFAULT_USER_ID, r["recipe_id"])
                            if save_resp["success"]:
                                st.success("✅ Saved!")
                            else:
                                st.error(f"⚠️ {save_resp['Message']}")
    else:
        st.info("No recipes found.")

# ----------------- SAVED RECIPES PAGE -----------------
elif page == "Saved Recipes":
    st.header("💾 Your Saved Recipes")
    saved_resp = manager.fetch_saved_recipes(DEFAULT_USER_ID)
    saved_recipe_ids = [r["recipe_id"] for r in saved_resp.get("data", [])]

    if saved_recipe_ids:
        all_resp = manager.fetch_all_recipes()
        all_recipes = all_resp.get("data", [])
        for r in all_recipes:
            if r["recipe_id"] in saved_recipe_ids:
                st.divider()
                col_img, col_info = st.columns([1, 3])

                with col_img:
                    if r.get("image_url"):
                        st.image(r["image_url"], use_container_width=True)

                with col_info:
                    st.subheader(r["title"])
                    st.write(f"📝 {r['description']}")
                    st.write(f"⏱️ Prep Time: {r.get('prep_time','N/A')}")
                    st.write(f"🥦 Ingredients: {r.get('ingredients','N/A')}")
                    st.write(f"⚠️ Allergens: {r.get('allergens','None')}")
                    if r.get("instructions"):
                        with st.expander("📖 Instructions"):
                            st.code(r["instructions"])
    else:
        st.info("You have no saved recipes yet.")