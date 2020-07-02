"""
Download editage lecture.
https://e.vhall.com/user/home/47261161
Download flash video stream with Chrome extension "Stream Recorder".
Download PPT image with this module.
Use development tool of Chrome to get prefix of images' url.
Open "Network" tab in development tool and refresh webpage.
Find url of any PPT image, it may be like
`https://cnstatic01.e.vhall.com/document/`
`25ad80b5705dd1f08dbcf6cd41838dce/data/img7.png`
The string before "data" is the prefix of url.
All PPT images are named as `1.jpg`, `2.jpg`, ...
So the url of the first PPT image is
`https://cnstatic01.e.vhall.com/document/`
`25ad80b5705dd1f08dbcf6cd41838dce/1.jpg`
"""
import requests
import shutil


def download_img_series(url_prefix, num, fmt, save_dir):
    for i in range(num):
        # Set up the image URL and filename
        url = f'{url_prefix}{i+1}.{fmt}'
        download_img(url, save_dir)


def download_img(url, save_dir):
    filename = url.split("/")[-1]
    # Open the url image, set stream to True, this will return the
    # stream content.
    r = requests.get(url, stream=True)

    # Check if the image was retrieved successfully
    if r.status_code == 200:
        # Set decode_content value to True, otherwise the downloaded
        # image file's size will be zero.
        r.raw.decode_content = True
        # Open a local file with wb ( write binary ) permission.
        with open(f'{save_dir}{filename}', 'wb') as f:
            shutil.copyfileobj(r.raw, f)

        print('Image sucessfully Downloaded: ', filename)
    else:
        print('Image Couldn\'t be retreived: ', filename)


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--url_prefix", type=str, default="")
    parser.add_argument("--save_dir", type=str, default="./")
    parser.add_argument("--fmt", type=str, default="")
    parser.add_argument("--num", type=int, default=1)

    args = parser.parse_args()

    download_img_series(args.url_prefix, args.num, args.fmt,
                        args.save_dir)


if __name__ == "__main__":
    main()
