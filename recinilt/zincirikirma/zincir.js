// Sayfa yüklendiğinde localStorage'den verileri yükle
window.onload = function() {
    loadHabits();
    createTargetInputs();
  };
  
  // Hedef inputlarını dinamik olarak oluştur
  function createTargetInputs() {
    const targetsDiv = document.getElementById("targets");
    targetsDiv.innerHTML = ""; // Önceki inputları temizle
  
    for (let i = 1; i <= 13; i++) {
      const targetLabel = document.createElement("label");
      targetLabel.textContent = i + ". 28 Günlük Hedef:";
      const targetInput = document.createElement("input");
      targetInput.type = "text";
      targetInput.id = "target" + i;
      targetInput.name = "target" + i;
  
      targetsDiv.appendChild(targetLabel);
      targetsDiv.appendChild(targetInput);
      targetsDiv.appendChild(document.createElement("br"));
    }
  }
  
  // İlk hedefi diğer hedef inputlarına kopyala
  document.getElementById("initialGoal").addEventListener("input", function() {
    const initialGoal = this.value;
    for (let i = 1; i <= 13; i++) {
      document.getElementById("target" + i).value = initialGoal;
    }
  });
  
  // Yeni alışkanlık formu gönderildiğinde
  document.getElementById("habitForm").addEventListener("submit", function(event) {
    event.preventDefault();
  
    const habitName = document.getElementById("habitName").value;
    const initialGoal = document.getElementById("initialGoal").value;
    const targets = [];
    for (let i = 1; i <= 13; i++) {
      targets.push(document.getElementById("target" + i).value);
    }
  
    saveHabit(habitName, initialGoal, targets);
  
    this.reset();
    // Formu gizlemek için gerekli kodları buraya ekleyin (örneğin, form.style.display = "none";)
  
    loadHabits();
  });
  
  // Alışkanlıkları localStorage'e kaydet
  function saveHabit(habitName, initialGoal, targets) {
    let habits = JSON.parse(localStorage.getItem("habits")) || {};
    habits[habitName] = { initialGoal: initialGoal, targets: targets, days: {} };
    localStorage.setItem("habits", JSON.stringify(habits));
  }
  
  // Alışkanlıkları localStorage'den yükle
  function loadHabits() {
    const habitList = document.getElementById("habitList");
    habitList.innerHTML = "";
  
    const habits = JSON.parse(localStorage.getItem("habits")) || {};
    for (const habitName in habits) {
      const habitItem = document.createElement("li");
      habitItem.textContent = habitName;
  
      // Silme butonu ekle
      const deleteButton = document.createElement("button");
      deleteButton.textContent = "X";
      deleteButton.style.color = "red"; // Kırmızı renk ekle
      deleteButton.addEventListener("click", function() {
        // Silme işlemini onayla
        if (confirm(habitName + " alışkanlığını silmek istediğinizden emin misiniz?")) {
          delete habits[habitName];
          localStorage.setItem("habits", JSON.stringify(habits));
          loadHabits(); // Listeyi güncelle
        }
      });
      habitItem.appendChild(deleteButton);
  
      habitItem.addEventListener("click", function(event) {
        if (event.target !== deleteButton) { // Silme butonuna tıklanmadığında tabloyu aç
          createHabitTable(habitName);
        }
      });
  
      habitList.appendChild(habitItem);
    }
  }
  
  // Alışkanlık tablosunu oluştur
  function createHabitTable(habitName) {
    const habits = JSON.parse(localStorage.getItem("habits")) || {};
    const habit = habits[habitName];
  
    const table = document.createElement("table");
  
    const days = ["Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz"];
    let dayCounter = 1;
  
    for (let i = 0; i < 13; i++) { // 13 dönem için döngü
      const periodRow = table.insertRow(); // Dönem başlığı için satır ekle
      const periodHeader = periodRow.insertCell(); // Dönem başlığı için hücre ekle
      periodHeader.colSpan = 7; // Hücrenin 7 sütun kaplamasını sağla
      periodHeader.textContent = (i + 1) + ". Dönem - " + habit.targets[i]; // Dönem başlığını yazdır
  
      const periodStartDay = i * 28 + 1; // Dönemin başlangıç günü
  
      for (let j = 0; j < 4; j++) { // 4 hafta için döngü
        const weekRow = table.insertRow();
        for (let k = 0; k < 7; k++) { // 7 gün için döngü
          const dayCell = weekRow.insertCell();
          const currentDayOfYear = periodStartDay + j * 7 + k;
          const date = new Date(new Date().getFullYear(), 0, currentDayOfYear - 1); // Düzeltme burada
          const dayOfWeek = days[date.getDay()];


          
  
          dayCell.textContent = currentDayOfYear + " " + dayOfWeek;
  
          dayCell.addEventListener("click", (function(day) {
            return function() {
              markDay(habitName, day);
            }
          })(currentDayOfYear));
  
          const today = new Date();
          const startOfYear = new Date(today.getFullYear(), 0, 1);
          const diff = Math.floor((today - startOfYear) / (1000 * 60 * 60 * 24));
          const currentDay = diff + 1;
  
          if (currentDayOfYear < currentDay) {
            dayCell.classList.add("missed");
          } else if (currentDayOfYear === currentDay) {
            dayCell.classList.add("today");
          } else {
            dayCell.classList.add("disabled");
          }
  
          if (habit.days[currentDayOfYear]) {
            dayCell.classList.add("completed");
            dayCell.classList.remove("missed");
          } else if (currentDayOfYear < currentDay) {
            dayCell.classList.add("missed");
          }
        }
      }
    }
  
    const habitList = document.getElementById("habitList");
    const existingTable = habitList.querySelector("table");
    if (existingTable) {
      habitList.removeChild(existingTable);
    }
    habitList.appendChild(table);
  }


  // Gün işaretleme fonksiyonu
  function markDay(habitName, day) {
    const habits = JSON.parse(localStorage.getItem("habits")) || {};
    const habit = habits[habitName];
  
    const today = new Date();
    const startOfYear = new Date(today.getFullYear(), 0, 1);
    const diff = Math.floor((today - startOfYear) / (1000 * 60 * 60 * 24));
    const currentDay = diff + 1;
  
    if (day === currentDay) {
      habit.days[day] = !habit.days[day]; // Değeri tersine çevirerek güncelle
      localStorage.setItem("habits", JSON.stringify(habits));
      createHabitTable(habitName);
    }
  }

  