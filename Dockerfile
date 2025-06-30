FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    build-essential \
    libncurses5 \
    libncurses5-dev \
    libbz2-1.0 \
    && rm -rf /var/lib/apt/lists/*

ENV BLAST_VERSION=2.16.0
ENV BLAST_TAR=ncbi-blast-${BLAST_VERSION}+-x64-linux.tar.gz

# Descarga y extrae BLAST+ en /opt
RUN wget https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/${BLAST_VERSION}/${BLAST_TAR} \
    && tar -xzf ${BLAST_TAR} -C /opt \
    && rm ${BLAST_TAR}

# Aquí detectamos la carpeta exacta (la que comienza con ncbi-blast-2.16.0+)
RUN BLAST_DIR=$(ls /opt | grep ncbi-blast-${BLAST_VERSION}+) && echo "Blast dir is $BLAST_DIR" && \
    ln -s /opt/$BLAST_DIR /opt/ncbi-blast

ENV PATH=/opt/ncbi-blast/bin:$PATH

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
