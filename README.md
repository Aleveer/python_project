<!-- Lưu ý -->
- Boundary copy code của Nguyên vô còn lỗi

<!-- Cách lấy score và mode  -->
1. Xác định sự kiện game sẽ thua
![collision check with itself](readme_source/collision%20check%20with%20itself.png)
![collision check with wall](readme_source/collision%20check%20with%20wall.png)
2. Lấy score và mode ngay sau khi thua và lưu vào biến tùy ý bằng lệnh
`score = self.game.score_and_mode.get_score()`
`mode = self.game.score_and_mode.get_mode()`
