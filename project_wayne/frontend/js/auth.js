document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("loginForm");
  const msg = document.getElementById("mensagem");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();

    try {
      const resp = await fetch("http://localhost:5000/api/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
      });

      const data = await resp.json();

      if (resp.ok && data.token) {
        localStorage.setItem("token", data.token);
        msg.textContent = "✅ Login bem-sucedido!";
        msg.style.color = "lime";
        setTimeout(() => (window.location.href = "dashboard.html"), 1000);
      } else {
        msg.textContent = data.erro || "Credenciais inválidas!";
        msg.style.color = "red";
      }
    } catch (error) {
      console.error(error);
      msg.textContent = "Erro ao conectar com o servidor.";
      msg.style.color = "red";
    }
  });
});
