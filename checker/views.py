from django.shortcuts import render
from .models import Disease

def home(request):
    result = None
    if request.method == 'POST':
        symptoms_input = request.POST.get('symptoms', '')
        user_symptoms = set(s.strip().lower() for s in symptoms_input.split(',') if s.strip())

        disease_scores = []
        for disease in Disease.objects.prefetch_related('symptoms').all():
            disease_symptoms = set(s.name.lower() for s in disease.symptoms.all())
            score = len(user_symptoms & disease_symptoms)
            if score > 0:
                disease_scores.append((disease.name, score))

        disease_scores.sort(key=lambda x: x[1], reverse=True)
        result = [disease for disease, score in disease_scores]

    return render(request, 'checker/home.html', {'result': result})