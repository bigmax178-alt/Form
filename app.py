from flask import Flask, render_template, request, send_file
from docxtpl import DocxTemplate
from docx2pdf import convert
import os

app = Flask(__name__)

def make_short_name(full_name: str) -> str:
    parts = full_name.split()
    if len(parts) == 3:
        return f"{parts[0]} {parts[1][0]}.{parts[2][0]}."
    elif len(parts) == 2:
        return f"{parts[0]} {parts[1][0]}."
    else:
        return full_name

@app.route("/")
def form():
    return render_template("form.html")

@app.route("/generate", methods=["POST"])
def generate():
    customer_name = request.form["customer_name"]

    context = {
        "contract_number": request.form["contract_number"],
        "contract_date": request.form["contract_date"],
        "start_date": request.form["start_date"],
        "customer_name": customer_name,
        "customer_short": make_short_name(customer_name),
        "customer_inn": request.form["customer_inn"],
        "customer_ogrnip": request.form["customer_ogrnip"],
        "customer_rs": request.form["customer_rs"],
        "customer_bank": request.form["customer_bank"],
        "customer_bik": request.form["customer_bik"],
        "customer_kors": request.form["customer_kors"],
        "bank_inn": request.form["bank_inn"],
        "bank_kpp": request.form["bank_kpp"]
    }

    template = DocxTemplate("Договор-шаблон-v2.docx")
    template.render(context)
    docx_file = "Договор_готовый.docx"
    pdf_file = "Договор_готовый.pdf"
    template.save(docx_file)

    try:
        convert(docx_file, pdf_file)
        return send_file(pdf_file, as_attachment=True)
    except:
        return send_file(docx_file, as_attachment=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
