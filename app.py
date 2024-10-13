from flask import Flask, request, render_template, redirect, url_for, request

import pandas as pd
import matplotlib.pyplot as plt

import os

import seaborn as sns

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["file"]
        if file and file.filename.endswith(".csv"):
            file_path = os.path.join(
                app.config["UPLOAD_FOLDER"], file.filename
            )
            file.save(file_path)
            return redirect(url_for('select_columns'))
    return render_template("upload.html")


# @app.route("/plot/<filename>")
# def plot(filename):
#     return render_template("plot.html", filename=filename)


@app.route("/select_columns", methods=["GET", "POST"])
def select_columns():
    filename = request.args.get("filename")

    if filename:
        df = pd.read_csv(f"uploads/{filename}")
        columns = df.columns.tolist()

    if request.method == "POST":
        x_column = request.form["x_column"]
        y_column = request.form["y_column"]
        return redirect(
            url_for(
                "plot_chart", column_x=x_column, column_y=y_column
            )
        )

    return render_template("select_columns.html", columns=columns)


@app.route("/plot/<column_x>/<column_y>")
def plot_chart(column_x, column_y):
    df = pd.read_csv("uploads/titanic.csv")

    # df_numeric = df.select_dtypes(include=["float64", "int64"])
    # corr = df_numeric.corr()
    # sns.heatmap(corr, annot=True, cmap='coolwarm')

    # Построение графика зависимости
    # plt.figure()
    # plt.scatter(df[column_x], df[column_y])
    # plt.xlabel(column_x)
    # plt.ylabel(column_y)

    # sns.boxplot(x=column_x, y=column_y, data=df)

    try:
        sns.countplot(x=column_x, data=df)

        # Сохранение графика в директорию static
        plot_path = os.path.join("static", "plot.png")
        plt.savefig(plot_path)
        plt.close()
    except Exception:
        return render_template("index.html")
    return render_template("plot.html")


@app.route("/datasets", methods=["GET"])
def list_datasets():
    files = os.listdir("uploads")
    files = [f for f in files if f.endswith(".csv")]
    return render_template("list_datasets.html", files=files)


if __name__ == "__main__":
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    if not os.path.exists("static"):
        os.makedirs("static")
    app.run(host="0.0.0.0", port=10000)
