# Oqtant REST API

The Oqtant REST API is the RESTful backend to both Oqtant and the Oqtant Web App. It's API provides endpoints that can be interacted with via Oqtant's Client API to execute and expand upon the same functionality found in the Oqtant Web App.

To see a list of available endpoints and try them out you can visit our [OpenAPI documentation](http://oqtant.infleqtion.com/api/docs)

Communication with the Oqtant REST API will need to be authorized via your Oqtant Account. To accomplish this you will need to find your authentication token and provide it when using the OpenAPI documentation. To do this you can follow the steps below:

** Both of these methods requires that oqtant be installed on your system and in a place where your python interpreter can access it. Ideally this would be inside of a virtual environment. For more information on how to set that up refer to our [Installation Guide](INSTALL.md) **

## Authentication Token via Oqtant Notebooks

When installing Oqtant for the first time you will have received a set of walkthrough Jupyter notebooks. Within each of these notebooks you will find that the beginning of each one starts with a step called `Authenticate with Oqtant`. At the end of this step is a line that contains the following:

```python
token = get_user_token()
```

This line is what handles the authorization process for you to begin using Oqtant and as a result the Oqtant REST API. To be able to use the endpoints available in our OpenAPI documentation you will need to perform the following using the aforementioned step:

1. Start up Jupyter

   ```shell
   jupyter notebook
   ```

2. Open up one of the walkthrough notebooks. Depending on the location you started Jupyter from you may need to navigate the file explorer interface of Jupyter to find them.

3. In the code cell that contains the import statements and the `get_user_token()` method call, add a new line at the bottom that contains:

   ```python
   print(token)
   ```

4. Run the cell in the Jupyter notebook. It will open up a new tab in your default browser where you will be prompted to log in with your Oqtant Account. Once logged in successfully you can close that tab and return to the Jupyter notebook.

5. Now that you are authenticated you can see in the output of the code cell the printed authentication token. Select it all and copy it to your clipboard. This is your token.

## Authentication Token via Pure Python

While a set of walkthrough Jupyter notebooks is provided to be used with Oqtant, at its core it is a python library and can be used on its own. To be able to use the endpoint available in our OpenAPI documentation you will need to perform the following inside of a python interpreter:

1. Inside of a terminal with `oqtant` available open a python interpreter by running `python`

2. Import the `get_user_token`method

   ```python
   from oqtant.util.auth import get_user_token
   ```

3. Call the imported method and assign the result to a variable

   ```python
   token = get_user_token()
   ```

4. A new tab in your default browser will open where you will be prompted to log in with your Oqtant Account. Once logged in successfully you can close that tab and return to your python interpreter.

5. Print the contents of the variable

   ```python
   print(token)
   ```

6. Select all of the output from the printed variable and copy it to your clipboard. This is your token.

## Authorizing OpenAPI Documentation

Now that you have your authentication token from one of the previous methods you can authorize the OpenAPI documentation to allow for interaction with the Oqtant REST API endpoints. To do this follow the below steps:

1. Navigate to our [OpenAPI documentation](https://oqtant.infleqtion.com/api/docs)

2. Once loaded you will see a list of the endpoints provided by the Oqtant REST API. Most of these will show a lock icon next to them on the right-hand side. Endpoints with a lock will require the authentication token we retrieved from the above methods.

3. Near the top right-hand side of the page you will see a green button with the text `Authorize`. Clicking on this will open a pop-up with a form to input `HTTPBearer`inside.

4. Paste the token from our clipboard into this field and click `Authorize`.

5. You should now see a message that says `Authorized`. You can close the pop-up and begin using the endpoints that require an authentication token.
