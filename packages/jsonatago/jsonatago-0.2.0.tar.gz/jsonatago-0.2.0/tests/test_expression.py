from jsonatago import Jsonata

JSONATA_TEST_DATA = """
{
  "Account": {
    "Account Name": "Firefly",
    "Order": [
      {
        "OrderID": "order103",
        "Product": [
          {
            "Product Name": "Bowler Hat",
            "ProductID": 858383,
            "SKU": "0406654608",
            "Description": {
              "Colour": "Purple",
              "Width": 300,
              "Height": 200,
              "Depth": 210,
              "Weight": 0.75
            },
            "Price": 34.45,
            "Quantity": 2
          },
          {
            "Product Name": "Trilby hat",
            "ProductID": 858236,
            "SKU": "0406634348",
            "Description": {
              "Colour": "Orange",
              "Width": 300,
              "Height": 200,
              "Depth": 210,
              "Weight": 0.6
            },
            "Price": 21.67,
            "Quantity": 1
          }
        ]
      },
      {
        "OrderID": "order104",
        "Product": [
          {
            "Product Name": "Bowler Hat",
            "ProductID": 858383,
            "SKU": "040657863",
            "Description": {
              "Colour": "Purple",
              "Width": 300,
              "Height": 200,
              "Depth": 210,
              "Weight": 0.75
            },
            "Price": 34.45,
            "Quantity": 4
          },
          {
            "ProductID": 345664,
            "SKU": "0406654603",
            "Product Name": "Cloak",
            "Description": {
              "Colour": "Black",
              "Width": 30,
              "Height": 20,
              "Depth": 210,
              "Weight": 2
            },
            "Price": 107.99,
            "Quantity": 1
          }
        ]
      }
    ]
  }
}
"""


def test_evaluate():
    expr = Jsonata("$sum(Account.Order.Product.(Price * Quantity))")
    print(expr.evaluate(JSONATA_TEST_DATA))
