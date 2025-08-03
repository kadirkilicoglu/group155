document.addEventListener("DOMContentLoaded", async () => {
  const token = localStorage.getItem("access_token");
  if (!token) {
    alert("Giriş yapmanız gerekmektedir.");
    window.location.href = "/main-page.html";
    return;
  }

  const payload = JSON.parse(atob(token.split(".")[1]));
  const doctorId = payload.user_id;

  // Doktorun adını sayfaya yaz
  document.getElementById("doctor-firstname").value = payload.user_first_name;
  document.getElementById("doctor-lastname").value = payload.user_last_name;

  try {
    const response = await fetch("/entry/get_entries", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (!response.ok) throw new Error("Veriler alınamadı.");

    const entries = await response.json();

    const filteredEntries = entries.filter(
      (entry) => entry.entry_assigned_doctor_id === doctorId
    );

    const tableBody = document.getElementById("patient-table-body");
    tableBody.innerHTML = "";

    for (const entry of filteredEntries) {
      const patient = entry.patient || {}; // Eğer backend'de ilişkili hasta gelmiyorsa, önlem
      const row = document.createElement("tr");

      row.innerHTML = `
        <td>${entry.entry_date}</td>
        <td>${patient.patient_first_name || "-"}</td>
        <td>${patient.patient_last_name || "-"}</td>
        <td><button class="btn green" onclick="alert('Detay sayfası eklenmeli')">Görüntüle</button></td>
      `;

      tableBody.appendChild(row);
    }
  } catch (err) {
    alert("Hastalar yüklenirken hata oluştu: " + err.message);
  }
});
