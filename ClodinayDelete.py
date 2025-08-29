import cloudinary
import cloudinary.api

cloudinary.config(
  cloud_name="dh9xmgxbx",
  api_key="596816732371556",
  api_secret="5POuYbUpWJrThldnJixbdd3daXM"
)

# 🚨 This will delete *all* images
cloudinary.api.delete_all_resources(resource_type="image")

# 🚨 This will delete *all* videos
cloudinary.api.delete_all_resources(resource_type="video")


