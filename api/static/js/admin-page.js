document.addEventListener("DOMContentLoaded", () => {
  const token = localStorage.getItem("token"); // sadece bu satır değiştirildi

  if (!token) {
    alert("Giriş yapmanız gerekiyor.");
    window.location.href = "/";
    return;
  }

  // Ana Sayfa butonu tıklama olayı
  const homeBtn = document.querySelector(".header-buttons .btn.green");
  if (homeBtn) {
    homeBtn.addEventListener("click", () => {
      window.location.href = "http://127.0.0.1:8000";
    });
  }

  const addForm = document.querySelector(".form-add");
  const deleteForm = document.querySelector(".form-delete");

  // Kullanıcı ekleme
  addForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = addForm.querySelector('input[type="email"]').value.trim();
    const password = addForm.querySelector('input[type="password"]').value.trim();
    const roleText = addForm.querySelector("select").value;

    const roleMap = {
      personel: 2,
      doktor: 3
    };

    const role = roleMap[roleText.toLowerCase()];
    if (!role) {
      alert("Geçerli bir rol seçiniz.");
      return;
    }

    const userData = {
      username: email,
      password: password,
      first_name: "Ad",
      last_name: "Soyad",
      role: role
    };

    try {
      const response = await fetch("/admin/create_user", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify(userData)
      });

      if (response.ok) {
        alert("Kullanıcı başarıyla eklendi.");
        addForm.reset();
      } else {
        const err = await response.json();
        alert("Hata: " + (err.detail || "Kullanıcı eklenemedi."));
      }
    } catch (error) {
      console.error("Ekleme hatası:", error);
      alert("Bir hata oluştu.");
    }
  });

  // Kullanıcı silme
  deleteForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const emailToDelete = deleteForm.querySelector('input[type="email"]').value.trim();

    try {
      const res = await fetch("/admin/get_users", {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`
        }
      });

      if (!res.ok) {
        alert("Kullanıcı listesi alınamadı.");
        return;
      }

      const users = await res.json();
      const user = users.find(u => u.user_email === emailToDelete);

      if (!user) {
        alert("Bu e-posta ile eşleşen kullanıcı bulunamadı.");
        return;
      }

      const deleteRes = await fetch(`/admin/delete_user/${user.user_id}`, {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${token}`
        }
      });

      if (deleteRes.ok) {
        alert("Kullanıcı başarıyla silindi.");
        deleteForm.reset();
      } else {
        alert("Silme işlemi başarısız.");
      }
    } catch (error) {
      console.error("Silme hatası:", error);
      alert("Bir hata oluştu.");
    }
  });
});
