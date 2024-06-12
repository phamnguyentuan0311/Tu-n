let originalText = "";

$(document).ready(function () {
    $('#checkBtn').click(() => {
        const text = $("#textToCheck").val().trim();
        originalText = text;

        // Kiểm tra nếu văn bản đầu vào không rỗng
        if (text) {
            // Hiển thị biểu tượng loading hoặc thông báo cho người dùng
            $("#checkBtn").prop("disabled", true).text("Đang kiểm tra...");

            $.ajax({
                type: "POST",
                url: `/`,
                contentType: 'application/json',
                data: JSON.stringify({ text }),
                success: (result) => {
                    // Xử lý kết quả trả về
                    const correctedText = result.corrected_text;
                    const wordCount = result.word_count;
                    $("#updatedText").text(correctedText);
                    $("#wordCount").text(`Số từ: ${wordCount}`);

                    // Đặt lại trạng thái của nút
                    $("#checkBtn").prop("disabled", false).text("Kiểm tra");
                },
                error: (xhr, status, error) => {
                    console.error("Lỗi: ", status, error);
                    alert("Đã xảy ra lỗi. Vui lòng thử lại.");

                    // Đặt lại trạng thái của nút
                    $("#checkBtn").prop("disabled", false).text("Kiểm tra");
                }
            });
        } else {
            alert("Vui lòng nhập văn bản");
        }
    });
});
