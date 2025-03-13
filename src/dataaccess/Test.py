from UserCRUD import *
from DataCon import *
from ImageCRUD import *
import bcrypt

conn = get_connection()

password = b'password'
# Adding the salt to password
salt = bcrypt.gensalt()
# Hashing the password
hashed = bcrypt.hashpw(password, salt)
#create_user(conn, "admin", hashed,salt,2)
#create_user(conn, "jane_doe", hashed,salt,1)
#create_user(conn, "anne2000", hashed,salt,1)
#create_user(conn, "emily_smith", hashed,salt,1)
        
#create_user(conn, "olivia2345", hashed,salt,1)
# Update user information
#update_user(conn, 1, username="new_user", usertype_id=1)
        
# Delete a user
#delete_user(conn, 8)


data = read_user(conn)
print(data)


# Create an image
"""
create_image(conn, user_id=14, image_name="/static/images/0e33f6a8-bb73-4267-adae-633dc7236c5e.jpg",uploadDate="2024-06-10")
create_image(conn, user_id=14, image_name="/static/image/0efcb1c8-fefa-4690-b1ca-eb2fc2549d46.jpg",uploadDate="2024-06-20")
create_image(conn, user_id=14, image_name="/static/images/1c2b32ac-ef8c-467c-a59c-ae24b55c8ed5.jpg",uploadDate="2024-07-13")
create_image(conn, user_id=14, image_name="/static/images/1da3941c-82ef-4e84-86fb-48c160635867.jpg",uploadDate="2024-08-05")
create_image(conn, user_id=14, image_name="/static/images/2b99b561-63e9-454f-b10c-25072839f5d4.jpg",uploadDate="2024-08-21")
create_image(conn, user_id=14, image_name="/static/images/2f520ff6-ebc4-4cad-af76-6647a6e9d712.jpg",uploadDate="2024-09-15")
create_image(conn, user_id=14, image_name="/static/images/3dd6a14e-14e7-4904-8862-d702d8167af0.jpg",uploadDate="2024-10-07")
create_image(conn, user_id=14, image_name="/static/images/3eb14a1b-8187-4ed0-ab80-a0154c927ea1.jpg",uploadDate="2024-10-18")
create_image(conn, user_id=14, image_name="/static/images/3f4a47d7-2868-4ba8-b31c-dcbf21f8b863.jpg",uploadDate="2024-11-15")
create_image(conn, user_id=14, image_name="/static/images/4a0fa32b-f13e-45af-a3da-248cd5a89e09.jpg",uploadDate="2024-11-25")
create_image(conn, user_id=14, image_name="/static/images/4bbab4bb-d25e-4d81-8ec6-f3de01354bd5.jpg",uploadDate="2024-12-09")


create_image(conn, user_id=15, image_name="/static/images/7cf4357a-5588-451a-bbcf-d916639b86d3.jpg",uploadDate="2024-09-26")
create_image(conn, user_id=15, image_name="/static/images/7d8fb834-588b-4d17-8a9f-c89dfa7e5919.jpg",uploadDate="2024-10-18")
create_image(conn, user_id=15, image_name="/static/images/9bd29934-f695-4005-91ca-79bde4a0627f.jpg",uploadDate="2024-10-07")
create_image(conn, user_id=15, image_name="/static/images/34dee898-ac0a-4ba2-bc46-7e25c637bc69.jpg",uploadDate="2024-11-12")
create_image(conn, user_id=15, image_name="/static/images/048a5604-bad8-49e8-9965-967ff76f82ef.jpg",uploadDate="2024-11-20")
create_image(conn, user_id=15, image_name="/static/images/55e77bb8-b679-4e83-ba34-19fb6b7ec009.jpg",uploadDate="2024-12-10")

create_image(conn, user_id=16, image_name="/static/images/f2221847-17aa-4927-8728-5a06d6341d84.jpg",uploadDate="2024-12-09")
create_image(conn, user_id=16, image_name="/static/images/ef886a0d-9646-4b08-92f7-0ca3626161aa.jpg",uploadDate="2024-12-11")
"""

# Update image information
#update_image(conn, image_id=1, crystals=0)

# Delete an image
#delete_image(conn, image_id=5)

#data = read_image(conn)
#print(data)

close_connection(conn)