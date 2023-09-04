from.models import Category

def categories(request):
    categories = Category.objects.all()  # Fetch all categories from the database
    return {'categories': categories}  # Return the categories as a dictionary
