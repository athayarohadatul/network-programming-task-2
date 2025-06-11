from socket import socket, AF_INET, SOCK_STREAM
import threading
import logging
from datetime import datetime
import pytz

# ===============================
# TIME SERVER (Port 45000, TCP)
# ===============================
# Menerima perintah "TIME" dan mengembalikan waktu dalam format
# "JAM hh:mm:ss\r\n", sesuai zona waktu Indonesia (Asia/Jakarta).
# Dapat menangani banyak klien secara bersamaan (multithreaded).
# ===============================

class ProcessTheClient(threading.Thread):
    def __init__(self, connection, address):
        threading.Thread.__init__(self, daemon=True)
        self.connection = connection
        self.address = address

    def run(self):
        try:
            while True:
                data = self.connection.recv(1024)
                if not data:
                    break

                # Decode dan strip karakter akhir
                message = data.decode('utf-8').strip()

                if message == "TIME":
                    # ===============================
                    # Mengambil waktu sesuai instruksi soal
                    # dari datetime import datetime
                    # now = datetime.now()
                    # waktu = now.strftime("%d %m %Y %H:%M:%S")
                    # ===============================

                    jakarta_tz = pytz.timezone("Asia/Jakarta")
                    now = datetime.now(jakarta_tz)

                    waktu_lengkap = now.strftime("%d %m %Y %H:%M:%S")  # Untuk log
                    current_time = now.strftime("%H:%M:%S")  # Untuk klien
                    response = f"JAM {current_time}\r\n"

                    # Kirim ke klien
                    self.connection.sendall(response.encode('utf-8'))

                    # Tampilkan di log (bisa jadi screenshot)
                    logging.info(f"Request from {self.address} => TIME")
                    logging.info(f"Log waktu: {waktu_lengkap}")
                    logging.info(f"Response sent: {response.strip()}")

                elif message == "QUIT":
                    logging.info(f"Client {self.address} disconnected.")
                    break
                else:
                    logging.warning(f"Invalid request from {self.address}: {message}")
        except Exception as e:
            logging.error(f"Error with client {self.address}: {e}")
        finally:
            self.connection.close()

class Server(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self, daemon=True)
        self.server_socket = socket(AF_INET, SOCK_STREAM)

    def run(self):
        self.server_socket.bind(('0.0.0.0', 45000))
        self.server_socket.listen(5)

        logging.info("Time Server is running on port 45000...")

        while True:
            conn, addr = self.server_socket.accept()
            logging.info(f"Accepted connection from {addr}")

            client_thread = ProcessTheClient(conn, addr)
            client_thread.start()

def main():
    # Konfigurasi log
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] %(levelname)s: %(message)s',
    )

    # Jalankan server
    server = Server()
    server.start()

    # Jaga thread utama tetap hidup
    try:
        while True:
            pass
    except KeyboardInterrupt:
        logging.info("Server terminated manually.")

if __name__ == "__main__":
    main()
