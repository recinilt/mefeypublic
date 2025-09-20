document.addEventListener("DOMContentLoaded", function () {
    const kaydetButton = document.getElementById("kaydet-button");
    const dateInput = document.getElementById("date-input");
    const entryInput = document.getElementById("entry-input");
    const listeSection = document.getElementById("liste-section");

    kaydetButton.addEventListener("click", function () {
        const tarih = dateInput.value;
        const giris = entryInput.value;

        if (tarih && giris) {
            const yeniGiris = document.createElement("LI");
            yeniGiris.classList.add("girisi");
            yeniGiris.innerHTML = `
                <div class="giriş-tarihi">${tarih}</div>
                <div>${giris}</div>
            `;
            listeSection.appendChild(yeniGiris);

            // Lokal Storage'ye kaydetme
            const girisListesi = JSON.parse(localStorage.getItem("giriler")) || [];
            girisListesi.push({ tarih, giris });
            localStorage.setItem("giriler", JSON.stringify(girisListesi));
        }
    });

    // Lokal Storage'dan okuyma
    const girisListesi = JSON.parse(localStorage.getItem("giriler"));
    if (girisListesi) {
        girisListesi.forEach(function (giris, index) {
            const yeniGiris = document.createElement("LI");
            yeniGiris.classList.add("girisi");
            yeniGiris.innerHTML = `
                <div class="giriş-tarihi">${giris.tarih}</div>
                <div>${giris.giris}</div>
            `;
            listeSection.appendChild(yeniGiris);
        });
    }
});
