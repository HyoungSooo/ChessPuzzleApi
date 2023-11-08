# Chess Puzzle API

- **GET** **/puzzle?limit=<int>& offset=<int> ⇒ puzzle 데이터를 limit만큼 제공.**

```json
{
  "items": [
    {
      "puzzleid": "string",
      "rating": "string",
      "fen": "string",
      "tag": "string",
      "gameurl": "string"
    }
  ],
  "count": 0
}
```

- **GET** **/puzzle/move?puzzleid=<str> ⇒ 특정 퍼즐의 문제 정보를 제공**

```json
}
	"puzzleid": "string",
  "tag": "string",
  "fen": "string",
  "move": [
    "string"
  ]
}
```

- **GET** **/theme ⇒ 모든 퍼즐의 테마를 제공**

```json
[
  {
    "theme": "string"
  }
]
```

- **GET** **/theme/puzzle?theme=<str> ⇒ 특정 테마의 퍼즐 중 랜덤한 하나의 퍼즐을 제공**

```json
{
  "puzzleid": "string",
  "tag": "string",
  "fen": "string",
  "move": [
    "string"
  ]
}
```
