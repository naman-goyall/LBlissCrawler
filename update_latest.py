import json

# Simulate a slightly different video title to trigger the new video detection
updated_video = {
    "title": "Manjhli Didi update test",
    "url": "https://player.vimeo.com/video/1068102517?h=67c46fc47f&badge=0&autopause=0&player_id=0&app_id=58479"
}

# Write to the latest_video.json file
with open("latest_video.json", "w") as file:
    json.dump(updated_video, file)
    
print("Updated latest_video.json to trigger new video detection.")
