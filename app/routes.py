import os
import json
import time
import geopandas as gpd
import folium
import threading
from flask import Blueprint, render_template, request, redirect, url_for, flash, Response, stream_with_context, jsonify
from werkzeug.utils import secure_filename
from app.forms import GeoJSONUploadForm
from extractions.extractions import Extractions
from extractions.extraction_cleaning import ExtractionCleaning
from openai_summary.summarize import Summarize

main = Blueprint("main", __name__)

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"geojson"}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Store extraction results temporarily
extraction_results = {}

# Helper function to check file extension


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@main.route("/", methods=["GET", "POST"])
def home():
    form = GeoJSONUploadForm()  # Create a form instance
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
                map_object = folium.Map(
                    location=[centroid.y, centroid.x], zoom_start=14)
                folium.GeoJson(
                    gdf.to_json(), name="Uploaded Polygon").add_to(map_object)

                map_html = map_object._repr_html_()

                # ✅ Pass form to template
                return render_template("confirm.html", form=form, map_html=map_html, gdf=gdf.to_json())

            except Exception as e:
                flash(f"Error processing GeoJSON: {str(e)}", "danger")
                return redirect(url_for("main.home"))

    return render_template("upload.html", form=form)


def perform_extraction(geojson_data, session_id):
    """Runs extraction in a separate thread and stores results."""
    global extraction_results
    try:
        gdf = gpd.GeoDataFrame.from_features(geojson_data["features"])
        gdf.set_crs("EPSG:4326", inplace=True)

        extractors = Extractions(gdf)
        spatial_attributes_df = extractors.extract_reference_layers()

        cleaners = ExtractionCleaning(spatial_attributes_df)
        extracted_attributes = cleaners.clean_data()
        summarizer = Summarize(extracted_attributes)
        summary = summarizer.get_response()

        extracted_attributes["summary"] = summary
        extraction_results[session_id] = extracted_attributes
    except Exception as e:
        extraction_results[session_id] = {
            "error": f"Extraction failed: {str(e)}"}


@main.route("/process", methods=["POST"])
def process_geojson():
    """Starts the extraction process and redirects to the processing page."""
    geojson_data = request.form.get("geojson_data")
    if not geojson_data:
        flash("No valid GeoJSON received.", "danger")
        return redirect(url_for("main.home"))

    geojson_data = json.loads(geojson_data)
    session_id = str(int(time.time()))  # Unique ID for session tracking

    # Run extraction in a separate thread
    thread = threading.Thread(
        target=perform_extraction, args=(geojson_data, session_id))
    thread.start()

    return redirect(url_for("main.processing", session_id=session_id))


@main.route("/processing/<session_id>")
def processing(session_id):
    """Renders the processing page with live logs."""
    return render_template("processing.html", session_id=session_id)


@main.route("/logs")
def stream_logs():
    """Ensures the log file exists before streaming logs in real-time."""

    log_dir = "/app/logs"
    log_file_path = os.path.join(log_dir, "extraction.log")

    # ✅ Ensure the log file exists
    if not os.path.exists(log_file_path):
        with open(log_file_path, "w") as f:
            f.write("Log started...\n")

    def generate():
        with open(log_file_path, "r") as log_file:
            log_file.seek(0, 2)  # Move to end of file
            while True:
                line = log_file.readline().strip()
                if line:
                    yield f"data: {line}\n\n"
                time.sleep(0.5)  # Prevents CPU overuse

    return Response(
        stream_with_context(generate()),
        content_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no"
        }
    )


@main.route("/check-status/<session_id>")
def check_status(session_id):
    """Checks if extraction is complete and returns status."""
    if session_id in extraction_results:
        return jsonify({"done": True})
    return jsonify({"done": False})


@main.route("/summary/<session_id>")
def summary(session_id):
    """Displays extracted attributes after processing is complete."""
    extracted_attributes = extraction_results.pop(session_id, {})

    # Ensure 'summary' key exists to avoid template errors
    extracted_attributes.setdefault("summary", "No summary available.")

    filepath = os.path.join(UPLOAD_FOLDER, 'test.geojson')

    with open(filepath) as f:
        geojson_data = json.load(f)

    gdf = gpd.GeoDataFrame.from_features(geojson_data["features"])
    gdf.set_crs("EPSG:4326", inplace=True)

    # Generate map with Leaflet
    centroid = gdf.geometry.centroid.iloc[0]
    map_object = folium.Map(location=[centroid.y, centroid.x], zoom_start=14)
    folium.GeoJson(gdf.to_json(), name="Uploaded Polygon").add_to(map_object)

    map_html = map_object._repr_html_()

    return render_template("summary.html", extracted_attributes=extracted_attributes, map_html=map_html)
