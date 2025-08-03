document.addEventListener("DOMContentLoaded", async () => {
  const token = localStorage.getItem("access_token");
  const entryId = localStorage.getItem("selected_entry_id");

  if (!token || !entryId) {
    alert("Giriş veya hasta seçimi eksik. Lütfen tekrar deneyin.");
    window.location.href = "/main-page";
    return;
  }

  try {
    const response = await fetch(`/entry/get_entry/${entryId}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (!response.ok) throw new Error("Hasta verisi alınamadı.");
    const entry = await response.json();
    const patient = entry.patient || {};

    // Temel bilgiler
    document.getElementById("hastaAdi").value = patient.patient_first_name || "-";
    document.getElementById("hastaSoyadi").value = patient.patient_last_name || "-";
    document.getElementById("cinsiyet").value = patient.patient_gender || "-";
    document.getElementById("yas").value =
      new Date().getFullYear() - parseInt(patient.patient_birth_date);

    // Klinik bilgiler
    document.getElementById("ktasRn").value = entry.ktas_rn;
    document.getElementById("mistriage").value = entry.mistriage;
    document.getElementById("errorGroup").value = entry.error_group;
    document.getElementById("nrsPain").value = entry.nrs_pain;
    document.getElementById("stayMin").value = entry.length_of_stay_min;
    document.getElementById("disposition").value = entry.disposition;
    document.getElementById("hr").value = entry.hr;
    document.getElementById("sbp").value = entry.sbp;
    document.getElementById("bt").value = entry.bt;
    document.getElementById("ktasDuration").value = entry.ktas_duration_min;
    document.getElementById("mental").value = entry.mental;
    document.getElementById("injury").value = entry.injury;

    // AI değerlendirmesi
    const aciliyet = entry.ktas_rn <= 2 ? "Kritik Hasta" : entry.ktas_rn == 3 ? "Orta Şiddette Hasta" : "Düşük Riskli Hasta";
    document.getElementById("aiDegerlendirme").innerText = `KTAS: ${entry.ktas_rn}, AI Tahmini: ${aciliyet}`;

  } catch (err) {
    console.error(err);
    alert("Hasta bilgileri yüklenemedi.");
  }
});