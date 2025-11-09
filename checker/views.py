from django.shortcuts import render
from .models import Disease, Symptom


def home(request):
    diseases = Disease.objects.prefetch_related('symptoms')
    symptoms = Symptom.objects.all()
    results = None

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
