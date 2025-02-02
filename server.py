import os
import smtplib
import requests
from flask import Flask, request, jsonify
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configurations
TMDB_API_KEY = "55b11132b5aef36e8376418dcce756f2"
GMAIL_USER = "titumvposting@gmail.com"
GMAIL_PASSWORD = "zbbkdssscyjmszfy"  # Use App Password (Not Normal Password)
BLOGGER_EMAIL = "asatkarsarvesh39.titu@blogger.com"

# Fetch movie details from TMDb
@app.route("/fetch_movie")
def fetch_movie():
    tmdb_id = request.args.get("tmdb_id")
    
    movie_url = f"https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={TMDB_API_KEY}&language=en-US"
    cast_url = f"https://api.themoviedb.org/3/movie/{tmdb_id}/credits?api_key={TMDB_API_KEY}"
    images_url = f"https://api.themoviedb.org/3/movie/{tmdb_id}/images?api_key={TMDB_API_KEY}"

    movie_response = requests.get(movie_url)
    cast_response = requests.get(cast_url)
    images_response = requests.get(images_url)

    if movie_response.status_code != 200:
        return jsonify({"error": "Movie not found"}), 404
    
    movie_data = movie_response.json()
    cast_data = cast_response.json()
    images_data = images_response.json()

    cast_list = ", ".join([actor["name"] for actor in cast_data["cast"][:5]])
    screenshots = [f"https://image.tmdb.org/t/p/w500{img['file_path']}" for img in images_data["backdrops"][:3]]

    movie_details = {
        "title": movie_data["title"],
        "poster": f"https://image.tmdb.org/t/p/w500{movie_data['poster_path']}",
        "cast": cast_list,
        "release_date": movie_data["release_date"],
        "synopsis": movie_data["overview"],
        "screenshots": screenshots,
        "embed_frame": f'<iframe src="https://vidsrc.icu/embed/movie/{tmdb_id}" width="700" height="400" frameborder="0" allowfullscreen></iframe>'
    }

    return jsonify(movie_details)

# Send Email using Gmail SMTP
@app.route("/send_data", methods=["POST"])
def send_data():
    data = request.json

    email_content = f"""
    <h1>{data['title']}</h1>
    <img src='{data['poster']}' width='200'><br>
    <p><b>Cast:</b> {data['cast']}</p>
    <p><b>Release Date:</b> {data['release_date']}</p>
    <p><b>Synopsis:</b> {data['synopsis']}</p>
    <h3>Screenshots:</h3>
    <div>
        {"".join([f"<img src='{img}' width='150'>" for img in data['screenshots']])}
    </div>
    <h3>Watch Now:</h3>
    {data['embed_frame']}
    """

    try:
        msg = MIMEMultipart()
        msg['From'] = GMAIL_USER
        msg['To'] = BLOGGER_EMAIL
        msg['Subject'] = data["title"]
        msg.attach(MIMEText(email_content, "html"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(GMAIL_USER, GMAIL_PASSWORD)
        server.sendmail(GMAIL_USER, BLOGGER_EMAIL, msg.as_string())
        server.quit()

        return jsonify({"message": "Movie details sent to Blogger!"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
