from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .models import Equipment, Message, Conversation
from .helper import generate_gpt_response
from django.contrib import messages

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('inventory')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def inventory(request):
    equipments = Equipment.objects.filter(quantity__gt=0).order_by('-created_at')
    return render(request, 'inventory.html', {'equipments': equipments})

@login_required
def add_equipment(request):
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        quantity = request.POST.get('quantity')

        # Validation
        if not name or not quantity:
            messages.error(request, "Name and Quantity are required!")
            return redirect('inventory')

        # Create new equipment
        Equipment.objects.create(
            name=name,
            description=description,
            quantity=int(quantity)
        )
        messages.success(request, "Equipment added successfully!")
        return redirect('inventory')

    return redirect('inventory')

@login_required
def delete_equipment(request, equipment_id):
    equipment = get_object_or_404(Equipment, id=equipment_id)
    equipment.delete()
    return redirect('inventory')

@login_required
def ai_experiment_view(request, conversation_id=None):
    conversations = Conversation.objects.all().order_by('-created_at')
    selected_conversation = None
    
    if conversation_id:
        selected_conversation = get_object_or_404(Conversation, id=conversation_id)

    return render(request, 'ai_experiment.html', {
        'conversations': conversations,
        'selected_conversation': selected_conversation,
    })


@login_required
def send_message(request, conversation_id):
    if request.method == 'POST':
        content = request.POST.get('message_content')
        conversation = get_object_or_404(Conversation, id=conversation_id)
        if conversation.user != request.user:
            return redirect('ai_experiment')
        Message.objects.create(
            conversation=conversation,
            content=content,
            is_user=True,
        )
        available_equipements = Equipment.objects.all()
        gpt_response = generate_gpt_response(available_equipements, content)
        Message.objects.create(
            conversation=conversation,
            content=gpt_response,
            is_user=False,
        )
        
        return redirect('ai_experiment_detail', conversation_id=conversation.id)

@login_required
def add_conversation(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        conversation = Conversation.objects.create(
            title=title,
            user=request.user,
        )
        return redirect('ai_experiment_detail', conversation_id=conversation.id)
    return redirect('ai_experiment')


@login_required
def delete_conversation(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id, user=request.user)
    
    if conversation.user != request.user:
        return redirect('ai_experiment')
    
    conversation.delete()
    
    return redirect('ai_experiment')