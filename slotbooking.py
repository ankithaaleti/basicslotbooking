from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import db
class SlotServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            conn = db.connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM slots WHERE is_booked = FALSE")
            slots = cursor.fetchall()
            conn.close()
            html = "<h2>Available Slots</h2>"
            for s in slots:
                html += f"{s[1]} <a href='/book?id={s[0]}'>Book</a><br>"
            html += "<br><a href='/bookings'>View Bookings</a>"
            self.send_response(200)
            self.send_header("Content-type","text/html")
            self.end_headers()
            self.wfile.write(html.encode())
        elif self.path.startswith("/book?id="):
            slot_id = self.path.split("=")[1]
            html = f"""
            <h2>Book Slot</h2>
            <form method='POST' action='/book'>
            <input type='hidden' name='slot_id' value='{slot_id}'>
            Name: <input type='text' name='name'>
            <button type='submit'>Book</button>
            </form>
            """
            self.send_response(200)
            self.send_header("Content-type","text/html")
            self.end_headers()
            self.wfile.write(html.encode())
        elif self.path == "/bookings":
            conn = db.connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM slots WHERE is_booked=TRUE")
            rows = cursor.fetchall()
            conn.close()
            html = "<h2>Booked Slots</h2>"
            for r in rows:
                html += f"{r[1]} - {r[3]}<br>"
            html += "<br><a href='/'>Back</a>"
            self.send_response(200)
            self.send_header("Content-type","text/html")
            self.end_headers()
            self.wfile.write(html.encode())
    def do_POST(self):
        if self.path == "/book":
            length = int(self.headers['Content-Length'])
            data = self.rfile.read(length).decode()
            params = urllib.parse.parse_qs(data)
            name = params['name'][0]
            slot_id = params['slot_id'][0]
            conn = db.connect_db()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE slots SET is_booked=TRUE, booked_by=%s WHERE id=%s",
                (name, slot_id)
            )
            conn.commit()
            conn.close()
            self.send_response(302)
            self.send_header('Location','/bookings')
            self.end_headers()
def run():
    server = HTTPServer(("localhost",8000), SlotServer)
    print("Server running on http://localhost:8000")
    server.serve_forever()
run()
