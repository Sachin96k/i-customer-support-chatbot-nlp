const form = document.getElementById("chat-form");
const input = document.getElementById("message-input");
const messages = document.getElementById("chat-messages");
const sendButton = document.getElementById("send-button");

function addMessage(text, sender) {
  const wrapper = document.createElement("div");
  wrapper.className = `message ${sender === "user" ? "user-message" : "bot-message"}`;

  const bubble = document.createElement("div");
  bubble.className = "bubble";
  // textContent prevents user or server text from being interpreted as HTML.
  bubble.textContent = text;

  const time = document.createElement("span");
  time.className = "message-time";
  time.textContent = sender === "user" ? "You" : "Assistant";

  wrapper.append(bubble, time);
  messages.appendChild(wrapper);
  messages.scrollTop = messages.scrollHeight;
}

async function sendMessage(text) {
  const message = text.trim();
  if (!message) return;

  addMessage(message, "user");
  input.value = "";
  sendButton.disabled = true;
  sendButton.textContent = "Sending...";

  try {
    const response = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message })
    });
    const data = await response.json();

    if (!response.ok) {
      addMessage(data.error || "Sorry, something went wrong. Please try again.", "bot");
      return;
    }
    addMessage(data.reply || "I couldn't generate a response. Please try again.", "bot");
  } catch (error) {
    addMessage("Unable to connect to the server. Check that the Flask app is running.", "bot");
  } finally {
    sendButton.disabled = false;
    sendButton.textContent = "Send";
    input.focus();
  }
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  sendMessage(input.value);
});

document.querySelectorAll("[data-question]").forEach((button) => {
  button.addEventListener("click", () => sendMessage(button.dataset.question));
});
