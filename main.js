const input = document.getElementById('q');
const box = document.getElementById('autocomplete-box');

if (input && box) {
    input.addEventListener('input', async () => {
        const val = input.value.trim();
        if (!val) { box.innerHTML = ''; return; }
        try {
            const res = await fetch(`/autocomplete?q=${encodeURIComponent(val)}`);
            const data = await res.json();
            box.innerHTML = data.slice(0, 6).map(item => 
                `<div class="autocomplete-item" onclick="selectSuggestion('${item}')">${item}</div>`
            ).join('');
        } catch (e) {
            box.innerHTML = '';
        }
    });
}

function selectSuggestion(text) {
    input.value = text;
    box.innerHTML = '';
    input.form.submit();
}