document.addEventListener("DOMContentLoaded", () => {
  // Ana sayfa yönlendirme
  document.querySelector(".green").addEventListener("click", () => {
    window.location.href = "/main-page";
  });

  // Doğum yılı listesini dinamik oluştur (örn. 2025 → 1940)
  const birthYearSelect = document.querySelector("select");
  const currentYear = new Date().getFullYear();
  for (let year = currentYear; year >= 1940; year--) {
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
      const res = await fetch(
        `/patients/check?email=${encodeURIComponent(email)}`
      );
      if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);

      const data = await res.json();
      if (data.exists) {
        localStorage.setItem("patient_email", email);
        window.location.href = "/patient-info-page";
      } else {
        alert("Hasta bulunamadı. Lütfen kayıt olun.");
      }
    } catch (err) {
      console.error(err);
      alert("Girişte bir hata oluştu.");
    }
  });

  // Hasta kayıt işlemi
  document.querySelectorAll(".submit")[1].addEventListener("click", async () => {
    const inputs = document
      .querySelectorAll(".form-container")[1]
      .querySelectorAll(".input");
    const [nameInput, surnameInput, emailInput] = inputs;
    const name = nameInput.value.trim();
    const surname = surnameInput.value.trim();
    const email = emailInput.value.trim();
    const birthYear = birthYearSelect.value;
    const gender = document.querySelector(
      "input[name='gender']:checked"
    )?.value;

    if (!name || !surname || !email || !birthYear || !gender) {
      return alert("Lütfen tüm alanları doldurun.");
    }

    const formData = new URLSearchParams({
      first_name: name,
      last_name: surname,
      email,
      birth_year: birthYear,
      gender,
    });

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