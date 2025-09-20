function exportToTxt() {
    const table = document.getElementById("resultTable");
    if (!table) {
      alert("Nincs adat a táblázatban!");
      return;
    }
    let txt = "";
    // fejlécek
    const headers = Array.from(table.querySelectorAll("thead th"))
      .map(th => th.innerText.trim()).join("\t");
    txt += headers + "\n";
    // sorok
    const rows = table.querySelectorAll("tbody tr");
    rows.forEach(tr => {
      const cells = Array.from(tr.querySelectorAll("td"))
        .map(td => td.innerText.trim()).join("\t");
      txt += cells + "\n";
    });
    // letöltés TXT-ként
    const blob = new Blob([txt], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "tabla_export.txt";
    a.click();
    URL.revokeObjectURL(url);
  }