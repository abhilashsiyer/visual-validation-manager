from imagekitio import ImageKit


def upload_image(image, name):
    imagekit = ImageKit(
        private_key='private_Gufvw5TqIpJXCHLXsflAmIhjsJU=',
        public_key='public_T79KXeQeARDMxvGEm70zJ2Zk6FY=',
        url_endpoint='https://ik.imagekit.io/it41uxh5d'
    )
    upload = imagekit.upload(
        file=open(image, "rb"),
        file_name=name,
        options={
            "response_fields": ["is_private_file", "tags"],
            "tags": ["tag-"+name]
        },
    )

    # upload = imagekit.upload(
    #     file=open("Q_Galaxy.png", "rb"),
    #     file_name="Q_Galaxy.jpg",
    #     options={
    #         "response_fields": ["is_private_file", "tags"],
    #         "tags": ["tag1", "tag2"]
    #     },
    # )

    print("Upload response", upload['response'])

    downloadURL = upload['response']['url']

    return downloadURL;
