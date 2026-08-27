alert ("Hello from an embedded script");
//LAB1
const grade = [
    {id: 1, name: "Phúc", math: 9, english:8.5, physics:9.5},
    {id: 2, name: "Phúc", math: 8, english:9, physics:8},
    {id: 3, name: "Phúc", math: 6.5, english:9.5, physics:7.5},
    {id: 4, name: "Phúc", math: 7, english:7, physics:8.5}
]
//Tổng điểm các môn của cả lớp 
const sumScores = (grade,subject) => {
    let total = 0
    for (let i = 0; i < grade.length; i++) {
        total += grade[i][subject];
    }
    return total;
};
console.log("Tổng điểm toán của lớp: ", sumScores(grade,"math"));
console.log("Tổng điểm anh của lớp: ", sumScores(grade,"english"));
console.log("Tổng điểm lý của lớp: ", sumScores(grade,"physics"));

//Học sinh có điểm trung bình cao nhất
function find_highest_grade(grade) {
    let top_student = grade[0];
    let avg_grade = (top_student.math + top_student.english + top_student.physics) / 3;

    for (let i = 1; i < grade.length; i++) {
        const current_student = grade[i]
        const current_grade = (current_student.math + current_student.english + current_student.physics) / 3;

        if (current_grade > avg_grade) {
            top_student = current_student;
            avg_grade = current_grade;
        }
    }
    return top_student;
};
console.log("Học sinh có điểm trung bình cao nhất: ",find_highest_grade(grade));

//Học sinh có ít nhất 1 môn có điểm trên 8
const atLeastOneExcellent = [];

for (let i = 0; i < grade.length; i++) {
    const studentss = grade[i];
    
    // Dùng || (HOẶC): Chỉ cần 1 trong 3 điều kiện đúng là lấy
    if (studentss.math > 8 || studentss.physics > 8 || studentss.english > 8) {
        atLeastOneExcellent.push(studentss);
    }
}

console.log("Học sinh có ít nhất 1 môn trên 8:", atLeastOneExcellent);


//LAB2

const form = document.querySelector("form");
const messageArea = document.createElement("div");
form.parentNode.appendChild(messageArea);

form.addEventListener("submit", function(event) {
    event.preventDefault();

    messageArea.innerHTML= "";

    const nameValue = document.getElementById("name").value;
    const phoneValue = document.getElementById("phone").value;
    const emailValue = document.getElementById("email").value;
    //xác minh form email
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (nameValue.trim() === "" || phoneValue.trim() === "" || emailValue.trim() === "") {
        const errorMsg = document.createElement("p");
        errorMsg.innerText = "Lỗi: Vui lòng điền đầy đủ thông tin";
        errorMsg.style.color = "red";
        messageArea.appendChild(errorMsg);

    } else if (Number(phoneValue) <= 0 || isNaN(Number(phoneValue))) {
        const errorMsg =  document.createElement("p")
        errorMsg.innerText = "Lỗi: Số điện thoại không hợp lệ";
        errorMsg.style.color = "red";
        messageArea.appendChild(errorMsg);

    } else if (emailRegex.test(emailValue) == false) {
        const errorMsg = document.createElement("p");
        errorMsg.innerText = "Lỗi: Định dạng email không hợp lệ";
        errorMsg.style.color = "red";
        messageArea.appendChild(errorMsg);
    
    } else {
        const successMsg = document.createElement("p");
        successMsg.innerText = "Đăng kí thành công";
        successMsg.style.color = "green";
        messageArea.appendChild(successMsg);
    }

});
