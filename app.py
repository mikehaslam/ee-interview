import os
import requests
from flask import Flask, jsonify, request
from typing import Dict, List, Any

app = Flask(__name__)

GITHUB_API_BASE_URL = os.environ.get("GITHUB_API_BASE_URL", "https://api.github.com")

def get_user_gists(username: str) -> List[Dict[str, Any]]:
    """
    Fetch public gists for a given GitHub user.

    Args:
        username: GitHub username

    Returns:
        List of gist dictionaries containing relevant information
    """
    url = f"{GITHUB_API_BASE_URL}/users/{username}/gists"
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        gists = response.json()

        formatted_gists = []
        for gist in gists:
            formatted_gists.append({
                "id": gist.get("id"),
                "description": gist.get("description"),
                "public": gist.get("public"),
                "html_url": gist.get("html_url"),
                "created_at": gist.get("created_at"),
                "updated_at": gist.get("updated_at"),
                "files": list(gist.get("files", {}).keys())
            })

        return formatted_gists

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            raise ValueError(f"User '{username}' not found")
        raise
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error fetching gists: {str(e)}")


@app.route("/<username>", methods=["GET"])
def get_gists(username: str):
    """
    API endpoint to get public gists for a GitHub user.

    Args:
        username: GitHub username from URL path

    Returns:
        JSON response with gists or error message
    """
    try:
        gists = get_user_gists(username)
        return jsonify({
            "username": username,
            "gist_count": len(gists),
            "gists": gists
        }), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 404

    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500


@app.route("/", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "message": "GitHub Gists API is running. Use /<username> to fetch gists."
    }), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)
