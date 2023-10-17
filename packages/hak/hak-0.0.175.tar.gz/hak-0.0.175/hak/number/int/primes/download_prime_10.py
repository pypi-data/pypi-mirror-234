from requests import get as requests_get
# download_prime_10
def f():
  url = "http://www.prime-numbers.org/free/prime10.zip"
  file_name = "prime10.zip"
  chunk_size = 8192  # Size of each chunk in bytes

  response = requests_get(url, stream=True)

  if response.status_code == 200:
    total_size = int(response.headers.get("Content-Length", 0))
    downloaded_size = 0

    with open(file_name, "wb") as file:
      for chunk in response.iter_content(chunk_size=chunk_size):
        file.write(chunk)
        downloaded_size += len(chunk)
        progress = (downloaded_size / total_size) * 100
        print(
          f"Downloaded {downloaded_size}/{total_size} bytes ({progress:.2f}%)",
          end="\r"
        )

    print(f"\nDownloaded {file_name} successfully.")
  else:
    print("Failed to download the file.")

t = lambda: True # TODO: Fix this test
