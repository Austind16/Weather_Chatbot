const themeToggle = document.getElementById("themeToggle");

if (themeToggle) {
    if (localStorage.getItem("theme") === "dark") {
        document.body.classList.add("dark");
        themeToggle.textContent = "☀️ Light";
    }

    themeToggle.addEventListener("click", () => {
        document.body.classList.toggle("dark");

        if (document.body.classList.contains("dark")) {
            themeToggle.textContent = "☀️ Light";
            localStorage.setItem("theme", "dark");
        } else {
            themeToggle.textContent = "🌙 Dark";
            localStorage.setItem("theme", "light");
        }
    });
}

const chatBox = document.querySelector(".chat-box");

if (chatBox) {
    chatBox.scrollTop = chatBox.scrollHeight;
}