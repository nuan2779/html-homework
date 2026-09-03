async function loadPrice() {
    try {
        const response = await fetch("./data.json");
        const data = await response.json();
       
        const tbody = document.querySelector("#pricing-table tbody");

        data.forEach(function(item){
            const row = document.createElement("tr");

            row.innerHTML = `
                <td>${item.tenGoi}</td>
                <td>${item.gia}</td>
                <td>${item.thoiLuongTuan}</td>
                <td>${item.thoiLuongThang}</td>
            `;
            tbody.appendChild(row);
        });
    } catch (error) {
        console.error("Error fetching price data:", error);
    }
}

loadPrice();