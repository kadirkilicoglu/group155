document.addEventListener("DOMContentLoaded", async () => {  
    document.querySelector(".green").onclick = () => window.location.href = "/main-page";

  // Hasta e-posta kontrolü
  const email = localStorage.getItem("patient_email");
  if (!email) {
    alert("Hasta bilgisi bulunamadı.");
    return window.location.href = "/patient-page";
  }

  try {
    // Hasta bilgilerini getir
    const res = await fetch(`/patients/get_by_email?email=${encodeURIComponent(email)}`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const patient = await res.json();

    localStorage.setItem("patient_id", patient.patient_id);

    document.querySelector('input[placeholder="İsim"]').value = patient.first_name;
    document.querySelector('input[placeholder="Soyisim"]').value = patient.last_name;
    document.querySelector('input[placeholder="Cinsiyet"]').value = patient.gender;
    document.querySelector('input[placeholder="Hasta Mail"]').value = patient.email;

    const birthYear = parseInt(patient.birth_year, 10);
    const age = new Date().getFullYear() - birthYear;
    document.querySelector('input[placeholder="Yaş"]').value = age;
    localStorage.setItem("age", age); 

    const today = new Date();
    const dd = String(today.getDate()).padStart(2, '0');
    const mm = String(today.getMonth() + 1).padStart(2, '0');
    const yyyy = today.getFullYear();
    document.querySelector('input[placeholder="gg/AA/yyyy"]').value = `${dd}/${mm}/${yyyy}`;

    // Kaydet butonu ve yönlendirme
    document.querySelector(".patient-form").addEventListener("submit", async (e) => {
      e.preventDefault();

      const get = (name) => document.querySelector(`[name="${name}"]`).value;

      const predictionData = {
        ktas_rn: parseFloat(get("ktas_rn")),
        mistriage: parseFloat(get("mistriage")),
        error_group: parseFloat(get("error_group")),
        nrs_pain: parseFloat(get("nrs_pain")),
        length_of_stay_min: parseFloat(get("length_of_stay_min")),
        age: parseFloat(get("age")),
        disposition: parseFloat(get("disposition")),
        hr: parseFloat(get("hr")),
        sbp: parseFloat(get("sbp")),
        bt: parseFloat(get("bt")),
        ktas_duration_min: parseFloat(get("ktas_duration_min")),
        mental: parseFloat(get("mental")),
        injury: parseFloat(get("injury"))
      };

      try {
        const response = await fetch("/prediction/get_emergency_color_prediction_without_auth", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(predictionData)
        });

        const result = await response.json();
        const color = result.prediction.toLowerCase();

        // Yönlendirme
        if (color === "green") {
          window.location.href = "/popup-green";
        } else if (color === "red") {
          window.location.href = "/popup-red";
        } else if (color === "yellow") {
          window.location.href = "/popup-yellow";
        } else {
          alert("Model bir tahmin yapamadı.");
        }

      } catch (error) {
        console.error("Tahmin hatası:", error);
        alert("Model tahmini alınamadı.");
      }
    });

  } catch (err) {
    console.error("Hasta bilgileri getirilemedi:", err);
    alert("Hasta bilgileri alınırken hata oluştu.");
  }
});
