import flask
from flask import render_template, request, jsonify
import pandas as pd
from constants import Name_File_Path
from boltons.setutils import IndexedSet
from copy import deepcopy

app = flask.Flask("Search By Name")

def get_search_result(df,column, search_str):
    result = list()
    df_copy  = deepcopy(df)
    df_copy[column] = df_copy[column].str.lower()
    idx = df_copy["Name"].str.contains(search_str)
    df_contain = df_copy["Name"][idx]
    df_start = df_contain.where(df_contain.str.startswith(search_str))
    df_start = df_start[~df_start.isnull()].values.tolist()
    df_start.sort()
    df_start.sort(key=len)
    df_in = df_contain.where(df_contain.str.startswith(search_str) == False)
    df_in = df_in[~df_in.isnull()].values.tolist()
    df_in.sort()
    df_in.sort(key=len)
    result.extend(df_start)
    result.extend(df_in)

    return result, idx

@app.route("/", methods = ["GET", "POST"])
def search():
    context = dict()
    try:
        if request.args:
            key_word = request.args["key"]
            df = pd.read_csv(Name_File_Path)
            search_result = []
            for idx in range(len(key_word) - 2):
                search_q = key_word[:len(key_word) - idx]
                r_list, used_word = get_search_result(df, "Name", search_q.lower())
                search_result.extend(r_list)
                index = df["Name"][used_word == True].index
                df = df.drop(index=index, axis=0)
            result = list(IndexedSet(search_result))
            if not result:
                context["message"] = "No Result Found!"
            else:
                context["search_result"] =  result
            return jsonify(context)
        else:
            return render_template("index.html", context=context)
    except Exception as e:
        return render_template("index.html", context={
            "error_message": str(e),
            "message": "Internal server error"
        })


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=27001)