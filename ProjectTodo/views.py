
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.dateparse import parse_datetime
import json
from django.contrib.auth import get_user_model  
from .models import Task
from django.contrib.auth import authenticate, login, logout
from functools import wraps

User = get_user_model() 

# decorator for authentication verification
def login_required_json(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Authentication required"}, status=401)
        return view_func(request, *args, **kwargs)
    return wrapper


# View all users
@csrf_exempt
@require_http_methods(["GET","POST"])
@login_required_json
def view_users(request):
    users = list(User.objects.values("id", "username", "email", "first_name", "last_name", "contact_no"))
    return JsonResponse({"users": users})

# View all tasks
@csrf_exempt
@require_http_methods(["GET","POST"])
@login_required_json
def view_tasks(request):
    tasks = Task.objects.filter(user=request.user)
    task_list = [{
        "id": task.id,
        "title": task.title,
        "due_date": task.due_date,
        "is_completed": task.is_completed
    } for task in tasks]
    return JsonResponse({"user": request.user.username, "tasks": task_list})


# Add a task
@csrf_exempt
@require_http_methods(["POST"])
@login_required_json
def add_task(request):
    try:
        data = json.loads(request.body)
        title = data.get("title")
        due_date = data.get("due_date")
        is_completed = data.get("is_completed", False)
        
        if not title:
            return JsonResponse({"error": "Title is required"}, status=400)

       

        task = Task(
            title=title,
            due_date=parse_datetime(due_date) if due_date else None,
            is_completed=bool(is_completed),
            user=request.user  # use the logged-in user 
        )
        task.save()
        return JsonResponse({"message": f"Task '{task.title}' added!", "task_id": task.id})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

# Remove a task
@csrf_exempt
@require_http_methods(["POST"])
@login_required_json
def remove_task(request):
    try:
        data = json.loads(request.body)
        task_id = data.get("id")
        if not task_id:
            return JsonResponse({"error": "Task ID is required"}, status=400)
        task = Task.objects.filter(id=task_id,user=request.user).first()
        if task:
            task.delete()
            return JsonResponse({"message": f"Task '{task.title}' removed"})
        else:
            return JsonResponse({"error": "Task not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

# Update a task
@csrf_exempt
@require_http_methods(["POST"])
@login_required_json
def update_task(request):
    try:
        data = json.loads(request.body)
        task_id = data.get("id")

        if not task_id:
            return JsonResponse({"error": "Task ID is required"}, status=400)

        task = Task.objects.filter(id=task_id,user=request.user).first()

        if not task:
            return JsonResponse({"error": "Task not found"}, status=404)

        title = data.get("title")
        due_date = data.get("due_date")
        is_completed = data.get("is_completed")

        if title is not None:
            task.title = title
        if due_date is not None:
            task.due_date = parse_datetime(due_date)
        if is_completed is not None:
            task.is_completed = bool(is_completed)
        task.save()

        return JsonResponse({"message": f"Task '{task.title}' updated successfully"})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

# View tasks of a specific user
@csrf_exempt
@require_http_methods(["GET","POST"])
@login_required_json
def user_tasks(request):
    try:
        user = request.user   # Use the custom user model
        tasks = Task.objects.filter(user=user)
        task_list = [{
            "id": task.id,
            "title": task.title,
            "due_date": task.due_date,
            "is_completed": task.is_completed
        } for task in tasks]
        return JsonResponse({"user": user.username, "tasks": task_list})
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)
    
@csrf_exempt
@require_http_methods(["POST"])

def register_user(request):
    try:
        data = json.loads(request.body)
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        contact_no = data.get("contact_no", "")
        first_name = data.get("first_name", "")
        last_name = data.get("last_name", "")

        if not username or not password or not email:
            return JsonResponse({"error": "Username, email, and password are required"}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username already taken"}, status=400)

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            contact_no=contact_no,
            first_name=first_name,
            last_name=last_name
        )
        return JsonResponse({"message": f"User {user.username} registered successfully"})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
@csrf_exempt
def user_login (request):
    if request.method == "POST" :
        data = json.loads(request.body) 
        username = data.get("username")
        password = data.get("password")

        user = authenticate(request, username=username , password = password )
        if user is not None:
            login(request, user)
            return JsonResponse({"message": "Login successful"})
        else:
              return JsonResponse({"message": "Login unsuccessful"}, status=401)


@csrf_exempt
@require_http_methods(["POST"])
def logout_user(request):
    logout(request)
    return JsonResponse({"message": "Logged out successfully"})


# Test endpoint (just for debugging)
@csrf_exempt
@require_http_methods(["GET"])
def test(request):
    return JsonResponse({"success": True})
