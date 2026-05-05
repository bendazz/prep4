async function loadCategories() {
    const response = await fetch("/categories");
    const data = await response.json();

    const list = document.getElementById("categories");
    for (const category of data.categories) {
        const item = document.createElement("li");
        item.textContent = category;
        list.appendChild(item);
    }
}

async function classifyText() {
    const text = document.getElementById("text-input").value;
    const resultSpan = document.getElementById("result");

    resultSpan.textContent = "Classifying...";

    const response = await fetch("/classify?text=" + encodeURIComponent(text));
    const result = await response.json();

    resultSpan.textContent = result;
}

document.getElementById("classify-button").addEventListener("click", classifyText);

loadCategories();
