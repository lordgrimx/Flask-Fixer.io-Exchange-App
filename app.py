from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "8a91d5ecea8d7aaa6e3ee9e6f7506dac"
URL = f"http://data.fixer.io/api/latest?access_key={API_KEY}"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        first_currency = request.values.get("firstCurrency")
        print(first_currency)
        second_currency = request.form.get("secondCurrency")
        print(second_currency)
        amount = request.form.get("amount")
        print(amount)

        response = requests.get(url=URL)
        infos = response.json()

        if "rates" in infos and first_currency in infos["rates"] and second_currency in infos["rates"]:
            first_value = infos["rates"][first_currency]
            second_value = infos["rates"][second_currency]

            result = f"{((second_value / first_value) * float(amount)):.2f}"

            currency_info = {
                "firstCurrency": first_currency,
                "secondCurrency": second_currency,
                "amount": amount,
                "result": result
            }

            return render_template("index.html", info=currency_info)
        else:
            error_message = "One or both of the currencies provided are not available."
            return render_template("index.html", error=error_message)
    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
