async function askWithout() {
    const text = document.getElementById("question-without").value;
    const answerSpan = document.getElementById("answer-without");

    answerSpan.textContent = "Thinking...";

    const response = await fetch("/ask_without?text=" + encodeURIComponent(text));
    const result = await response.json();

    answerSpan.textContent = result;
}

async function askWith() {
    const text = document.getElementById("question-with").value;
    const answerSpan = document.getElementById("answer-with");

    answerSpan.textContent = "Thinking...";

    const response = await fetch("/ask_with?text=" + encodeURIComponent(text));
    const result = await response.json();

    answerSpan.textContent = JSON.stringify(result, null, 2);
}

document.getElementById("ask-without-button").addEventListener("click", askWithout);
document.getElementById("ask-with-button").addEventListener("click", askWith);
