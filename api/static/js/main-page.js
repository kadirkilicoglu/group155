document.addEventListener("DOMContentLoaded", () => {
  const loginForm = document.querySelector(".login-form");

  loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const email = loginForm.querySelector("input[type='email']").value;
    const password = loginForm.querySelector("input[type='password']").value;

    try {
      const response = await fetch("/authentication/token", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: new URLSearchParams({
          username: email,
          password: password,
        }),
      });

      if (!response.ok) {
        // More specific error handling based on status if needed, or a generic message
        if (response.status === 401) {
          throw new Error("Geçersiz e-posta veya şifre.");
        } else {
          throw new Error("Giriş başarısız. Lütfen tekrar deneyin.");
        }
      }

      const data = await response.json();
      const token = data.access_token;

      // JWT token içeriğini çöz (base64 decode)
      const payload = JSON.parse(atob(token.split(".")[1]));

      console.log("Decoded JWT Payload:", payload);

      const roleId = payload.user_role.role_id;

      console.log("User Role ID:", roleId);

      // Rol bazlı yönlendirme
if (roleId === 1) {
  window.location.href = "/authentication/admin-page"; // Admin sayfası
} else if (roleId === 3) {
  window.location.href = "/doctor-page"; // Doktor sayfası
} else if (roleId === 2) {
  window.location.href = "/patient-page"; // Personel sayfası (örneğin hemşireler)
} else {
  alert("Yetkisiz rol türü.");
}
    } catch (error) {
      alert(error.message); // Display the specific error message
    }
  });
});