function showTab(tabId) {
    // Hide all tabs
    document.querySelectorAll('.tab').forEach(tab => {
        tab.style.display = 'none';
    });

    // Show the selected tab
    document.getElementById(tabId).style.display = 'block';
}

// Show the first tab (upload)
document.addEventListener('DOMContentLoaded', function() {
    showTab('upload-tab');
});

document.getElementById("submit-video").addEventListener("click", function() {
    let file = document.getElementById("video-input").files[0];

    if (!file) {
        alert("Please upload a video first!");
        return;
    }

    let formData = new FormData();
    formData.append("file", file);

    // Show loading spinner
    document.getElementById("loading-spinner").style.display = "block";  // Assuming you have a spinner with this id

    fetch("http://127.0.0.1:5000/upload", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("loading-spinner").style.display = "none";  // Hide spinner when processing is done
        if (data.success) {
            let videoUrl = data.video_url;
            document.getElementById("video-preview").src = videoUrl;
            document.getElementById("video-preview").style.display = "block";
            alert("Video uploaded and processed successfully!");
        } else {
            alert("Error processing the video: " + data.message);
        }
    })
    .catch(error => {
        document.getElementById("loading-spinner").style.display = "none";  // Hide spinner on error
        console.error("Error:", error);
        alert("Error uploading video.");
    });
});
