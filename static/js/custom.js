let selectedCategoryId;

        function showSentences(categoryId) {

    selectedCategoryId = categoryId;


    fetch(`/${categoryId}/`)
        .then(response => response.json())
        .then(data => {

            const sentenceList = document.getElementById('sentence-list');
            sentenceList.innerHTML = '';

            data.user_inputs.forEach(userInput => {
                const sentenceCard = document.createElement('div');
                sentenceCard.classList.add('sentence-card');
                const sentimentBox = document.createElement('div');
                sentimentBox.classList.add('sentiment-box');
                sentimentBox.style.backgroundColor = getSentimentColor(userInput.sentiment_label);
                const textContent = document.createElement('div');
                textContent.textContent = `Text Content: ${userInput.sentence}`;

                const sentimentResult = document.createElement('div');
                sentimentResult.textContent = `Sentiment Result: ${userInput.sentiment_label}`;

                sentenceCard.appendChild(textContent);
                sentenceCard.appendChild(sentimentResult);
                sentenceCard.appendChild(sentimentBox);

                sentenceList.appendChild(sentenceCard);
            });

        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
}


function createNewSentence() {
            const newSentenceInput = document.getElementById('newSentence');
            const newSentence = newSentenceInput.value;
                const submitButton = document.getElementById('submitButton');

            const csrftoken = getCookie('csrftoken');
                submitButton.disabled = true;


                const loadingSpinner = document.getElementById('loadingSpinner');
                loadingSpinner.style.display = 'block';
            fetch(`/add_sentence/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                },
                body: JSON.stringify({ newSentence: newSentence }),
            })
                .then(response => response.json())
                .then(data => {
                    console.log('New sentence created:', data);
                                loadingSpinner.style.display = 'none';
                                        submitButton.disabled = false;

                                         if (data['success']) {

            document.getElementById('successMessage').innerText = data.msg;
            $('#successModal').modal('show');

            showSentences(selectedCategoryId ?? 1);
        } else {
            document.getElementById('errorMessage').innerText = data.msg;
            $('#errorModal').modal('show');
        }


                                 showSentences(data['category_id']);


                })
                .catch(error => {
                    console.error('Error creating new sentence:', error);
                                loadingSpinner.style.display = 'none';
                                        submitButton.disabled = false;


                });

            newSentenceInput.value = '';
        }

        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = cookies[i].trim();
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

        function getSentimentColor(sentiment) {
    switch (sentiment.toLowerCase()) {
        case 'positive':
            return 'green';
        case 'negative':
            return 'red';
        case 'neutral':
            return '#cccccc';
        default:
            return '#cccccc';
    }
}

