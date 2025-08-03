document.addEventListener("DOMContentLoaded", function () {
  const button = document.querySelector(".btn-black");

  button.addEventListener("click", async function () {
    const select = document.querySelector(".select-box");
    const selectedDoctorId = select.value;

    if (!selectedDoctorId || selectedDoctorId === "DOKTOR SEÇİMİ") {
      alert("Lütfen bir doktor seçiniz.");
      return;
    }

    const patientId = localStorage.getItem("patient_id");
    const token = localStorage.getItem("token");

    if (!patientId || !token) {
      alert("Hasta bilgisi veya oturum anahtarı eksik. Lütfen tekrar giriş yapınız.");
      return;
    }

    const entryData = {
      patient_id: parseInt(patientId),
      assigned_doctor_id: parseInt(selectedDoctorId),
      entry_date: new Date().toISOString(),
      entry_arrival_mode: "Yürüyerek",
      entry_injury: "Yok",
      entry_chief_complaint: "Hafif şikayet",
      entry_patient_mental: "Normal",
      entry_patient_pain: "Hafif",
      entry_nrs_pain: "2",
      entry_sbp: "125",
      entry_dbp: "80",
      entry_hr: "85",
      entry_rr: "18",
      entry_bt: "36.5"
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
        const errorText = await response.text();
        alert("Yönlendirme başarısız oldu:\n" + errorText);
      }
    } catch (err) {
      console.error("Sunucu hatası:", err);
      alert("Sunucuya bağlanılamadı.");
    }
  });
});
