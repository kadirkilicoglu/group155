document.addEventListener("DOMContentLoaded", async () => {
  // Ana sayfa butonu
  document.querySelector(".green").onclick = () => window.location.href = "/main-page";

  // LocalStorage'dan e-posta al
  const email = localStorage.getItem("patient_email");
  if (!email) {
    alert("Hasta bilgisi bulunamadı.");
    return window.location.href = "/patient-page";
  }

  try {
    const res = await fetch(
      `/patients/get_by_email?email=${encodeURIComponent(email)}`
    );
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const patient = await res.json();

    // Input alanlarını placeholder ile seç
    const nameInput = document.querySelector('input[placeholder="İsim"]');
    const genderInput = document.querySelector('input[placeholder="Cinsiyet"]');
    const dateInput = document.querySelector('input[placeholder="gg/AA/yyyy"]');

    const surnameInput = document.querySelector('input[placeholder="Soyisim"]');
    const mailInput = document.querySelector('input[placeholder="Hasta Mail"]');
    const ageInput = document.querySelector('input[placeholder="Yaş"]');

    // Değerleri ata
    nameInput.value = patient.first_name;
    surnameInput.value = patient.last_name;
    genderInput.value = patient.gender;
    mailInput.value = patient.email;

    // Yaş hesaplama
    const birthYear = parseInt(patient.birth_year, 10);
    ageInput.value = new Date().getFullYear() - birthYear;

    // Bugünün tarihini ata
    const today = new Date();
    const dd = String(today.getDate()).padStart(2, '0');
    const mm = String(today.getMonth() + 1).padStart(2, '0');
    const yyyy = today.getFullYear();
    dateInput.value = `${dd}/${mm}/${yyyy}`;

  } catch (err) {
    console.error(err);
    alert("Hasta bilgileri alınırken bir hata oluştu.");
  }
});