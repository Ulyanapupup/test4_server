const minRange = window.minRange;
const maxRange = window.maxRange;
let gameId = null;

document.getElementById('min-range-setup').textContent = minRange;
document.getElementById('max-range-setup').textContent = maxRange;

document.getElementById('start-button').onclick = startGame;

function startGame() {
  const secret = Number(document.getElementById('user-secret').value);
  if (isNaN(secret) || secret < minRange || secret > maxRange) {
    alert(`Введите число от ${minRange} до ${maxRange}`);
    return;
  }

  document.getElementById('secret-number').textContent = `Загаданное число: ${secret}`;

  fetch('/start_game_1_2', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ secret, min_range: minRange, max_range: maxRange })
  })
    .then(res => res.json())
    .then(data => {
      if (data.error) {
        alert(data.error);
        return;
      }
      gameId = data.game_id;
      document.getElementById('setup').style.display = 'none';
      document.getElementById('game').style.display = 'block';
      appendToChat("Компьютер", data.question);
      updateRangeDisplay(data.min, data.max);
    });
}

function processAnswer() {
  const answerInput = document.getElementById('answer');
  const answer = answerInput.value.trim().toLowerCase();

  if (answer !== 'да' && answer !== 'нет') {
    alert('Пожалуйста, введите "да" или "нет"');
    return;
  }

  appendToChat("Вы", answer);
  answerInput.value = '';

  fetch('/answer_1_2', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ game_id: gameId, answer })
  })
    .then(res => res.json())
    .then(data => {
      if (data.error) {
        alert(data.error);
        return;
      }

      appendToChat("Компьютер", data.response);

      if (data.finished && data.number !== undefined) {
        document.getElementById('secret-number').textContent = `Компьютер угадал: ${data.number}`;
        document.getElementById('answer').disabled = true;
      }

      if (data.min !== undefined && data.max !== undefined) {
        updateRangeDisplay(data.min, data.max);
      }
    });
}

function updateRangeDisplay(min, max) {
  document.getElementById('min-range-game').textContent = min;
  document.getElementById('max-range-game').textContent = max;
}

function appendToChat(sender, text) {
  const chat = document.getElementById('chat');
  const div = document.createElement('div');
  div.innerHTML = `<strong>${sender}:</strong> ${text}`;
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
}

function exitGame() {
  window.location.href = '/';
}
