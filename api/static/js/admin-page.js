document.addEventListener("DOMContentLoaded", () => {
  const addForm = document.querySelector(".form-add");
  const deleteForm = document.querySelector(".form-delete");

  // Sadece nurse ve doctor rolleri için ID eşlemeleri
  const roleMap = {
    personel: 2,  // hemşire rolünün ID'si
    doktor: 3     // doktor rolünün ID'si
  };


  // Personel Ekleme Formu
  addForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(addForm);
    const roleValue = formData.get("role");

    if (!roleMap[roleValue]) {
      alert("Geçerli bir rol seçiniz.");
      return;
    }

    const payload = {
      username: formData.get("username"),
      password: formData.get("password"),
      first_name: formData.get("first_name"),
      last_name: formData.get("last_name"),
      role: roleMap[roleValue]
    };

    try {
      const token = localStorage.getItem("access_token");

      const response = await fetch("/admin/create_user", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...(token ? { "Authorization": `Bearer ${token}` } : {})
        },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        const errorData = await response.json();
        alert("Hata: " + (errorData.detail || "Kullanıcı oluşturulamadı"));
        return;
      }

      alert("Personel başarıyla eklendi.");
      addForm.reset();

    } catch (error) {
      alert("Sunucu hatası: " + error.message);
    }
  });

  // Personel Silme Formu
  deleteForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const emailInput = deleteForm.querySelector("input[type=email]");
    const email = emailInput.value.trim();

    if (!email) {
      alert("Lütfen mail adresini girin.");
      return;
    }

    try {
      const token = localStorage.getItem("access_token");

      const usersRes = await fetch("/admin/get_users", {
        headers: {
          ...(token ? { "Authorization": `Bearer ${token}` } : {})
        }
      });
      if (!usersRes.ok) throw new Error("Kullanıcı listesi alınamadı");
      const users = await usersRes.json();

      const userToDelete = users.find(u => u.user_email.toLowerCase() === email.toLowerCase());
      if (!userToDelete) {
        alert("Kullanıcı bulunamadı.");
        return;
      }

      const deleteRes = await fetch(`/admin/delete_user/${userToDelete.user_id}`, {
        method: "DELETE",
        headers: {
          ...(token ? { "Authorization": `Bearer ${token}` } : {})
        }
      });

      if (!deleteRes.ok) {
        const errorData = await deleteRes.json();
        alert("Silme işlemi başarısız: " + (errorData.detail || ""));
        return;
      }

      alert("Personel başarıyla silindi.");
      emailInput.value = "";

    } catch (error) {
      alert("Sunucu hatası: " + error.message);
    }
  });
});
