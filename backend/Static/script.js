const loadHistoryBtn = document.getElementById("loadHistoryBtn");
loadHistoryBtn.addEventListener("click", loadHistory);
const askBtn = document.getElementById("askBtn");
const genBtn = document.getElementById("genBtn");
const input = document.getElementById("question");
const chatBox = document.getElementById("chatBox");
const productInfo = document.getElementById("productInfo");
const descResult = document.getElementById("descResult");


askBtn.addEventListener("click", askAssistant);
genBtn.addEventListener("click", generateDescription);

async function askAssistant() {
    const question = input.value.trim();
    if (question.length < 2) return;

    askBtn.disabled = true;

    chatBox.innerHTML = "";

    const userMsg = document.createElement("div");
    userMsg.className = "chat-msg user";
    userMsg.innerText = "You: " + question;
    chatBox.appendChild(userMsg);

    const assistantMsg = document.createElement("div");
    assistantMsg.className = "chat-msg assistant";
    assistantMsg.innerText = "Assistant: Thinking...";
    chatBox.appendChild(assistantMsg);

    input.value = "";
    chatBox.scrollTop = chatBox.scrollHeight;

    try {
        const response = await fetch(
            "http://127.0.0.1:8000/assistant?question=" +
            encodeURIComponent(question)
        );

        const data = await response.json();
        assistantMsg.innerText = "Assistant: " + data.answer;
    } catch {
        assistantMsg.innerText = "Assistant: Error occurred";
    }

    chatBox.scrollTop = chatBox.scrollHeight;
    askBtn.disabled = false;
}

async function generateDescription() {
    const info = productInfo.value.trim();
    if (info.length < 3) return;

    genBtn.disabled = true;
    descResult.innerText = "Generating...";

    try {
        const response = await fetch(
            "http://127.0.0.1:8000/generate-description?product_info=" +
            encodeURIComponent(info)
        );

        const data = await response.json();
        descResult.innerText = data.generated_text;
    } catch {
        descResult.innerText = "Error occurred";
    }

    genBtn.disabled = false;
}
async function loadHistory() {
    chatBox.innerHTML = "";

    try {
        const response = await fetch("http://127.0.0.1:8000/chat-history");
        const data = await response.json();

        data.history.forEach(item => {
            const q = document.createElement("div");
            q.className = "chat-msg user";
            q.innerText = "You: " + item.question;

            const a = document.createElement("div");
            a.className = "chat-msg assistant";
            a.innerText = "Assistant: " + item.answer;

            chatBox.appendChild(q);
            chatBox.appendChild(a);
        });

        chatBox.scrollTop = chatBox.scrollHeight;
    } catch {
        chatBox.innerText = "Failed to load history";
    }
}
