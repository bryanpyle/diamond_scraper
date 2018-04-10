import json
import urllib.request
import urllib

COMMA = "%2C"
# 8812 4/9 pm
# 8980 4/10 am
# should have a target and if it's worse, minus points, but if better, plus points. 

SHAPE_TOLERANCE =   0   # max 1
CUT_TOLERANCE =     4   # max 4
COLOR_TOLERANCE =   5   # max 6   
CLARITY_TOLERANCE = 6   # max 7

CUT_TARGET =        "Ideal"
COLOR_TARGET =      "H"
CLARITY_TARGET =    "VS2"
PRICE_TARGET =      3500

MIN_CARAT =     1.25
MAX_CARAT =     1.5
MIN_PRICE =     2500
MAX_PRICE =     4000
NUM_RESULTS =   1000
REAL_VIEW =     "Yes"

COLOR_WEIGHT = 100 
CUT_WEIGHT = 100 
CLARITY_WEIGHT = 50 
PRICE_WEIGHT = 33

def getMap(array, target):
    _map = {}

    target_index = array.index(target)
    value = -target_index
    for i, elem in enumerate(array):
        _map[elem.replace("+", " ")] = value
        value = value + 1
    return _map

def buildParamString(type_array, tolerance):
    param_string = ""
    i = 0
    while i <= tolerance:
        if i == tolerance:
            param_string = param_string + type_array[i]
        else:
            param_string = param_string + type_array[i] + COMMA
        i = i+1
    return param_string


# arrays
shapes = ["Round", "Cushion"]
cuts = ["Super+Ideal", "Ideal", "Very+Good", "Good", "Fair"]
colors = ["D", "E", "F", "G", "H", "I", "J"]
clarities = ["FL", "IF", "VVS1", "VVS2", "VS1", "VS2", "SI1", "SI2"]

# maps
color_map = getMap(colors, COLOR_TARGET)
cut_map = getMap(cuts, CUT_TARGET)
clarity_map = getMap(clarities, CLARITY_TARGET)


print(clarity_map)

def diamondImperfections(color, cut, clarity, price):
    price_score = (price - PRICE_TARGET) * PRICE_WEIGHT / 100
    color_score = COLOR_WEIGHT * color_map[color]
    cut_score = CUT_WEIGHT * cut_map[cut]
    clarity_score = CLARITY_WEIGHT * clarity_map[clarity]
    return price_score + color_score + cut_score + clarity_score

def mapDiamond(d):
    diamond = {}
    diamond["id"] = d["id"]
    diamond["carat"] = d["carat"]
    diamond["clarity"] = d["clarity"]
    diamond["color"] = d["color"]
    diamond["cut"] = d["cut"]
    diamond["price"] = d["price"]
    diamond["link"] = "https://www.brilliantearth.com/lab-diamonds-search/view_detail/" + str(diamond["id"])
    diamond["imperfection"] = diamondImperfections(diamond["color"], diamond["cut"], diamond["clarity"], diamond["price"])
    return diamond

# params
shapes_param = buildParamString(shapes, SHAPE_TOLERANCE)
cuts_param = buildParamString(cuts, CUT_TOLERANCE)
colors_param = buildParamString(colors, COLOR_TOLERANCE)
clarities_param = buildParamString(clarities, CLARITY_TOLERANCE)
min_carat_param = str(MIN_CARAT)
max_carat_param = str(MAX_CARAT)
min_price_param = str(MIN_PRICE)
max_price_param = str(MAX_PRICE)
num_results_param = str(NUM_RESULTS)
real_view_param = REAL_VIEW


def urlEncode(query):
    query.replace(",", "%2C")
    query.replace(" ", "+")
    return query

query = "shapes=%s&cuts=%s&colors=%s&clarities=%s&min_carat=%s&max_carat=%s&min_price=%s&max_price=%s&requestedDataSize=%s&real_diamond_view=%s"\
    % (shapes_param, cuts_param, colors_param, clarities_param, \
    min_carat_param, max_carat_param, min_price_param, max_price_param, num_results_param, real_view_param)
url = "https://www.brilliantearth.com/lab-diamonds/list/?%s" % (query)

print(url, "\n")

data = json.load(urllib.request.urlopen(url))["diamonds"]
diamonds = list(map(mapDiamond, data))

print("Number Diamonds: ", len(diamonds))

max_d = 0
for i, d in enumerate(diamonds):
    if d["imperfection"] > max_d:
        max_d = d["imperfection"]

sorted_diamonds = sorted(diamonds, key = lambda d: (d['imperfection']))

print()
def printDiamond(diamond):
    print("%s: %s\n\t%d %s %s %s %s\n\t%s\n" % (diamond["id"], diamond["imperfection"], diamond["price"], diamond["carat"], diamond["color"], diamond["clarity"], diamond["cut"], diamond["link"]))

i = 0
while i < 10:
    printDiamond(sorted_diamonds[i])
    i = i + 1

print("WORST:")
printDiamond(sorted_diamonds[-1])

# for d in sorted_diamonds:
#     printDiamond(d)




