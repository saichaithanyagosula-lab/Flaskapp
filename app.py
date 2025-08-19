from flask import Flask, render_template, Response
import datetime

app = Flask(__name__)


# -----------------
# Normal Routes
# -----------------
@app.route("/")
def home():
    return render_template("index.html")


# -----------------
# Sitemap (auto-generate)
# -----------------
@app.route("/sitemap.xml", methods=["GET"])
def sitemap():
    pages = []
    base_url = "https://flaskapp-rxvd.onrender.com"  # your Render site URL
    lastmod = datetime.date.today().isoformat()

    for rule in app.url_map.iter_rules():
        if "GET" in rule.methods and len(rule.arguments) == 0:
            url = base_url + str(rule.rule)
            pages.append(
                f"""
            <url>
                <loc>{url}</loc>
                <lastmod>{lastmod}</lastmod>
                <changefreq>weekly</changefreq>
                <priority>1.0</priority>
            </url>"""
            )

    sitemap_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
        {''.join(pages)}
    </urlset>"""

    return Response(sitemap_xml, mimetype="application/xml")


# -----------------
# Robots.txt
# -----------------
@app.route("/robots.txt")
def robots():
    robots_txt = """User-agent: *
Allow: /

Sitemap: https://flaskapp-rxvd.onrender.com/sitemap.xml
"""
    return Response(robots_txt, mimetype="text/plain")


if __name__ == "__main__":
    app.run(debug=True)
