// Инициализация карты
ymaps.ready(function () {
    var map = new ymaps.Map('map', {
        center: [55.751574, 37.573856], // Москва по умолчанию
        zoom: 10
    });

    // Обработка клика по карте
    map.events.add('click', function (e) {
        var coords = e.get('coords');
        document.getElementById('latitude').value = coords[0];
        document.getElementById('longitude').value = coords[1];
        var modal = new bootstrap.Modal(document.getElementById('emotionModal'));
        modal.show();
    });

    // Загрузка и отображение маркеров
    fetch('/get_markers')
        .then(response => response.json())
        .then(markers => {
            markers.forEach(marker => {
                const placemark = new ymaps.Placemark([
                    marker.latitude, marker.longitude
                ], {
                    balloonContentHeader: marker.title,
                    balloonContentBody: `<b>Эмоция:</b> ${emotionToRussian(marker.emotion)}<br><b>Описание:</b> ${marker.description}<br><b>Дата:</b> ${marker.date}`
                }, {
                    preset: 'islands#icon',
                    iconColor: getEmotionColor(marker.emotion)
                });
                map.geoObjects.add(placemark);
            });
        });
});

// Выбор эмоции
let selectedEmotion = null;
document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.emotion-btn').forEach(function (btn) {
        btn.addEventListener('click', function () {
            document.querySelectorAll('.emotion-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            selectedEmotion = btn.getAttribute('data-emotion');
        });
    });

    // Отправка формы
    document.getElementById('emotionForm').addEventListener('submit', function (e) {
        e.preventDefault();
        if (!selectedEmotion) {
            alert('Пожалуйста, выберите эмоцию!');
            return;
        }
        const data = {
            emotion: selectedEmotion,
            title: document.getElementById('title').value,
            description: document.getElementById('description').value,
            date: document.getElementById('date').value,
            latitude: document.getElementById('latitude').value,
            longitude: document.getElementById('longitude').value
        };
        fetch('/save_marker', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(result => {
            if (result.success) {
                location.reload();
            } else {
                alert('Ошибка при сохранении!');
            }
        });
    });
});

// Функция для выбора цвета по эмоции
function getEmotionColor(emotion) {
    switch (emotion) {
        case 'Joy': return '#ffb3b3';
        case 'Sadness': return '#a3c2f7';
        case 'Anger': return '#ffe066';
        case 'Love': return '#b3ffd9';
        case 'Fear': return '#d1b3ff';
        case 'Excitement': return '#ffd1ec';
        case 'Peace': return '#b3e6ff';
        case 'Neutral;': return '#cccccc';
        default: return '#888888';
    }
}

// Инициализация карты истории точек при активации вкладки
let historyMapInitialized = false;
document.addEventListener('DOMContentLoaded', function () {
    const historyTab = document.getElementById('history-tab');
    if (historyTab) {
        historyTab.addEventListener('shown.bs.tab', function () {
            if (!historyMapInitialized) {
                ymaps.ready(function () {
                    var historyMap = new ymaps.Map('history-map', {
                        center: [55.751574, 37.573856],
                        zoom: 10
                    });
                    fetch('/get_markers')
                        .then(response => response.json())
                        .then(markers => {
                            markers.forEach(marker => {
                                const placemark = new ymaps.Placemark([
                                    marker.latitude, marker.longitude
                                ], {
                                    balloonContentHeader: marker.title,
                                    balloonContentBody: `<b>Эмоция:</b> ${emotionToRussian(marker.emotion)}<br><b>Описание:</b> ${marker.description}<br><b>Дата:</b> ${marker.date}`
                                }, {
                                    preset: 'islands#icon',
                                    iconColor: getEmotionColor(marker.emotion)
                                });
                                historyMap.geoObjects.add(placemark);
                            });
                            // Заполнение таблицы
                            fillMarkersTable(markers);
                        });
                });
                historyMapInitialized = true;
            }
        });
    }
});

// Функция для заполнения таблицы точек
function fillMarkersTable(markers) {
    const tbody = document.querySelector('#markers-table tbody');
    tbody.innerHTML = '';
    markers.forEach(marker => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${getEmotionIcon(emotionToRussian(marker.emotion))} ${emotionToRussian(marker.emotion)}</td>
            <td>${marker.title}</td>
            <td>${marker.description}</td>
            <td>${marker.date}</td>
            <td>${marker.latitude}</td>
            <td>${marker.longitude}</td>
        `;
        tbody.appendChild(row);
    });
}

// Функция для иконки эмоции
function getEmotionIcon(emotion) {
    switch (emotion) {
        case 'Радость': return '😊';
        case 'Грусть': return '😢';
        case 'Злость': return '😠';
        case 'Любовь': return '💚';
        case 'Страх': return '😨';
        case 'Восхищение': return '🤩';
        case 'Спокойствие': return '☮️';
        case 'Нейтрально': return '😐';
        default: return '';
    }
}

// Функция для перевода эмоции на русский
function emotionToRussian(emotion) {
    switch (emotion) {
        case 'Joy': return 'Радость';
        case 'Sadness': return 'Грусть';
        case 'Anger': return 'Злость';
        case 'Love': return 'Любовь';
        case 'Fear': return 'Страх';
        case 'Excitement': return 'Восхищение';
        case 'Peace': return 'Спокойствие';
        case 'Neutral': return 'Нейтрально';
        default: return emotion;
    }
} 