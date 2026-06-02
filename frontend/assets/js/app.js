function updateChecklistSummary() {
  const total = document.querySelectorAll('[data-symptom="yes"]').length;
  const selected = document.querySelectorAll('[data-symptom="yes"]:checked').length;
  const score = Math.min(0.72, selected * 0.08).toFixed(2);
  const scoreElement = document.querySelector('[data-score]');
  const countElement = document.querySelector('[data-selected-count]');
  const recommendationElement = document.querySelector('[data-recommendation]');

  if (scoreElement) scoreElement.textContent = score;
  if (countElement) countElement.textContent = `${selected} de ${total}`;

  if (recommendationElement) {
    recommendationElement.textContent = Number(score) >= 0.56 ? 'Encaminhar' : 'Nao encaminhar';
    recommendationElement.className = Number(score) >= 0.56 ? 'status warn' : 'status good';
  }

  document.querySelectorAll('.check-group').forEach((group) => {
    const groupSelected = group.querySelectorAll('[data-symptom="yes"]:checked').length;
    const groupCount = group.querySelector('[data-group-count]');

    if (groupCount) {
      groupCount.textContent = `${groupSelected} selecionados`;
    }
  });
}

document.querySelectorAll('[data-symptom]').forEach((input) => {
  input.addEventListener('change', updateChecklistSummary);
});

updateChecklistSummary();
