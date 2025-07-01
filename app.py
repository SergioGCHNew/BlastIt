from flask import Flask, request, render_template_string
from blast_script import procesar_archivos  # tu función modular

app = Flask(__name__)

HTML = """
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Blast It</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet" />
  <style>
    body {
      padding-top: 50px;
      background: linear-gradient(135deg, #667eea, #764ba2);
      min-height: 100vh;
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      color: #333;
    }

    .container {
      max-width: 900px;
      background: #fff;
      padding: 30px 20px;
      border-radius: 15px;
      box-shadow: 0 12px 30px rgba(102, 126, 234, 0.3);
    }

    h1 {
      font-weight: 700;
      font-size: 2.2rem;
      color: #5a4cae;
      margin-bottom: 1.5rem;
      text-align: center;
      text-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }

    label.form-label {
      font-weight: 600;
      font-size: 1rem;
      color: #5a4cae;
      margin-bottom: 0.5rem;
    }

    button.btn-primary {
      background: linear-gradient(90deg, #667eea, #764ba2);
      border: none;
      font-weight: 600;
      font-size: 1.1rem;
      padding: 12px 0;
      transition: background 0.3s ease;
      border-radius: 8px;
    }

    button.btn-primary:hover {
      background: linear-gradient(90deg, #5a4cae, #5e3b8a);
      box-shadow: 0 4px 15px rgba(102, 126, 234, 0.5);
    }

    table {
      border-radius: 10px;
      overflow: hidden;
      box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
      font-size: 0.9rem;
    }

    thead.table-dark {
      background: linear-gradient(90deg, #5a4cae, #764ba2);
      color: #fff;
      font-weight: 600;
    }

    tbody tr:hover {
      background-color: #f0e9ff;
      transition: background-color 0.25s ease;
    }

    .alert-info {
      background-color: #e0e7ff;
      color: #4f46e5;
      font-weight: 600;
      text-align: center;
      border-radius: 8px;
      padding: 15px;
      box-shadow: 0 4px 10px rgba(102, 126, 234, 0.2);
      margin-top: 20px;
    }

    input[type="file"] {
      cursor: pointer;
      border-radius: 8px;
      border: 1px solid #ccc;
      padding: 8px 12px;
      transition: border-color 0.3s ease;
    }

    input[type="file"]:focus {
      outline: none;
      border-color: #764ba2;
      box-shadow: 0 0 5px #764ba2;
    }

    @media (max-width: 576px) {
      .container {
        padding: 25px 15px;
      }

      h1 {
        font-size: 1.8rem;
      }

      table, thead, tbody, th, td, tr {
        display: block;
      }

      thead {
        display: none;
      }

      tbody td {
        padding: 8px 0;
        text-align: right;
        position: relative;
        padding-left: 50%;
      }

      tbody td::before {
        content: attr(data-label);
        position: absolute;
        left: 15px;
        width: 45%;
        padding-right: 10px;
        white-space: nowrap;
        font-weight: 600;
        color: #5a4cae;
        text-align: left;
      }
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>Blast It</h1>
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
      <h3 class="mb-3" style="color: #5a4cae;">Resultados:</h3>
      <table class="table table-striped table-bordered align-middle">
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
              <td data-label="Archivo">{{ r.archivo }}</td>
              <td data-label="Identidad (%)">{{ r.pident if r.pident is defined else '' }}</td>
              <td data-label="Longitud">{{ r.length if r.length is defined else '' }}</td>
              <td data-label="E-value">{{ r.evalue if r.evalue is defined else '' }}</td>
              <td data-label="Descripción">{{ r.stitle if r.stitle is defined else '' }}</td>
              <td data-label="Error">{{ r.error if r.error is defined else '' }}</td>
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
