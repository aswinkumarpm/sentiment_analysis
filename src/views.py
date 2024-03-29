from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from transformers import pipeline
from .models import UserInput, Category
from django.core.serializers.json import DjangoJSONEncoder
from .forms import CategoryForm
import json
import csv
from django.http import HttpResponse


def download_category_csv(request, category_name):
    user_inputs = UserInput.objects.filter(category__name=category_name)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{category_name}_sentiments.csv"'
    csv_writer = csv.writer(response)
    csv_writer.writerow(['Serial number', 'Review', 'Sentiment'])
    for index, user_input in enumerate(user_inputs, start=1):
        csv_writer.writerow([index, user_input.sentence, user_input.sentiment_label])

    return response


def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()

    return render(request, 'category_new.html', {'form': form})


@csrf_exempt
def add_sentence(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        sentence = data.get('newSentence')
        categories = list(Category.objects.all().values_list('name', flat=True))

        classifier = pipeline("zero-shot-classification")

        result = classifier(sentence, categories)

        sentiment_analyzer = pipeline("sentiment-analysis")

        sentiment_result = sentiment_analyzer(sentence)
        sentiment_label = sentiment_result[0]['label']
        sentiment_score = sentiment_result[0]['score']

        print(sentiment_label)
        print(sentiment_score)

        matching_categories = []
        matching_category_ids = []

        for label, score in zip(result['labels'], result['scores']):
            print(f"- {label} -{score}")
            if score > 0.5:
                category_instance = Category.objects.get(name=label)
                matching_categories.append(label)
                matching_category_ids.append(category_instance.id)
                UserInput.objects.create(
                    sentence=sentence,
                    category=category_instance,
                    sentiment_label=sentiment_label,
                    sentiment_score=score
                )

        if matching_categories:
            return JsonResponse({"success": True, "status_code": 200, "category_id": matching_category_ids[0], "msg": "Given Sentence Classified"})
        else:
            return JsonResponse({"success": False, "status_code": 500, "msg": "No matching categories found. Redirecting to first Category page", "category_id": 1 })
    else:
        return JsonResponse({"success": False, "status_code": 500})


def category_detail(request, category_id):
    user_inputs = UserInput.objects.filter(category=category_id).values()
    user_inputs_list = list(user_inputs)
    return JsonResponse({'user_inputs': user_inputs_list}, encoder=DjangoJSONEncoder)


def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})
