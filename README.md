<!-- Note -->
### Note
- Boundary copy code from Nguyên still has errors

<!-- How to get score and mode (Cách lấy score và mode) -->
### How to Get Score and Mode (Cách lấy score và mode)
1. Xác định sự kiện game sẽ thua
![collision check with itself](readme_source/collision%20check%20with%20itself.png)
![collision check with wall](readme_source/collision%20check%20with%20wall.png)
2. Get the score and mode right after losing and save them to any variable using the command
`score = self.game.score_and_mode.get_score()`

`mode = self.game.score_and_mode.get_mode()`
