from flask import Flask, render_template, request, redirect, url_for
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


UPLOAD_FOLDER = "uploads"
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def index():
    csv_files = [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith(".csv")]

    return render_template("index.html", csv_files=csv_files)


@app.route("/statistic/<filename>/")
def statistic(filename):
    # Путь к загруженному CSV файлу
    file_path = f"uploads/{filename}"

    # Чтение CSV файла с помощью pandas
    df = pd.read_csv(file_path)

    # Получение основной статистики
    stats = {
        "columns": df.columns.tolist(),
        "shape": df.shape,
        "description": df.describe().to_html(),
        "null_values": df.isnull().sum().to_dict(),
    }

    # Передаем статистику в шаблон
    return render_template("stat.html", stats=stats, filename=filename)


@app.route("/upload/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["file"]
        if file and file.filename.endswith(".csv"):
            file_path = os.path.join(
                app.config["UPLOAD_FOLDER"],
                file.filename
            )
            file.save(file_path)
            return redirect(url_for("plot", filename=file.filename))
    return render_template("upload.html")


@app.route("/plot/<filename>/")
def plot(filename):
    try:
        col = request.args.get("col")
        context = {}
        context["filename"] = filename
        # titanic.csv
        # ru.csv
        df = pd.read_csv(f"uploads/{filename}")
        columns = df.columns.tolist()
        context["columns"] = columns
        context["message"] = "Hello from code"
        col = request.args.get("col")
        unic = len(df[col].unique())

        if unic > 50:
            context["error"] = "To many vallues"
            return render_template("plot.html", context=context)

        sns.countplot(x=col, data=df)
        save_path = os.path.join("static", "plot.png")
        plt.savefig(save_path)
        plt.close()
    except Exception:
        plt.close()
        return render_template("plot.html", context=context)

    return render_template("plot.html", context=context)


if __name__ == "__main__":
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    if not os.path.exists("static"):
        os.makedirs("static")
    app.run(host="0.0.0.0", port=5000)
