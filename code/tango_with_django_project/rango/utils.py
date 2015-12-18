from rango.models import Category

"""
Helper function for suggest_category() view. Modified from the get_category_list templatetag that was previously used for the sidebar.
"""

def get_category_list(max_results=0, starts_with=''):
    cat_list = []
    print starts_with
    if starts_with:
        #_istartswith is the case-insensitive way to search the
        # Category model for the term in the "name" field
        cat_list = Category.objects.filter(name__istartswith=starts_with)

    if max_results>0:
        if len(cat_list) > max_results:
            cat_list = cat_list[:max_results]

    return cat_list