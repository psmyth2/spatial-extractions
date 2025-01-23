import os
import json
import geopandas as gpd
import folium
from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from app.forms import GeoJSONUploadForm

main = Blueprint("main", __name__)

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"geojson"}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Helper function to check file extension
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route("/", methods=["GET", "POST"])
def home():
    form = GeoJSONUploadForm()
    if form.validate_on_submit():
        file = form.file.data
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            # Validate & Convert to GeoDataFrame
            try:
                with open(filepath) as f:
                    geojson_data = json.load(f)

                gdf = gpd.GeoDataFrame.from_features(geojson_data["features"])
                gdf.set_crs("EPSG:4326", inplace=True)

                # Check if geometry column is valid
                if "geometry" not in gdf.columns or gdf.is_empty.any():
                    flash("Invalid GeoJSON: No valid geometries found.", "danger")
                    return redirect(url_for("main.home"))

                # Generate map with Leaflet
                centroid = gdf.geometry.centroid.iloc[0]
                map_object = folium.Map(location=[centroid.y, centroid.x], zoom_start=14)

                # Add polygon(s) to map
                folium.GeoJson(gdf.to_json(), name="Uploaded Polygon").add_to(map_object)

                # Save map
                map_html = map_object._repr_html_()

                return render_template("confirm.html", map_html=map_html, gdf=gdf.to_json())

            except Exception as e:
                flash(f"Error processing GeoJSON: {str(e)}", "danger")
                return redirect(url_for("main.home"))
    
    return render_template("upload.html", form=form)


@main.route("/process", methods=["POST"])
def process_geojson():
    try:
        geojson_data = request.form.get("geojson_data")
        if not geojson_data:
            flash("No valid GeoJSON received.", "danger")
            return redirect(url_for("main.home"))

        gdf = gpd.read_file(json.loads(geojson_data))

        flash("GeoJSON confirmed successfully!", "success")
        return redirect(url_for("main.home"))

    except Exception as e:
        flash(f"Error processing GeoJSON: {str(e)}", "danger")
        return redirect(url_for("main.home"))
