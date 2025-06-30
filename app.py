from flask import Flask, request, render_template_string
from blast_script import procesar_archivos  # tu función modular

app = Flask(__name__)

HTML = """
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>BLAST Local con Flask</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet" />
  <style>
    body { padding-top: 40px; background: #f8f9fa; }
    .container {
      max-width: 900px;
      background: white;
      padding: 30px;
      border-radius: 10px;
      box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    }
  </style>
</head>
<body>
  <div class="container">
    <h1 class="mb-4 text-center">BLAST Local con Flask</h1>
    <form method="post" enctype="multipart/form-data" class="mb-4">
      <div class="mb-3">
        <label for="seqfiles" class="form-label">Sube uno o más archivos <code>.seq</code></label>
        <input
          class="form-control"
          type="file"
          id="seqfiles"
          name="seqfiles"
          multiple
          required
          accept=".seq,text/plain"
        />
      </div>
      <button type="submit" class="btn btn-primary w-100">Ejecutar BLAST</button>
    </form>

    {% if resultados %}
      <h3>Resultados:</h3>
      <table class="table table-striped table-bordered">
        <thead class="table-dark">
          <tr>
            <th>Archivo</th>
            <th>Identidad (%)</th>
            <th>Longitud</th>
            <th>E-value</th>
            <th>Descripción</th>
            <th>Error</th>
          </tr>
        </thead>
        <tbody>
          {% for r in resultados %}
            <tr>
              <td>{{ r.archivo }}</td>
              <td>{{ r.pident if r.pident is defined else '' }}</td>
              <td>{{ r.length if r.length is defined else '' }}</td>
              <td>{{ r.evalue if r.evalue is defined else '' }}</td>
              <td>{{ r.stitle if r.stitle is defined else '' }}</td>
              <td>{{ r.error if r.error is defined else '' }}</td>
            </tr>
          {% endfor %}
        </tbody>
      </table>
    {% elif resultados is not none %}
      <div class="alert alert-info">No se encontraron resultados.</div>
    {% endif %}
  </div>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    resultados = None
    if request.method == "POST":
        if "seqfiles" not in request.files:
            resultados = []
        else:
            files = request.files.getlist("seqfiles")
            if not files or files[0].filename == "":
                resultados = []
            else:
                resultados = procesar_archivos(files)
    return render_template_string(HTML, resultados=resultados)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
