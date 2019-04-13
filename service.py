import flask
from flask import render_template, request, jsonify
import pandas as pd
from constants import Name_File_Path
from copy import deepcopy

app = flask.Flask("Search By Name")

def get_search_result(df,column, search_str):
    df_copy = deepcopy(df)
    df_copy[column] = df_copy[column].str.lower()
    df_contain = df_copy[column][df_copy[column].str.contains(search_str.lower())]
    df_contain = df_contain.drop_duplicates()
    df_start = df_contain.where(df_contain.str.startswith(search_str.lower()))
    df_start = df_start[~df_start.isnull()]
    idx = df_start.str.len().sort_values().index
    df_start = df.reindex(idx)
    df_in = df_contain.where(df_contain.str.startswith(search_str.lower()) == False)
    df_in = df_in[~df_in.isnull()]
    idx = df_in.str.len().sort_values().index
    df_in = df.reindex(idx)
    return df_start.append(df_in)[column].values.tolist()

@app.route("/", methods = ["GET", "POST"])
def search():
    context = dict()
    try:
        if request.args:
            key_word = request.args["key"]
            df = pd.read_csv(Name_File_Path)
            df.columns = ["Name"]
            result = get_search_result(df, "Name", key_word.lower())
            if not result:
                context["message"] = "No Result Found!"
            else:
                context["search_result"] =  result
            return jsonify(context)
        else:
            return render_template("index.html", context=context)
    except Exception as e:
        return render_template("index.html", context={
            "error_message":str(e),
            "message":"Internal server error"
        })


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=27001)