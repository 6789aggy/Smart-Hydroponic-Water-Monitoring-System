from flask import Flask, request, jsonify, render_template_string, redirect
import sqlite3
import re
from datetime import datetime, timedelta

app = Flask(__name__)

# ==================================
# DATABASE
# ==================================

DB_NAME = "hydroponic_pro.db"

# ==================================
# GLOBAL SENSOR DATA
# ==================================

sensor_data = {
    "ph": 0,
    "turbidity": 0,
    "level": 0,
    "flow": 0,
    "pump": "OFF"
}

# ==================================
# SYSTEM STATUS
# ==================================

status_text = "Khởi động"
message_text = "Đang chờ dữ liệu"

mode = "THỦ CÔNG"

recommended_seconds = 0

auto_end_time = None

pump_command = ""

# ==================================
# HISTORY BUFFER FOR CHARTS
# ==================================

chart_history = {
    "time": [],
    "ph": [],
    "turbidity": [],
    "level": [],
    "flow": []
}

MAX_POINTS = 30
# ==================================
# INIT DATABASE
# ==================================

def init_db():

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS logs(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        timestamp TEXT,

        ph REAL,

        turbidity REAL,

        level REAL,

        flow REAL,

        pump TEXT,

        status TEXT
    )
    """)

    conn.commit()
    conn.close()
    # ==================================
# SAVE LOG
# ==================================

def save_log():

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
    INSERT INTO logs
    (
        timestamp,
        ph,
        turbidity,
        level,
        flow,
        pump,
        status
    )
    VALUES
    (
        ?,?,?,?,?,?,?
    )
    """,
    (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

        sensor_data["ph"],

        sensor_data["turbidity"],

        sensor_data["level"],

        sensor_data["flow"],

        sensor_data["pump"],

        status_text
    ))

    conn.commit()
    conn.close()
    # ==================================
# GET LOGS
# ==================================

def get_logs(limit=50):

    conn = sqlite3.connect(DB_NAME)

    c = conn.cursor()

    c.execute("""
    SELECT
        timestamp,
        ph,
        turbidity,
        level,
        flow,
        pump,
        status

    FROM logs

    ORDER BY id DESC

    LIMIT ?
    """, (limit,))

    rows = c.fetchall()

    conn.close()

    return rows
    # ==================================
# EXTRACT NUMBER
# ==================================

def extract_number(text):

    m = re.search(
        r"[-+]?\d*\.?\d+",
        str(text)
    )

    if m:
        return float(m.group())

    return 0


# ==================================
# PARSE SENSOR STRING
# ==================================

def parse_sensor(raw):

    global sensor_data

    parts = raw.split(",")

    parsed = {}

    for p in parts:

        if ":" in p:

            k, v = p.split(":", 1)

            parsed[k.strip()] = v.strip()

    sensor_data["ph"] = extract_number(
        parsed.get("PH", 0)
    )

    sensor_data["turbidity"] = extract_number(
        parsed.get("TUR", 0)
    )

    sensor_data["level"] = extract_number(
        parsed.get("LEVEL", 0)
    )

    sensor_data["flow"] = extract_number(
        parsed.get("FLOW", 0)
    )

    sensor_data["pump"] = parsed.get(
        "PUMP",
        "OFF"
    )
    # ==================================
# UPDATE CHART DATA
# ==================================

def update_chart_data():

    now = datetime.now().strftime("%H:%M:%S")

    chart_history["time"].append(now)

    chart_history["ph"].append(
        sensor_data["ph"]
    )

    chart_history["turbidity"].append(
        sensor_data["turbidity"]
    )

    chart_history["level"].append(
        sensor_data["level"]
    )

    chart_history["flow"].append(
        sensor_data["flow"]
    )

    if len(chart_history["time"]) > MAX_POINTS:

        for key in chart_history:

            chart_history[key].pop(0)
            # ==================================
# ANALYSIS ENGINE
# ==================================

def analyze():

    global status_text
    global message_text
    global recommended_seconds

    turb = sensor_data["turbidity"]

    level = sensor_data["level"]

    flow = sensor_data["flow"]

    pump = sensor_data["pump"]

    recommended_seconds = 0

    if level < 100:

        status_text = "NGUY HIỂM"

        message_text = (
            "Mực nước quá thấp"
        )

        return

    if pump == "ON" and flow < 0.1:

        status_text = "CẢNH BÁO"

        message_text = (
            "Bơm chạy nhưng không có lưu lượng"
        )

        return

    if turb > 900:

        status_text = "NGUY HIỂM"

        message_text = (
            "Nước rất đục"
        )

        recommended_seconds = 30

    elif turb > 700:

        status_text = "CẢNH BÁO"

        message_text = (
            "Nước đục cao"
        )

        recommended_seconds = 20

    elif turb > 500:

        status_text = "CẢNH BÁO"

        message_text = (
            "Nước hơi đục"
        )

        recommended_seconds = 10

    else:

        status_text = "AN TOÀN"

        message_text = (
            "Hệ thống ổn định"
        )
# ==================================
# IOT PRO DASHBOARD
# ==================================

HTML = """
<!DOCTYPE html>
<html lang="vi">

<head>

<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width,
               initial-scale=1.0">

<title>
Giám sát thủy canh thông minh
</title>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

<style>

html{
    scroll-behavior:smooth;
}

*{
    margin:0;
    padding:0;
    box-sizing:border-box;
    font-family:'Segoe UI',sans-serif;
}

body{

    background:
    linear-gradient(
        135deg,
        #0f172a,
        #1e293b,
        #0f172a
    );

    color:white;

    min-height:100vh;
}

/* ==========================
SIDEBAR
========================== */

.sidebar{

    position:fixed;

    left:0;
    top:0;

    width:240px;
    height:100vh;

    background:
    rgba(15,23,42,0.95);

    border-right:
    1px solid rgba(255,255,255,0.08);

    padding:25px;
}

.logo{

    font-size:24px;
    font-weight:bold;

    color:#38bdf8;

    margin-bottom:30px;
}

.menu-item{

    display:block;

    color:#cbd5e1;

    text-decoration:none;

    padding:14px 18px;

    margin-bottom:8px;

    border-radius:12px;

    transition:all .3s ease;

    font-size:15px;

    font-weight:500;
}

.menu-item:hover{

    background:
    rgba(56,189,248,.15);

    color:#38bdf8;

    transform:
    translateX(4px);
}

/* MENU ĐANG ACTIVE */

.menu-item.active{

    background:
    linear-gradient(
        90deg,
        #0ea5e9,
        #38bdf8
    );

    color:white;

    font-weight:600;

    box-shadow:
    0 0 15px
    rgba(56,189,248,.35);
}

/* ==========================
MAIN
========================== */

.main{

    margin-left:260px;

    padding:25px;
}

.title{

    font-size:34px;

    font-weight:bold;

    margin-bottom:25px;
}

/* ==========================
STATUS BAR
========================== */

.status-bar{

    display:flex;

    gap:15px;

    flex-wrap:wrap;

    margin-bottom:20px;
}

.status-box{

    background:
    rgba(255,255,255,0.08);

    backdrop-filter:blur(12px);

    padding:12px 20px;

    border-radius:15px;
}

/* ==========================
CARDS
========================== */

.cards{

    display:grid;

    grid-template-columns:
    repeat(
      auto-fit,
      minmax(220px,1fr)
    );

    gap:20px;
}

.card{

    background:
    rgba(255,255,255,0.08);

    backdrop-filter:blur(12px);

    border:
    1px solid rgba(255,255,255,0.08);

    border-radius:20px;

    padding:25px;

    text-align:center;

    transition:0.3s;
}

.card:hover{

    transform:
    translateY(-5px);
}

.card-title{

    font-size:18px;

    color:#cbd5e1;

    margin-bottom:12px;
}

.card-value{

    font-size:36px;

    font-weight:bold;
}

/* ==========================
ALERT BOX
========================== */

.alert-box{

    margin-top:25px;

    background:
    rgba(255,255,255,0.08);

    padding:25px;

    border-radius:20px;
}

#status{

    font-size:28px;

    font-weight:bold;
}

/* ==========================
BUTTONS
========================== */

.controls{

    margin-top:25px;

    display:flex;

    gap:15px;

    flex-wrap:wrap;
}

.btn{

    border:none;

    padding:14px 24px;

    border-radius:12px;

    color:white;

    cursor:pointer;

    font-size:16px;

    font-weight:bold;

    transition:0.3s;
}

.btn:hover{

    transform:scale(1.05);
}

.btn-on{

    background:
    linear-gradient(
      45deg,
      #16a34a,
      #22c55e
    );
}

.btn-off{

    background:
    linear-gradient(
      45deg,
      #dc2626,
      #ef4444
    );
}

.btn-auto{

    background:
    linear-gradient(
      45deg,
      #2563eb,
      #3b82f6
    );
}

/* ==========================
CHART AREA
========================== */

.chart-container{

    margin-top:30px;

    background:
    rgba(255,255,255,0.08);

    padding:20px;

    border-radius:20px;
}

canvas{

    max-height:400px;
}

/* ==========================
TABLE
========================== */

.logs{

    margin-top:30px;

    background:
    rgba(255,255,255,0.08);

    padding:20px;

    border-radius:20px;
}

table{

    width:100%;

    border-collapse:collapse;
}

th{

    background:#2563eb;

    padding:12px;
}

td{

    padding:10px;

    text-align:center;

    border-bottom:
    1px solid rgba(255,255,255,0.05);
}

/* ==========================
RESPONSIVE
========================== */

@media(max-width:900px){

    .sidebar{

        display:none;
    }

    .main{

        margin-left:0;
    }
}

.safe{
    color:#22c55e;
}

.warning{
    color:#facc15;
}

.danger{
    color:#ef4444;
}

.menu-item{
    display:block;
    color:white;
    text-decoration:none;
    padding:15px;
    margin-bottom:10px;
    border-radius:12px;
    transition:0.3s;
}

.menu-item:hover{
    background:rgba(255,255,255,0.08);
    color:#38bdf8;
}

</style>
</head>

<body>

<div class="sidebar">

<div class="logo">
🌱 Hydroponic Pro
</div>

<a href="#top"
   class="menu-item nav-link active">
🏠 Dashboard
</a>

<a href="#chart"
   class="menu-item nav-link">
📊 Thống kê
</a>

<a href="#water"
   class="menu-item nav-link">
💧 Chất lượng nước
</a>

<a href="#control"
   class="menu-item nav-link">
⚙ Điều khiển
</a>

<a href="#logs"
   class="menu-item nav-link">
📝 Nhật ký
</a>

</div>

<div id="top" class="main">

<div class="title">
GIÁM SÁT THỦY CANH THÔNG MINH
</div>

<div class="status-bar">

<div class="status-box">
ESP8266 ● Online
</div>

<div class="status-box">
Arduino UNO ● Online
</div>

<div class="status-box">
WiFi ● Connected
</div>

</div>

<div id="water" class="cards">

<div class="card">
<div class="card-title">
💧 pH
</div>
<div id="ph"
     class="card-value">
0
</div>
</div>

<div class="card">
<div class="card-title">
🌫 Độ đục
</div>
<div id="turbidity"
     class="card-value">
0
</div>
</div>

<div class="card">
<div class="card-title">
📏 Mực nước
</div>
<div id="level"
     class="card-value">
0
</div>
</div>

<div class="card">
<div class="card-title">
🌊 Lưu lượng
</div>
<div id="flow"
     class="card-value">
0
</div>
</div>

<div class="card">
<div class="card-title">
⚙ Bơm
</div>
<div id="pump"
     class="card-value">
OFF
</div>
</div>

<div class="card">
<div class="card-title">
🛡 Chế độ
</div>
<div id="mode"
     class="card-value">
THỦ CÔNG
</div>
</div>

</div>

<!-- ==========================
AI BOX
========================== -->

<div class="alert-box">

<div id="status">
Khởi động
</div>

<br>

<div id="message">
Đang chờ dữ liệu
</div>

<br>

<div id="recommendation">
Không có đề xuất
</div>

<br>

<div id="timer">
</div>

</div>

<!-- ==========================
CONTROLS
========================== -->

<div id="control" class="controls">

<form action="/run_auto"
      method="post">

<button
class="btn btn-auto">

🤖 Tự động

</button>

</form>

<form action="/pump/on"
      method="post">

<button
class="btn btn-on">

▶ Bật bơm

</button>

</form>

<form action="/pump/off"
      method="post">

<button
class="btn btn-off">

■ Tắt bơm

</button>

</form>

</div>

<!-- ==========================
CHART
========================== -->

<div id="chart" class="chart-container">

<h2>
📊 Biểu đồ thời gian thực
</h2>

<br>

<canvas id="sensorChart"></canvas>

</div>

<!-- ==========================
LOGS
========================== -->

<div id="logs" class="logs">

<h2>
📝 Nhật ký hệ thống
</h2>

<br>

<table>

<tr>

<th>Thời gian</th>

<th>pH</th>

<th>Độ đục</th>

<th>Mực nước</th>

<th>Lưu lượng</th>

<th>Bơm</th>

<th>Trạng thái</th>

</tr>

{% for row in logs %}

<tr>

<td>{{row[0]}}</td>

<td>{{row[1]}}</td>

<td>{{row[2]}}</td>

<td>{{row[3]}}</td>

<td>{{row[4]}}</td>

<td>{{row[5]}}</td>

<td>{{row[6]}}</td>

</tr>

{% endfor %}

</table>

</div>

</div>

<!-- ==========================
CHART JS
========================== -->

<script>

const ctx =
document
.getElementById(
"sensorChart"
);

const sensorChart =
new Chart(ctx, {

type: "line",

data: {

labels: [],

datasets: [

{
label:"pH",
data:[],
borderWidth:3
},

{
label:"Độ đục",
data:[],
borderWidth:3
},

{
label:"Mực nước",
data:[],
borderWidth:3
},

{
label:"Lưu lượng",
data:[],
borderWidth:3
}

]

},

options: {

responsive:true,

animation:false,

scales:{
y:{
beginAtZero:true
}
}

}

});


// ==========================
// UPDATE CHART
// ==========================

function updateChart(d){

let now =
new Date()
.toLocaleTimeString();

sensorChart
.data
.labels
.push(now);

sensorChart
.data
.datasets[0]
.data
.push(d.ph);

sensorChart
.data
.datasets[1]
.data
.push(d.turbidity);

sensorChart
.data
.datasets[2]
.data
.push(d.level);

sensorChart
.data
.datasets[3]
.data
.push(d.flow);


// giữ 30 điểm

if(
sensorChart
.data
.labels
.length > 30
){

sensorChart
.data
.labels
.shift();

sensorChart
.data
.datasets
.forEach(ds=>{
ds.data.shift();
});

}

sensorChart.update();

}


// ==========================
// REFRESH
// ==========================

function refreshData(){

fetch('/api/status')

.then(r=>r.json())

.then(d=>{

document
.getElementById("ph")
.innerText = d.ph;

document
.getElementById("turbidity")
.innerText = d.turbidity;

document
.getElementById("level")
.innerText = d.level;

document
.getElementById("flow")
.innerText = d.flow;

document
.getElementById("pump")
.innerText = d.pump;

document
.getElementById("mode")
.innerText = d.mode;


// status color

let st =
document
.getElementById(
"status"
);

st.innerText =
d.status;

st.className = "";

if(
d.status ==
"AN TOÀN"
){

st.classList.add(
"safe"
);

}
else if(
d.status ==
"CẢNH BÁO"
){

st.classList.add(
"warning"
);

}
else{

st.classList.add(
"danger"
);

}


document
.getElementById(
"message"
)
.innerText =
d.message;


document
.getElementById(
"recommendation"
)
.innerText =
d.recommendation;


document
.getElementById(
"timer"
)
.innerText =
d.timer;


updateChart(d);

});

}


setInterval(
refreshData,
1000
);

refreshData();

</script>
<script>

const sections = document.querySelectorAll(
    "#top,#water,#chart,#control,#logs"
);

const navLinks = document.querySelectorAll(
    ".nav-link"
);

window.addEventListener("scroll", () => {

    let current = "";

    sections.forEach(section => {

        const sectionTop =
            section.offsetTop - 150;

        if (
            pageYOffset >= sectionTop
        ) {
            current = section.getAttribute("id");
        }

    });

    navLinks.forEach(link => {

        link.classList.remove(
            "active"
        );

        if (
            link.getAttribute("href")
            === "#" + current
        ) {

            link.classList.add(
                "active"
            );

        }

    });

});

</script>

</body>
</html>
"""

# ==================================
# DASHBOARD
# ==================================

@app.route("/")
def dashboard():

    auto_logic()

    return render_template_string(
        HTML,
        logs=get_logs()
    )
# ==================================
# SENSOR
# ==================================

@app.route(
    "/sensor",
    methods=["POST"]
)
def sensor():

    raw = request.data.decode(
        errors="ignore"
    )

    print(
        "RX SENSOR:",
        raw
    )

    parse_sensor(raw)

    analyze()

    update_chart_data()

    return "OK"
# ==================================
# PUMP ON
# ==================================

@app.route(
    "/pump/on",
    methods=["POST"]
)
def pump_on():

    global pump_command
    global mode
    global auto_end_time

    mode = "THỦ CÔNG"

    auto_end_time = None

    pump_command = "PUMP_ON"

    return redirect("/")

@app.route("/pump/off", methods=["POST"])
def pump_off():

    global pump_command
    global mode
    global auto_end_time

    print("PUMP OFF CLICKED")

    mode = "THỦ CÔNG"
    auto_end_time = None

    pump_command = "PUMP_OFF"
    sensor_data["pump"] = "OFF"

    return redirect("/")
# ==================================
# AUTO START
# ==================================

@app.route(
    "/run_auto",
    methods=["POST"]
)
def run_auto():

    global mode
    global pump_command
    global auto_end_time

    analyze()

    if recommended_seconds > 0:

        mode = "TỰ ĐỘNG"

        auto_end_time = (
            datetime.now()
            +
            timedelta(
                seconds=
                recommended_seconds
            )
        )

        pump_command = "PUMP_ON"
        sensor_data["pump"] = "ON"

    return redirect("/")
# ==================================
# COMMAND
# ==================================

@app.route("/command")
def command():

    auto_logic()

    return pump_command
# ==================================
# STATUS API
# ==================================

@app.route(
    "/api/status"
)
def api_status():

    auto_logic()

    remaining = 0

    if auto_end_time:

        remaining = int(
            (
                auto_end_time
                -
                datetime.now()
            ).total_seconds()
        )

        if remaining < 0:

            remaining = 0

    return jsonify({

        "ph":
        sensor_data["ph"],

        "turbidity":
        sensor_data["turbidity"],

        "level":
        sensor_data["level"],

        "flow":
        sensor_data["flow"],

        "pump":
        sensor_data["pump"],

        "mode":
        mode,

        "status":
        status_text,

        "message":
        message_text,

        "recommendation":
        (
            f"Đề xuất bơm "
            f"{recommended_seconds} giây"
        )
        if recommended_seconds > 0
        else
        "Không cần bơm",

        "timer":
        (
            f"Tự tắt sau "
            f"{remaining} giây"
        )
        if mode == "TỰ ĐỘNG"
        else ""
    })
# ==================================
# CHART API
# ==================================

@app.route(
    "/api/chart"
)
def chart_api():

    return jsonify(
        chart_history
    )
# ==================================
# AUTO ENGINE
# ==================================

def auto_logic():

    global mode
    global auto_end_time
    global pump_command

    if mode != "TỰ ĐỘNG":
        return

    if auto_end_time is None:
        return

    if datetime.now() >= auto_end_time:

        print("AUTO STOP")

        pump_command = "PUMP_OFF"

        auto_end_time = None

        mode = "THỦ CÔNG"

        sensor_data["pump"] = "OFF"
# ==================================
# MAIN
# ==================================

if __name__ == "__main__":

    init_db()

    print(
        "HYDROPONIC IOT PRO READY"
    )

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )