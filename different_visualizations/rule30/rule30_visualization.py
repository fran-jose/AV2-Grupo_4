from mesa import Model
from mesa.time import SimultaneousActivation
from flask import Flask, render_template_string, jsonify
import matplotlib
matplotlib.use('Agg')  
import matplotlib.pyplot as plt
import io
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

class Rule30Cell:
    def __init__(self, state):
        self.state = state
        self.next_state = 0

    def compute_next_state(self, left, center, right):
        self.next_state = left ^ (center | right)

    def advance(self):
        self.state = self.next_state

class Rule30Model(Model):
    def __init__(self, width=128):
        self.width = width
        self.schedule = SimultaneousActivation(self)
        self.cells = [Rule30Cell(1 if i == width // 2 else 0) for i in range(width)]
        self.steps = []
        self.collect_state()

    def step(self):
        for i in range(self.width):
            left = self.cells[i - 1].state if i > 0 else 0
            center = self.cells[i].state
            right = self.cells[i + 1].state if i < self.width - 1 else 0
            self.cells[i].compute_next_state(left, center, right)
        self.schedule.step()
        for cell in self.cells:
            cell.advance()
        self.collect_state()

    def collect_state(self):
        row = [cell.state for cell in self.cells]
        self.steps.append(row)

app = Flask(__name__)
model = Rule30Model(width=128)
max_steps = 64
step_count = 0

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, plot_png=plot_png())

@app.route('/step')
def step():
    global step_count
    if step_count < max_steps:
        model.step()
        step_count += 1
        return jsonify(success=True)
    else:
        return jsonify(success=False, message="Maximum number of steps reached.")

@app.route('/plot.png')
def plot_png():
    fig, ax = plt.subplots()
    ax.imshow(model.steps, cmap='binary', aspect='auto')
    ax.set_xticks([])
    ax.set_yticks([])
    plt.title("Rule 30 - Current State")
    canvas = FigureCanvas(fig)
    img = io.BytesIO()
    canvas.print_png(img)
    plt.close(fig)
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode('utf8')

HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>Rule 30 Visualization</title>
  </head>
  <body>
    <div style="text-align: center;">
      <h1>Rule 30 Cellular Automaton</h1>
      <img id="rule30-image" src="data:image/png;base64,{{ plot_png }}" alt="Rule 30">
      <br><br>
      <button onclick="nextStep()">Next Step</button>
    </div>
    <script>
      function nextStep() {
        fetch('/step').then(response => response.json()).then(data => {
          if (data.success) {
            updateImage();
          } else {
            alert(data.message);
          }
        });
      }
      function updateImage() {
        fetch('/plot.png').then(response => response.text()).then(data => {
          document.getElementById('rule30-image').src = 'data:image/png;base64,' + data;
        });
      }
    </script>
  </body>
</html>
"""

if __name__ == "__main__":
    app.run(debug=True, port=5000)
