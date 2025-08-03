document.addEventListener("DOMContentLoaded", () => {
  // Ana sayfa yönlendirme
  document.querySelector(".green").addEventListener("click", () => {
    window.location.href = "/main-page";
  });

  // Dinamik doğum yılı (2024 → 1940)
  const birthYearSelect = document.querySelector("select");
  for (let year = 2024; year >= 1940; year--) {
    const option = document.createElement("option");
    option.value = year;
    option.textContent = year;
    birthYearSelect.appendChild(option);
  }

  // Hasta giriş işlemi
  document.querySelectorAll(".submit")[0].addEventListener("click", async () => {
    const email = document.querySelectorAll(".input")[0].value.trim();

    if (!email) return alert("Lütfen hasta mail adresini giriniz.");

    try {
      const res = await fetch(`/patients/check?email=${encodeURIComponent(email)}`);

      if (res.ok) {
        const data = await res.json();
        if (data.exists) {
          localStorage.setItem("patient_email", email);
          window.location.href = "/patient-info-page";
        } else {
          alert("Hasta bulunamadı. Lütfen kayıt olun.");
        }
      } else {
        alert("Bir hata oluştu.");
      }
    } catch (err) {
      console.error(err);
      alert("Girişte bir hata oluştu.");
    }
  });

  // Hasta kayıt işlemi
  document.querySelectorAll(".submit")[1].addEventListener("click", async () => {
    const inputs = document.querySelectorAll(".form-container")[1].querySelectorAll(".input");
    const name = inputs[0].value.trim();
    const surname = inputs[1].value.trim();
    const email = inputs[2].value.trim();
    const birthYear = inputs[3].value;
    const gender = document.querySelector("input[name='gender']:checked")?.value;

    if (!name || !surname || !email || !birthYear || !gender) {
      return alert("Lütfen tüm alanları doldurun.");
    }

    const formData = new URLSearchParams();
    formData.append("first_name", name);
    formData.append("last_name", surname);
    formData.append("email", email);
    formData.append("birth_year", birthYear);
    formData.append("gender", gender);

    try {
      const res = await fetch("/patients/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded"
        },
        body: formData.toString()
      });

      if (res.redirected) {
        localStorage.setItem("patient_email", email);
        window.location.href = res.url;
      } else {
        const error = await res.json();
        alert(error.detail || "Kayıt başarısız.");
      }
    } catch (err) {
      console.error(err);
      alert("Kayıt sırasında bir hata oluştu.");
    }
  });
});
