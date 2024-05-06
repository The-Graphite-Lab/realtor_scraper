from modal import Stub, Image, Mount

pandas_image = Image.debian_slim().pip_install(
    "pandas", "requests", "tls_client",)


stub = Stub("imcm-scraper", image=pandas_image)

# For some reason, the modal pip mirror could not pull the package itself so I had to take the source code and mount it locally
@stub.function(mounts=[Mount.from_local_dir("./homeharvest", remote_path="/root/homeharvest")])
def get_addresses(location, listing_type):
    from pandas import DataFrame
    from homeharvest import scrape_property
    try:
        addresseses: DataFrame = scrape_property(
            # site_name=[site_name],
            past_days=365,
            location=location,
            listing_type=listing_type  # for_sale / sold
        )
    except Exception as e:
        print(f"Error on {location} with {listing_type}: {e}")
        return DataFrame()

    return addresseses

# This is just example code of how you can call the function locally
@stub.local_entrypoint()
def main():    
    result = get_addresses.local(
        "21901", "for_sale")
    result.to_csv("addresses_test1.csv", index=False)
    result = get_addresses.local(
        "21901", "sold21")
    result.to_csv("addresses_test2.csv", index=False)
