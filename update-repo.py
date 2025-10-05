import xml.etree.ElementTree as ET
import json
import requests

FDROID_INDEX_URL = "https://f-droid.org/repo/index.xml"
FDROID_APK_BASE = "https://f-droid.org/repo/"

def fetch_index():
    response = requests.get(FDROID_INDEX_URL)
    response.raise_for_status()
    return ET.fromstring(response.content)

def extract_apps(xml_root):
    apps = []

    for app in xml_root.findall("application"):
        pkg_id = app.attrib.get("id")
        name_elem = app.find("name")
        name = name_elem.text if name_elem is not None else pkg_id

        summary_elem = app.find("summary")
        summary = summary_elem.text if summary_elem is not None else ""

        packages = app.findall("package")
        if not packages:
            continue

        latest = packages[-1]
        apkname = latest.findtext("apkname")
        if not apkname:
            continue

        apk_url = f"{FDROID_APK_BASE}{apkname}"

        apps.append({
            "name": name,
            "description": summary,
            "apk": apk_url
        })

    return apps

def save_manifest(apps, filename="manifest.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(apps, f, indent=2, ensure_ascii=False)

def main():
    print("Downloading index.xml...")
    xml_root = fetch_index()
    print("Extracting applications...")
    apps = extract_apps(xml_root)
    print(f"Found {len(apps)} applications")
    print("Saving manifest.json...")
    save_manifest(apps)
    print("Done!")

if __name__ == "__main__":
    main()

