document.addEventListener("DOMContentLoaded", async () => {
  const token = localStorage.getItem("access_token");
  if (!token) {
    alert("Giriş yapmanız gerekmektedir.");
    window.location.href = "/main-page";
    return;
  }

  let payload;
  try {
    payload = JSON.parse(atob(token.split(".")[1]));
  } catch (e) {
    alert("Geçersiz oturum bilgisi.");
    return window.location.href = "/main-page";
  }

  const doctorId = payload.user_id;

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

    filteredEntries.forEach((entry) => {
      const patient = entry.patient || {};
      const row = document.createElement("tr");

      row.innerHTML = `
        <td>${entry.entry_date}</td>
        <td>${patient.patient_first_name || "-"}</td>
        <td>${patient.patient_last_name || "-"}</td>
        <td>
          <button class="btn green" onclick="viewEntry(${entry.entry_id})">Görüntüle</button>
        </td>
      `;

      tableBody.appendChild(row);
    });

  } catch (err) {
    console.error(err);
    alert("Hastalar yüklenirken hata oluştu: " + err.message);
  }
});

window.viewEntry = function(entryId) {
  localStorage.setItem("selected_entry_id", entryId);
  window.location.href = "/doctor-page";
};
