import os
import subprocess
import tempfile
import shutil

base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, "db", "16S_ribosomal_RNA")
blastn_path = shutil.which("blastn")  # Cambia si es necesario
if blastn_path is None:
    raise RuntimeError("blastn no encontrado en PATH")
def blast_local(fasta_path, db_path, out_path, threads=7):
    cmd = [
        blastn_path,
        "-query", fasta_path,
        "-db", db_path,
        "-out", out_path,
        "-outfmt", "6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore stitle",
        "-max_target_seqs", "1",
        "-num_threads", str(threads)
    ]
    try:
        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar blastn: {e}")
        return False

def leer_middle_de_archivo(path):
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()
    sequence = "".join(line.strip().lower() for line in lines[1:])
    if len(sequence) < 100:
        print(f"⚠️ {path} es demasiado corta ({len(sequence)} bases), se omite.")
        return None
    return sequence[50:-50]

def parse_blast_output(out_txt, filename):
    resultados = []
    with open(out_txt, encoding="utf-8") as f:
        lines = f.readlines()
    for line in lines:
        cols = line.strip().split("\t")
        if len(cols) >= 13:
            resultados.append({
                "archivo": filename,
                "qseqid": cols[0],
                "sseqid": cols[1],
                "pident": cols[2],
                "length": cols[3],
                "mismatch": cols[4],
                "gapopen": cols[5],
                "qstart": cols[6],
                "qend": cols[7],
                "sstart": cols[8],
                "send": cols[9],
                "evalue": cols[10],
                "bitscore": cols[11],
                "stitle": cols[12],
            })
    return resultados

def procesar_archivos(files):
    resultados_totales = []
    with tempfile.TemporaryDirectory() as tmpdir:
        for i, file in enumerate(files, 1):
            filename = file.filename
            input_path = os.path.join(tmpdir, filename)
            file.save(input_path)

            secuencia_middle = leer_middle_de_archivo(input_path)
            if secuencia_middle is None:
                continue

            temp_fasta = os.path.join(tmpdir, f"{filename}_middle.fasta")
            with open(temp_fasta, "w", encoding="utf-8") as f:
                f.write(f">{filename}_middle\n{secuencia_middle}\n")

            out_txt = os.path.join(tmpdir, f"{filename}_blast.txt")
            ok = blast_local(temp_fasta, db_path, out_txt, threads=7)

            if ok:
                blast_result = parse_blast_output(out_txt, filename)
                resultados_totales.extend(blast_result)
            else:
                # Si error en BLAST, se añade una fila con error
                resultados_totales.append({
                    "archivo": filename,
                    "error": "Error en BLAST"
                })
    return resultados_totales
