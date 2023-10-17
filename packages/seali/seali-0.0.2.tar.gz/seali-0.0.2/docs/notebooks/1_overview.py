# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     custom_cell_magics: kql
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.11.2
#   kernelspec:
#     display_name: base
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Overview
#
# SeaLI connects to your GDataSea instance, which can be remote or local.
#
# By default it will try to connect to https://localhost:3131 and you will need to have [GDataSea](https://github.com/gdsfactory/gdatasea/) running.
#
# If you want to connect to a different server you have 3 options:
#
# 1. Define an environment variable `SEALI_URL`. `export SEALI_URL='https://mydatasea.mycompany.com`
# 2. Define a `seali.yml` on your current working directory.
#
# ```yaml
# url: localhost:3131
# ```
#
# 3. Modify `seali.CONF`.
#
# ```python
# import seali as sea
#
# sea.CONF.url = 'https://mydatasea.mycompany.com'
#
# ```

# %%
import seali as sea

# %% [markdown]
# ## Create new project
#
# You can easily create a new project from the web interface or using python. A project requires an EDA file (`.gds`, `.oas`) and optionally a Klayout layer properties for layer names and colors (`.lyp`).
#
# Lets upload a simple reticle.

# %%
response = sea.project.create(
    file=sea.PATH.test_data / "sample_reticle.gds",
    name="my_sample_reticle",
    lyp_file=sea.PATH.test_data / "layers.lyp",
)
print(response)

# %% [markdown]
# If everything went well you should receive a "200 OK" HTTP status code, commonly used to indicate that a request has succeeded.
#
# If you're working with web servers, APIs, or web development in general, a "200 OK" status is standard communication for successful HTTP requests.
#
# If you're testing an API or a web server, you might receive a 200 status code response when you make a GET, POST, or other types of HTTP requests, and the server successfully processes it.

# %%

if response.status_code == 200:
    print("Success!")
    # You can also use response.json() to parse JSON responses or response.text to get the raw response body
else:
    print("An error has occurred. Status code:", response.status_code)


# %% [markdown]
# However if you try to post a new project with a name that already exists, you should receive an error response.

# %%
response = sea.project.create(
    file=sea.PATH.test_data / "sample_reticle.gds",
    name="my_sample_reticle",
    lyp_file=sea.PATH.test_data / "layers.lyp",
)
print(response)

# %%
if response.status_code == 200:
    print("Success!")
    # Process your successful response here
elif response.status_code == 400:
    print("Bad Request!")
    # Try to parse and print more info:
    try:
        error_details = (
            response.json()
        )  # Assuming JSON response with details of the error
        print(error_details)
    except ValueError:  # includes simplejson.decoder.JSONDecodeError
        print(
            "Response content is not in JSON format or 'Content-Type' header is not 'application/json'"
        )
        print(response.text)  # display the raw response text
else:
    print(f"An error has occurred. Status code: {response.status_code}")

# %% [markdown]
# ## Delete project
#
# You can also easily delete a project with the python API. Given that you have the right permissions.

# %%
sea.project.delete("my_sample_reticle")
