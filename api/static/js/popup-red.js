document.addEventListener("DOMContentLoaded", function () {
  const button = document.querySelector(".btn-black");

  button.addEventListener("click", async function () {
    const selectedDoctorId = document.querySelector(".select-box").value;

    if (!selectedDoctorId || selectedDoctorId === "DOKTOR SEÇİMİ") {
      alert("Lütfen bir doktor seçiniz.");
      return;
    }

    const patientId = localStorage.getItem("patient_id");
    const token = localStorage.getItem("token");

    if (!patientId || !token) {
      alert("Giriş bilgileri eksik. Lütfen tekrar giriş yapın.");
      return;
    }

    const entryData = {
      patient_id: parseInt(patientId),
      assigned_doctor_id: parseInt(selectedDoctorId),
      entry_date: new Date().toISOString(),
      entry_arrival_mode: "Ambulans",
      entry_injury: "Travma",
      entry_chief_complaint: "Acil - Şiddetli Durum",
      entry_patient_mental: "Bilinçsiz",
      entry_patient_pain: "Şiddetli",
      entry_nrs_pain: "9",
      entry_sbp: "90",
      entry_dbp: "60",
      entry_hr: "120",
      entry_rr: "30",
      entry_bt: "39.0"
    };

    try {
      const response = await fetch("/entry/create_entry", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    Authorization: "Bearer " + token
  },
  body: JSON.stringify(entryData)
});


      if (response.ok) {
        alert("Hasta başarıyla yönlendirildi.");
        window.location.href = "/main-page";
      } else {
        const error = await response.text();
        alert("Yönlendirme başarısız:\n" + error);
      }
    } catch (err) {
      console.error("Hata:", err);
      alert("Sunucuya erişilemedi.");
    }
  });
});
