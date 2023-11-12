# CHESS PUZZLE API

**Chess puzzle API!
This API utilizes chess puzzle data from the lichess database.
We will continue to update, so please give us a lot of interest.**

### Notice

- **Limit values per page maximum is 1000**

• **GET** **api/puzzle?limit=<int>& offset=<int>**

[](https://chess.run.goorm.site/api/puzzle)

**Provides puzzles.**

• **GET** **api/puzzle/theme?limit=<int>& offset=<int>**

[](https://chess.run.goorm.site/api/puzzle/theme)

**Provides puzzles with specific themes.**

• **GET** **api/rating?limit=<int>& offset=<int>**

[](https://chess.run.goorm.site/api/rating)

**Provides puzzles with specific rating.
The rating range is +100. To apply detailed ratings, use other API.**

 • **GET** **api/rating/range?max=<int>&min=<int>&limit=<int>& offset=<int>**

[](https://chess.run.goorm.site/api/rating/range)

**Provides puzzles with range of rating.**

• **GET** **api/tag?limit=<int>& offset=<int>**

[](https://chess.run.goorm.site/api/tag)

**Provides puzzles with specific tag.**

```json
"Tag" : ['easy', 'normal', 'hard']
```

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

**used LimitOffsetPagination technique.
The limit that can be called at once is limited to 1000.**

- **GET** **api/puzzle/move?puzzleid=<str>**

[](https://chess.run.goorm.site/api/puzzle/move)

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

**Provides fen and moves of puzzles with a specific ID.**

• **GET** **api/theme**

[](https://chess.run.goorm.site/api/theme)

```json
[
  {
    "theme": "string"
  }
]
```

**Provides all puzzle chess themes.**

• **GET** **api/puzzle/rush?num=<int>& easy=<int>& normal=<int>& hard=<int>**

[](https://chess.run.goorm.site/api/puzzle/rush)

```json
[
  {
    "puzzleid": "string",
    "rating": "string",
    "fen": "string",
    "tag": "string",
    "gameurl": "string"
  }
]
```

**This is the puzzle rush mode API. The number of puzzles that can be called at once is 100.**