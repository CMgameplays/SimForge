from flask import Flask, render_template, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "60 per hour"],
    storage_uri="memory://",
)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/simulate", methods=["POST"])
@limiter.limit("30 per minute")
def simulate():
    data = request.get_json(force=True)

    try:
        wave_count     = int(data.get("wave_count", 10))
        player_hp      = float(data.get("player_hp", 100))
        player_dps     = float(data.get("player_dps", 50))
        player_scale   = float(data.get("player_scale", 10))   # % per wave
        enemy_hp       = float(data.get("enemy_hp", 80))
        enemy_damage   = float(data.get("enemy_damage", 20))
        enemy_scale    = float(data.get("enemy_scale", 15))    # % per wave
    except (TypeError, ValueError) as e:
        return jsonify({"error": f"Invalid input: {e}"}), 400

    # Clamp wave count
    wave_count = max(5, min(50, wave_count))

    waves            = list(range(1, wave_count + 1))
    player_power     = []
    enemy_difficulty = []

    for w in waves:
        # Player power = base_dps * (1 + scale_pct/100)^wave
        pp = player_dps * (1 + player_scale / 100) ** w
        player_power.append(round(pp, 4))

        # Enemy difficulty = base_hp * (1 + enemy_scale_pct/100)^wave
        ed = enemy_hp * (1 + enemy_scale / 100) ** w
        enemy_difficulty.append(round(ed, 4))

    danger_waves  = [w for w, pp, ed in zip(waves, player_power, enemy_difficulty) if ed > pp]
    trivial_waves = [w for w, pp, ed in zip(waves, player_power, enemy_difficulty) if pp > ed * 2]

    return jsonify({
        "waves":            waves,
        "player_power":     player_power,
        "enemy_difficulty": enemy_difficulty,
        "danger_waves":     danger_waves,
        "trivial_waves":    trivial_waves,
    })


if __name__ == "__main__":
    app.run(debug=True)
