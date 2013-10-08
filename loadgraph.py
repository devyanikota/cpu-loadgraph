#!/usr/bin/env python


from flask import Flask, request, render_template
from urlparse import parse_qs
from loadgraphmodules.readsqlite import fetch_database
from re import split



app = Flask(__name__)



@app.route('/')
def index():
    """
Renders index view. The url accepts a query string with the following
fields:
selectby: parameter to which the range is related. Can be either:
*time - The selection is based on hour:minute for one given day.
Requires day_for_time field, as the day to which the
time is related.

*date - The selection is based on year/month/day format.

*all - The graphic shows the entire collection of data.

start: start of the range of the selection, in the format specified by
selectby.

end: end of the range of the selection.

day_for_time: specifies the day on which the time range is applied.
Note: that even when not needed, the field must be present
in the query string (with empty value if you will) or the
graphic won't be shown.

In case of error:
If at least one of the required fields is missing, KeyError is handled and
the template is rendered without graphic. Instead, only the filter
form is shown, which can be used to specify the data to be shown in the graph.

"""


    try:
        plot_data = manage_query(parse_qs(request.query_string,
                                          keep_blank_values = True))

        return render_template("index.html", plot_data = plot_data)

    except KeyError:
        print "Key Error, query string = %s" % request.query_string
        return render_template("index.html", plot_data = None)



def manage_query(query_string_dict):
    """
Accepts a dictionary containing the query string as the one returned by
urlparse.parse_qs, and returns an array containing all the data queried,
following the filter specified by the query string. Uses regex to remove
all possible date/time separators, as '-', '/' or ':' as the database
time and date data is stored without them.

"""

    """ Removing separators with regex """
    start = "".join(split("\.+|/+|-+|:+|'+", query_string_dict["start"][0]))
    end = "".join(split("\.+|/+|-+|:+|'+", query_string_dict["end"][0]))
    day_for_time = "".join(split("\.+|/+|-+|:+|'+",
                           query_string_dict["day_for_time"][0]))

    return fetch_database(query_string_dict["selectby"][0],
                          start,
                          end,
                          day_for_time,
                          "/var/www/html/loadgraph/database/sloads.db")



if __name__ == '__main__':
    app.debug=True
    app.run()
