import os
import requests

from dotenv import load_dotenv


load_dotenv()


def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = False):
    if mock:
        linkedin_profile_url = "https://gist.githubusercontent.com/fullstack-yao/b43adfa6f9a72777389039407ee734c4/raw/886fdf01b64ab06431ee64a0e4620262e7eec3b2/aaron-song.json"
        response = requests.get(linkedin_profile_url, timeout=10)
    else:
        headers = {"Authorization": f'Bearer {os.environ.get("PROXYCURL_API_KEY")}'}
        api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
        params = {
            "url": linkedin_profile_url,
        }
        response = requests.get(
            api_endpoint, params=params, headers=headers, timeout=10
        )

    data = response.json()
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", "", None)
        and k not in ["people_also_viewed", "certifications"]
    }

    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")

    return data


if __name__ == "__main__":
    print(
        scrape_linkedin_profile(
            linkedin_profile_url="https://www.linkedin.com/in/aaron-song-fullstack/",
            mock=True,
        )
    )
