const SVG_NS = "http://www.w3.org/2000/svg";
const PADDING = 30;
const SCALE = 50;

function toSvg(x, y) {
    return { sx: PADDING + x * SCALE, sy: 300 - PADDING - y * SCALE };
}

let allPositions = [];

async function loadPositions() {
    const response = await fetch("/positions");
    const data = await response.json();
    allPositions = data.positions;
}

function drawBackground(svg) {
    svg.innerHTML = "";
    for (const p of allPositions) {
        const { sx, sy } = toSvg(p.x, p.y);
        const dot = document.createElementNS(SVG_NS, "circle");
        dot.setAttribute("cx", sx);
        dot.setAttribute("cy", sy);
        dot.setAttribute("r", 4);
        dot.setAttribute("fill", "#ccc");
        svg.appendChild(dot);
    }
}

function drawAnswer(svg, x, y) {
    drawBackground(svg);
    if (x === null || y === null) return;
    const { sx, sy } = toSvg(x, y);
    const dot = document.createElementNS(SVG_NS, "circle");
    dot.setAttribute("cx", sx);
    dot.setAttribute("cy", sy);
    dot.setAttribute("r", 9);
    dot.setAttribute("fill", "tomato");
    svg.appendChild(dot);
}

async function ask() {
    const text = document.getElementById("question").value;
    const query = "?text=" + encodeURIComponent(text);

    const [withoutResponse, withResponse] = await Promise.all([
        fetch("/ask_without" + query),
        fetch("/ask_with" + query),
    ]);

    const withoutText = await withoutResponse.json();
    const withData = await withResponse.json();

    document.getElementById("answer-without").textContent = withoutText;

    const plot = document.getElementById("plot-with");
    const answerWith = document.getElementById("answer-with");

    if (typeof withData === "object" && withData !== null) {
        answerWith.textContent = "";
        answerWith.hidden = true;
        plot.hidden = false;
        drawAnswer(plot, withData.x, withData.y);
    } else {
        plot.hidden = true;
        answerWith.hidden = false;
        answerWith.textContent = withData;
    }
}

document.getElementById("ask-button").addEventListener("click", ask);

loadPositions();
