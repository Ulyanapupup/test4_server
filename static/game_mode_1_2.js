const minRange = {{ min_range }};
const maxRange = {{ max_range }};
let gameId = null;

document.getElementById('min-range-setup').textContent = minRange;
document.getElementById('max-range-setup').textContent = maxRange;

function startGame() {
const secret = Number(document.getElementById('user-secret').value);
if (isNaN(secret) || secret < minRange || secret > maxRange) {
  alert(`Введите число от ${minRange} до ${maxRange}`);
  return;
}

fetch('/start_game_1_2', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({secret, min_range: minRange, max_range: maxRange})
})
.then(res => res.json())
.then(data => {
  gameId = data.game_id;
  document.getElementById('setup').style.display = 'none';
  document.getElementById('game').style.display = 'block';
  addMessage("Компьютер: " + data.question);
  updateRangeDisplay(minRange, maxRange);
});
}

function addMessage(text) {
const chat = document.getElementById('chat');
const p = document.createElement('p');
p.textContent = text;
chat.appendChild(p);
chat.scrollTop = chat.scrollHeight;
}

function processAnswer() {
const answer = document.getElementById('answer').value.trim().toLowerCase();
if (answer !== 'да' && answer !== 'нет') {
  alert('Пожалуйста, ответьте "да" или "нет"');
  return;
}
fetch('/answer_1_2', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({game_id: gameId, answer})
})
.then(res => res.json())
.then(data => {
  if (data.error) {
	alert(data.error);
	return;
  }
  addMessage("Вы: " + answer);
  addMessage("Компьютер: " + data.response);
  document.getElementById('answer').value = '';

  // Обновим диапазон отображения, если возможно
  // (для упрощения обновляем его из объекта игры на сервере)
  // Можно в ответе сервером добавить min и max, если надо
});
}

function updateRangeDisplay(min, max) {
document.getElementById('min-range-game').textContent = min;
document.getElementById('max-range-game').textContent = max;
}

function exitGame() {
window.location.href = '/select_range_1_2';
}

document.getElementById('start-button').onclick = startGame;