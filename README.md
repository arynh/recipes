# Recipes

_Efficiently describe and present recipes for easy reference._

This tool parses recipes in a standardized JSON format, produces human-readable Latex, then renders them as PDFs. An example of the format of the JSON recipe files:

```json
{
  "dish_name": "Toast",
  "author": "Gordon Ramsay",
  "source": "the chef himself",
  "notes": "This happens to be one of Gordon's more difficult dishes.",
  "ingredients": ["bread", "butter"],
  "method": ["toast the bread", "spread the butter"]
}
```
