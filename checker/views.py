from django.shortcuts import render
from .models import Disease, Symptom, Feedback
from django.core.management import call_command
from django.shortcuts import redirect
from django.contrib import messages



def home(request):
    # Temporary migration fix for Render
    try:
        call_command("migrate", interactive=False)
    except Exception as e:
        print("Migration error:", e)

    symptoms = Symptom.objects.all()
    results = []
    diseases = Disease.objects.prefetch_related('symptoms')

    if request.method == 'POST':
        selected_symptom_ids = request.POST.getlist('symptoms')
        age = int(request.POST.get('age', 0))
        gender = request.POST.get('gender', '').lower()

        selected_symptoms = set(Symptom.objects.filter(id__in=selected_symptom_ids))
        disease_scores = []

        for disease in diseases:
            disease_symptoms = set(disease.symptoms.all())
            overlap = len(selected_symptoms & disease_symptoms)
            if overlap > 0:
                score = overlap
                if gender == 'sow' and any(word in disease.name.lower() for word in ['ovarian', 'uterus']):
                    score += 1
                if gender == 'boar' and 'testicular' in disease.name.lower():
                    score += 1
                if age > 4 and any(word in disease.name.lower() for word in ['cancer', 'tumor']):
                    score += 1
                if age < 2 and 'respiratory' in disease.name.lower():
                    score += 1

                disease_scores.append((disease, score))

        disease_scores.sort(key=lambda x: x[1], reverse=True)
        results = disease_scores[:3]

    return render(request, 'checker/home.html', {'symptoms': symptoms, 'results': results})


def submit_feedback(request):
    if request.method == "POST":
        rating = request.POST.get("rating")
        message = request.POST.get("message")

        Feedback.objects.create(
            rating=rating,
            message=message
        )

        messages.success(request, "Thank you for your feedback! ❤️")

        return redirect('home')