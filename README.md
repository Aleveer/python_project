<!-- Note -->
### Note
- Boundary copy code from Nguyên still has errors

<!-- How to get score and mode (Cách lấy score và mode) -->
### How to Get Score and Mode (Cách lấy score và mode)
1. **Xác định sự kiện game sẽ thua**  
   Khi người chơi thua, kiểm tra va chạm với các điều kiện sau:
   - Va chạm với chính mình:
     ![Collision check with itself](readme_source/collision%20check%20with%20itself.png)
   - Va chạm với tường:
     ![Collision check with wall](readme_source/collision%20check%20with%20wall.png)

2. **Get the score and mode**  
   Ngay sau khi game kết thúc, lấy điểm số và chế độ chơi bằng lệnh sau:
   ```python
   score = self.game.score_and_mode.get_score()
   mode = self.game.score_and_mode.get_mode()
