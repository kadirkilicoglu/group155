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
      alert("Giriş bilgileri eksik.");
      return;
    }

    const entryData = {
      patient_id: parseInt(patientId),
      assigned_doctor_id: parseInt(selectedDoctorId),
      entry_date: new Date().toISOString(),
      entry_arrival_mode: "Kendi İmkânıyla",
      entry_injury: "Orta Düzey",
      entry_chief_complaint: "Ağrı",
      entry_patient_mental: "Sersem",
      entry_patient_pain: "Orta",
      entry_nrs_pain: "6",
      entry_sbp: "110",
      entry_dbp: "70",
      entry_hr: "100",
      entry_rr: "24",
      entry_bt: "37.5"
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
      alert("Sunucu hatası.");
    }
  });
});
