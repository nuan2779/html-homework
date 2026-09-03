// 1. Khai báo hàm bất đồng bộ bằng async
async function loadUsers() {
    try {
        // 2. Gọi API để lấy dữ liệu
        const response = await fetch("https://jsonplaceholder.typicode.com/users");
        const users = await response.json();
        const tbody = document.querySelector("#user-table tbody");
        
        // 5. Lặp qua từng người dùng trong mảng data vừa lấy được
        users.forEach(function(user) {
            // Tạo một hàng <tr> mới
            const row = document.createElement("tr");
    
            row.innerHTML = `
                <td>${user.id}</td>
                <td>${user.name}</td>
                <td>${user.email}</td>
                <td>${user.address.city}</td>
                <td>${user.address.zipcode}</td>
            `;
            
            tbody.appendChild(row);
        });

    } catch (error) {
        console.error("Lỗi khi gọi API:", error);
    }
}
loadUsers();
