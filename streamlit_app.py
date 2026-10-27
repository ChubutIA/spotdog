import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="SPOT DOG OS - SergioWeb", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
        header[data-testid="stHeader"] { display: none; }
        .block-container {
            padding-top: 0.3rem !important;
            padding-bottom: 0.3rem !important;
            max-width: 820px !important;
        }
        body, .stApp { background-color: #0b0e14; color: white; }
        iframe { border: none; }
    </style>
""", unsafe_allow_html=True)

html_code = """
<!DOCTYPE html>
<html>
<head>
<script src="https://unpkg.com/mqtt/dist/mqtt.min.js"></script>
<style>
    * { box-sizing: border-box; }
    body {
        background: radial-gradient(circle at top, #1e2530, #0d1015);
        color: #ffffff;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        text-align: center;
        margin: 0;
        padding: 14px 18px;
        border-radius: 14px;
        border: 1px solid #2d3748;
        user-select: none;
    }
    h1 { letter-spacing: 3px; font-size: 20px; margin: 0 0 10px 0; color: #e2e8f0; }

    .conn-bar {
        margin-bottom: 10px;
        display: flex;
        justify-content: center;
        gap: 8px;
        align-items: center;
        flex-wrap: wrap;
        background: rgba(0,0,0,0.35);
        padding: 7px 10px;
        border-radius: 8px;
        border: 1px solid #2d3748;
    }
    select, input {
        background: #1a202c;
        border: 1px solid #4a5568;
        color: #00e5ff;
        padding: 5px 9px;
        border-radius: 6px;
        font-family: monospace;
        font-size: 12px;
    }

    .status-bar {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        border-top: 1px solid #2d3748;
        border-bottom: 1px solid #2d3748;
        padding: 7px 0;
        margin-bottom: 10px;
        gap: 4px;
    }
    .metric-label { font-size: 9px; color: #a0aec0; letter-spacing: 1px; }
    .metric-val { font-size: 13px; font-weight: bold; color: #00e5ff; margin-top: 2px; }

    .section-title {
        font-size: 10px;
        color: #718096;
        letter-spacing: 1.5px;
        margin: 6px 0 5px 0;
        text-transform: uppercase;
    }

    .btn-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 7px;
        margin-bottom: 8px;
    }
    .btn {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.18);
        color: white;
        padding: 7px 5px;
        border-radius: 8px;
        font-weight: bold;
        font-size: 11px;
        cursor: pointer;
        transition: all 0.15s;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 3px;
    }
    .btn:hover, .btn.active-btn {
        background: rgba(0, 229, 255, 0.22);
        border-color: #00e5ff;
        box-shadow: 0 0 10px rgba(0, 229, 255, 0.45);
        transform: scale(0.98);
    }
    .btn-stop {
        background: rgba(245, 101, 101, 0.18);
        border-color: #f56565;
        color: #feb2b2;
    }
    .btn-stop:hover, .btn-stop.active-btn {
        background: rgba(245, 101, 101, 0.4);
        box-shadow: 0 0 12px rgba(245, 101, 101, 0.6);
    }
    .btn-toggle-on {
        border-color: #48bb78;
        color: #9ae6b4;
    }

    .ps-badge {
        font-size: 9px;
        padding: 1px 5px;
        border-radius: 4px;
        background: rgba(0, 0, 0, 0.45);
        border: 1px solid rgba(255, 255, 255, 0.15);
        font-family: monospace;
        color: #cbd5e0;
    }
    .ps-cross { color: #63b3ed; border-color: #63b3ed55; }
    .ps-circle { color: #fc8181; border-color: #fc818155; }
    .ps-square { color: #f687b3; border-color: #f687b355; }
    .ps-triangle { color: #68d391; border-color: #68d39155; }

    .sliders-row {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 10px;
        background: rgba(255,255,255,0.03);
        padding: 7px 12px;
        border-radius: 8px;
        border: 1px solid #2d3748;
        margin-bottom: 10px;
        font-size: 11px;
    }
    .slider-box { display: flex; align-items: center; justify-content: space-between; gap: 6px; }

    .joysticks-container {
        display: flex;
        justify-content: space-around;
        align-items: center;
        margin: 8px 0;
    }
    .joy-wrapper { display: flex; flex-direction: column; align-items: center; }
    .joy-label { font-size: 10px; color: #a0aec0; margin-bottom: 5px; }
    .joystick-zone {
        width: 120px;
        height: 120px;
        border: 2px solid rgba(0, 229, 255, 0.45);
        border-radius: 50%;
        position: relative;
        background: radial-gradient(circle, rgba(0,229,255,0.1) 0%, rgba(0,0,0,0.45) 100%);
        touch-action: none;
    }
    .stick {
        width: 38px;
        height: 38px;
        background: #00e5ff;
        border-radius: 50%;
        position: absolute;
        top: 39px;
        left: 39px;
        box-shadow: 0 0 14px #00e5ff;
        cursor: grab;
    }
    .gamepad-bar {
        margin-top: 6px;
        padding: 6px 10px;
        background: rgba(0, 0, 0, 0.35);
        border: 1px solid #2d3748;
        border-radius: 6px;
        font-size: 11px;
        color: #a0aec0;
    }
</style>
</head>
<body>

    <h1>SPOT DOG OS <span style="font-size:11px; color:#00e5ff;">SERGIOWEB MQTT</span></h1>

    <div class="conn-bar">
        <select id="conn-mode" onchange="toggleConnMode()">
            <option value="mqtt">🌐 Internet MQTT (Datos Móviles / Cualquier Wi-Fi)</option>
            <option value="lan">📡 Wi-Fi Local Directo (Red SergioWeb 192.168.4.1)</option>
        </select>
        <span id="code-wrap" style="font-size:11px; color:#a0aec0;">
            Código: <input type="text" id="remote-code" value="permatrago" style="width:110px;" onchange="reconnectMQTT()">
        </span>
        <input type="text" id="esp-ip" value="192.168.4.1" placeholder="IP Local" style="width:120px; display:none;">
    </div>

    <div class="status-bar">
        <div>
            <div class="metric-label">ESTADO</div>
            <div class="metric-val" id="st-estado">SIN FUERZA</div>
        </div>
        <div>
            <div class="metric-label">MODO</div>
            <div class="metric-val" id="st-modo">MANUAL</div>
        </div>
        <div>
            <div class="metric-label">IMU (R / P)</div>
            <div class="metric-val" id="st-imu">0.0° / 0.0°</div>
        </div>
        <div>
            <div class="metric-label">SONAR (I / D)</div>
            <div class="metric-val" id="st-sonar">200 / 200 cm</div>
        </div>
        <div>
            <div class="metric-label">CONEXIÓN</div>
            <div class="metric-val" id="st-conn" style="color:#ecc94b;">CONECTANDO...</div>
        </div>
    </div>

    <!-- 4 Modos exactos de SergioWeb.ino (modo?m=0..3) -->
    <div class="section-title">Modos de Operación (△ cambia en PS4)</div>
    <div class="btn-grid">
        <button class="btn" id="btn-m0" onclick="sendRaw('modo?m=0', 'btn-m0')">
            <span>🕹️ MANUAL</span>
            <span class="ps-badge ps-square">■ Cuadrado</span>
        </button>
        <button class="btn" id="btn-m1" onclick="sendRaw('modo?m=1', 'btn-m1')">
            <span>🧭 EXPLORAR</span>
            <span class="ps-badge ps-triangle">▲ Modo 1</span>
        </button>
        <button class="btn" id="btn-m2" onclick="sendRaw('modo?m=2', 'btn-m2')">
            <span>👣 SÍGUEME (30cm)</span>
            <span class="ps-badge ps-triangle">▲ Modo 2</span>
        </button>
        <button class="btn" id="btn-m3" onclick="sendRaw('modo?m=3', 'btn-m3')">
            <span>🛡️ GUARDIÁN</span>
            <span class="ps-badge ps-triangle">▲ Modo 3</span>
        </button>
    </div>

    <!-- Acciones exactas de SergioWeb.ino (accion?a=...) -->
    <div class="section-title">Acciones y Estabilización</div>
    <div class="btn-grid">
        <button class="btn" id="btn-pararse" onclick="sendRaw('accion?a=pararse', 'btn-pararse')">
            <span>⚡ DE PIE</span>
            <span class="ps-badge ps-cross">✖ Cruz</span>
        </button>
        <button class="btn btn-stop" id="btn-relajar" onclick="sendRaw('accion?a=relajar', 'btn-relajar')">
            <span>🚨 RELAJAR (STOP)</span>
            <span class="ps-badge ps-circle">● Círculo / PS</span>
        </button>
        <button class="btn" id="btn-nivelar" onclick="sendRaw('accion?a=nivelar', 'btn-nivelar')">
            <span>📐 NIVELAR IMU</span>
            <span class="ps-badge">OPTIONS</span>
        </button>
        <button class="btn btn-toggle-on" id="btn-estab" onclick="toggleEstab()">
            <span id="txt-estab">EQUILIBRIO: SÍ</span>
            <span class="ps-badge">R3 (Stick Der)</span>
        </button>
    </div>

    <!-- Velocidad y Altura + Freno -->
    <div class="sliders-row">
        <div class="slider-box">
            <span>🐢/🐇 <b>Velocidad:</b> <span id="val-vel">7</span> <span class="ps-badge">L1 / R1</span></span>
            <div>
                <button class="btn" style="display:inline; padding:4px 10px;" onclick="changeVel(-1)">-</button>
                <button class="btn" style="display:inline; padding:4px 10px;" onclick="changeVel(1)">+</button>
            </div>
        </div>
        <div class="slider-box">
            <span>📏 <b>Altura:</b> <span id="val-alt">0</span> mm <span class="ps-badge">⬆ / ⬇</span></span>
            <div>
                <button class="btn" style="display:inline; padding:4px 10px;" onclick="changeAlt(-5)">-5</button>
                <button class="btn" style="display:inline; padding:4px 10px;" onclick="changeAlt(5)">+5</button>
            </div>
        </div>
    </div>

    <!-- Joysticks -->
    <div class="joysticks-container">
        <div class="joy-wrapper">
            <div class="joy-label">AVANZAR / RETROCEDER (Stick Izq)</div>
            <div class="joystick-zone" id="zone-left">
                <div class="stick" id="stick-left"></div>
            </div>
        </div>
        <div class="joy-wrapper">
            <div class="joy-label">GIRAR IZQ / DER (Stick Der)</div>
            <div class="joystick-zone" id="zone-right">
                <div class="stick" id="stick-right"></div>
            </div>
        </div>
    </div>

    <div class="gamepad-bar" id="gp-status">
        🎮 DualShock 4: Conectá el mando a tu celular/PC o directo por Bluetooth al ESP32
    </div>

<script>
    // Configuración exacta de SergioWeb.ino
    const MQTT_URI  = "wss://mqtt-ws.buxlab.online:443/mqtt";
    const MQTT_USER = "spotdog";
    const MQTT_PASS = "h78gn28K39uLCMt22eQ7tNxA";
    const MODE_NAMES = ["MANUAL", "EXPLORAR", "SÍGUEME", "GUARDIÁN"];

    let mqttClient = null;
    let moveState = { x: 0, w: 0 };
    let wasMoving = false;
    let curVel = 7;
    let curAlt = 0;
    let curMode = 0;
    let estabOn = true;
    let brakeOn = true;
    const maxDist = 39;

    function getTopics() {
        const code = document.getElementById('remote-code').value.trim().toLowerCase();
        return {
            cmd: `sergioperro/${code}/cmd`,
            state: `sergioperro/${code}/estado`
        };
    }

    function connectMQTT() {
        if (mqttClient) { try { mqttClient.end(true); } catch(e) {} }
        const connEl = document.getElementById('st-conn');
        connEl.innerText = "CONECTANDO...";
        connEl.style.color = "#ecc94b";

        mqttClient = mqtt.connect(MQTT_URI, {
            username: MQTT_USER,
            password: MQTT_PASS,
            clientId: "web-sergio-" + Math.random().toString(16).slice(2, 8),
            keepalive: 15,
            reconnectPeriod: 3000
        });

        mqttClient.on('connect', () => {
            connEl.innerText = "ONLINE (MQTT)";
            connEl.style.color = "#48bb78";
            const t = getTopics();
            mqttClient.subscribe(t.state);
            // Pedir estado inicial al perro para activar el envío periódico (watching)
            mqttClient.publish(t.cmd, "estado");
        });

        mqttClient.on('message', (topic, message) => {
            try {
                const d = JSON.parse(message.toString());
                updateUIFromStatus(d);
            } catch (e) {}
        });

        mqttClient.on('offline', () => {
            if (document.getElementById('conn-mode').value === 'mqtt') {
                connEl.innerText = "SIN SEÑAL";
                connEl.style.color = "#f56565";
            }
        });
    }

    function reconnectMQTT() {
        if (document.getElementById('conn-mode').value === 'mqtt') connectMQTT();
    }

    function updateUIFromStatus(d) {
        if (d.estado) document.getElementById('st-estado').innerText = d.estado;
        if (d.modo !== undefined) {
            curMode = d.modo;
            document.getElementById('st-modo').innerText = MODE_NAMES[d.modo] || "MANUAL";
        }
        if (d.roll !== undefined && d.pitch !== undefined) {
            document.getElementById('st-imu').innerText = `${d.roll.toFixed(1)}° / ${d.pitch.toFixed(1)}°`;
        }
        if (d.dl !== undefined && d.dr !== undefined) {
            document.getElementById('st-sonar').innerText = `${d.dl} / ${d.dr} cm`;
        }
        if (d.vel !== undefined) {
            curVel = d.vel;
            document.getElementById('val-vel').innerText = curVel;
        }
        if (d.alt !== undefined) {
            curAlt = d.alt;
            document.getElementById('val-alt').innerText = curAlt;
        }
        if (d.estab !== undefined) {
            estabOn = d.estab;
            document.getElementById('txt-estab').innerText = estabOn ? "EQUILIBRIO: SÍ" : "EQUILIBRIO: NO";
        }
    }

    connectMQTT();

    // Mantener vivo el canal de estado cada 8 segundos (en SergioWeb.ino REMOTE_IDLE_MS = 10000)
    setInterval(() => {
        if (document.getElementById('conn-mode').value === 'mqtt' && mqttClient && mqttClient.connected) {
            mqttClient.publish(getTopics().cmd, "estado");
        }
    }, 8000);

    function toggleConnMode() {
        const m = document.getElementById('conn-mode').value;
        document.getElementById('code-wrap').style.display = (m === 'mqtt') ? 'inline-block' : 'none';
        document.getElementById('esp-ip').style.display = (m === 'lan') ? 'inline-block' : 'none';
        const connEl = document.getElementById('st-conn');
        if (m === 'lan') {
            connEl.innerText = "MODO WIFI LOCAL";
            connEl.style.color = "#00e5ff";
        } else {
            reconnectMQTT();
        }
    }

    function flashBtn(id) {
        if (!id) return;
        const el = document.getElementById(id);
        if (el) {
            el.classList.add('active-btn');
            setTimeout(() => el.classList.remove('active-btn'), 220);
        }
    }

    // Envía comando exacto en formato SergioWeb.ino ("accion?a=pararse", "mover?x=0.5&w=0", etc.)
    async function sendRaw(cmdStr, btnId) {
        flashBtn(btnId);
        const mode = document.getElementById('conn-mode').value;
        if (mode === 'mqtt') {
            if (mqttClient && mqttClient.connected) {
                mqttClient.publish(getTopics().cmd, cmdStr);
            }
        } else {
            const ip = document.getElementById('esp-ip').value.trim();
            const base = ip.startsWith('http') ? ip : `http://${ip}`;
            try {
                const res = await fetch(`${base}/${cmdStr}`);
                if (res.ok && !cmdStr.startsWith('mover')) {
                    const d = await res.json();
                    updateUIFromStatus(d);
                }
            } catch (e) {}
        }
    }

    function toggleEstab() {
        estabOn = !estabOn;
        sendRaw(estabOn ? 'accion?a=estab_on' : 'accion?a=estab_off', 'btn-estab');
    }

    function changeVel(delta) {
        curVel = Math.min(10, Math.max(2, curVel + delta));
        document.getElementById('val-vel').innerText = curVel;
        sendRaw(`accion?a=vel&v=${curVel}`);
    }

    function changeAlt(delta) {
        curAlt = Math.min(15, Math.max(-40, curAlt + delta));
        document.getElementById('val-alt').innerText = curAlt;
        sendRaw(`accion?a=altura&v=${curAlt}`);
    }

    // --- Joysticks ---
    function setupJoystick(zoneId, stickId, onMove) {
        const zone = document.getElementById(zoneId);
        const stick = document.getElementById(stickId);
        let dragging = false;

        zone.addEventListener('pointerdown', (e) => { dragging = true; update(e); });
        window.addEventListener('pointermove', (e) => { if (dragging) update(e); });
        window.addEventListener('pointerup', () => {
            if (!dragging) return;
            dragging = false;
            stick.style.transform = `translate(0px, 0px)`;
            onMove(0, 0);
            sendRaw(`mover?x=${moveState.x}&w=${moveState.w}`);
        });

        function update(e) {
            const rect = zone.getBoundingClientRect();
            const dx = e.clientX - (rect.left + rect.width / 2);
            const dy = e.clientY - (rect.top + rect.height / 2);
            const dist = Math.min(Math.hypot(dx, dy), maxDist);
            const angle = Math.atan2(dy, dx);
            const px = Math.cos(angle) * dist;
            const py = Math.sin(angle) * dist;
            stick.style.transform = `translate(${px}px, ${py}px)`;
            onMove(+(px / maxDist).toFixed(2), +(-py / maxDist).toFixed(2));
        }
    }

    // En SergioWeb.ino: x = adelante(+), w = giro izquierda(+)
    setupJoystick('zone-left', 'stick-left', ( horizontal, vertical ) => {
        moveState.x = vertical;
        moveState.w = -horizontal;
    });
    setupJoystick('zone-right', 'stick-right', ( horizontal, vertical ) => {
        moveState.w = -horizontal;
    });

    // Envío continuo cada 180 ms mientras se mueve (CMD_TIMEOUT_MS en el ESP32 es 1000 ms)
    setInterval(() => {
        const moving = (Math.abs(moveState.x) > 0.05 || Math.abs(moveState.w) > 0.05);
        if (moving) {
            sendRaw(`mover?x=${moveState.x}&w=${moveState.w}`);
            wasMoving = true;
        } else if (wasMoving) {
            sendRaw(`mover?x=0&w=0`);
            wasMoving = false;
        }
    }, 180);

    // --- Soporte Mando DualShock 4 conectado al Celular / PC ---
    let lastBtn = {};
    window.addEventListener("gamepadconnected", (e) => {
        document.getElementById('gp-status').innerHTML = `🟢 <b>DualShock 4 Activo:</b> ${e.gamepad.id}`;
        requestAnimationFrame(pollGamepad);
    });

    function justPressed(gp, i) {
        const p = gp.buttons[i]?.pressed;
        const prev = lastBtn[i] || false;
        lastBtn[i] = p;
        return p && !prev;
    }

    function pollGamepad() {
        const gp = navigator.getGamepads()[0];
        if (gp) {
            const dz = 0.12;
            let lx = Math.abs(gp.axes[0]) > dz ? +gp.axes[0].toFixed(2) : 0;
            let ly = Math.abs(gp.axes[1]) > dz ? +(-gp.axes[1]).toFixed(2) : 0;
            let rx = Math.abs(gp.axes[2]) > dz ? +gp.axes[2].toFixed(2) : 0;

            moveState.x = ly;
            moveState.w = (rx !== 0) ? -rx : -lx;

            document.getElementById('stick-left').style.transform = `translate(${lx * maxDist}px, ${-ly * maxDist}px)`;
            document.getElementById('stick-right').style.transform = `translate(${rx * maxDist}px, 0px)`;

            // Mismo mapeo exacto que tenés en padButtonsDown() de SergioWeb.ino
            if (justPressed(gp, 0)) sendRaw('accion?a=pararse', 'btn-pararse'); // Cruz (X)
            if (justPressed(gp, 1) || justPressed(gp, 16)) sendRaw('accion?a=relajar', 'btn-relajar'); // Círculo o PS
            if (justPressed(gp, 2)) sendRaw('modo?m=0', 'btn-m0');              // Cuadrado -> Manual
            if (justPressed(gp, 3)) {                                           // Triángulo -> Siguiente modo
                curMode = (curMode + 1) % 4;
                sendRaw(`modo?m=${curMode}`, `btn-m${curMode}`);
            }
            if (justPressed(gp, 4)) changeVel(-1);                              // L1 -> Velocidad -
            if (justPressed(gp, 5)) changeVel(1);                               // R1 -> Velocidad +
            if (justPressed(gp, 9)) sendRaw('accion?a=nivelar', 'btn-nivelar'); // Options -> Nivelar
            if (justPressed(gp, 11)) toggleEstab();                             // R3 -> Equilibrio Sí/No
            if (justPressed(gp, 12)) changeAlt(5);                              // D-Pad Arriba -> Altura +5
            if (justPressed(gp, 13)) changeAlt(-5);                             // D-Pad Abajo -> Altura -5
        }
        requestAnimationFrame(pollGamepad);
    }
</script>
</body>
</html>
"""

components.html(html_code, height=670, scrolling=False)
