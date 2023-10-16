
## ⚙️ Installation

Open a terminal and run (Requires Python 3.7+):

```bash
pip install nextpy
```

## 🥳 Create your first app

Installing `dotreact` also installs the `dotreact` command line tool.

Test that the install was successful by creating a new project. (Replace `my_app_name` with your project name):

```bash
mkdir my_app_name
cd my_app_name
dotreact init
```

This command initializes a template app in your new directory. 

You can run this app in development mode:

```bash
dotreact run
```

You should see your app running at http://localhost:3000.

Now you can modify the source code in `my_app_name/my_app_name.py`. Dotreact has fast refreshes so you can see your changes instantly when you save your code.


## 🫧 Example App

Let's go over an example: creating an image generation UI around DALL·E. For simplicity, we just call the OpenAI API, but you could replace this with an ML model run locally.

&nbsp;



&nbsp;

Here is the complete code to create this. This is all done in one Python file!

```python
import dotreact as dr
import openai

openai.api_key = "YOUR_API_KEY"

class State(dr.State):
    """The app state."""
    prompt = ""
    image_url = ""
    processing = False
    complete = False

    def get_image(self):
        """Get the image from the prompt."""
        if self.prompt == "":
            return dr.window_alert("Prompt Empty")

        self.processing, self.complete = True, False
        yield
        response = openai.Image.create(prompt=self.prompt, n=1, size="1024x1024")
        self.image_url = response["data"][0]["url"]
        self.processing, self.complete = False, True
        

def index():
    return dr.center(
        dr.vstack(
            dr.heading("DALL·E"),
            dr.input(placeholder="Enter a prompt", on_blur=State.set_prompt),
            dr.button(
                "Generate Image",
                on_click=State.get_image,
                is_loading=State.processing,
                width="100%",
            ),
            dr.cond(
                State.complete,
                     dr.image(
                         src=State.image_url,
                         height="25em",
                         width="25em",
                    )
            ),
            padding="2em",
            shadow="lg",
            border_radius="lg",
        ),
        width="100%",
        height="100vh",
    )

# Add state and page to the app.
app = dr.App()
app.add_page(index, title="dotreact:DALL·E")
app.compile()
```

## Let's break this down.

### **Dotreact UI**

Let's start with the UI.

```python
def index():
    return dr.center(
        ...
    )
```

This `index` function defines the frontend of the app.

We use different components such as `center`, `vstack`, `input`, and `button` to build the frontend. Components can be nested within each other
to create complex layouts. And you can use keyword args to style them with the full power of CSS.


### **State**

Dotreact represents your UI as a function of your state.

```python
class State(dr.State):
    """The app state."""
    prompt = ""
    image_url = ""
    processing = False
    complete = False
```

The state defines all the variables (called vars) in an app that can change and the functions that change them.

Here the state is comprised of a `prompt` and `image_url`. There are also the booleans `processing` and `complete` to indicate when to show the circular progress and image.

### **Event Handlers**

```python
def get_image(self):
    """Get the image from the prompt."""
    if self.prompt == "":
        return dr.window_alert("Prompt Empty")

    self.processing, self.complete = True, False
    yield
    response = openai.Image.create(prompt=self.prompt, n=1, size="1024x1024")
    self.image_url = response["data"][0]["url"]
    self.processing, self.complete = False, True
```

Within the state, we define functions called event handlers that change the state vars. Event handlers are the way that we can modify the state in Dotreact. They can be called in response to user actions, such as clicking a button or typing in a text box. These actions are called events.

Our DALL·E. app has an event handler, `get_image` to which get this image from the OpenAI API. Using `yield` in the middle of an event handler will cause the UI to update. Otherwise the UI will update at the end of the event handler.

### **Routing**

Finally, we define our app.

```python
app = dr.App()
```

We add a page from the root of the app to the index component. We also add a title that will show up in the page preview/browser tab.

```python
app.add_page(index, title="DALL-E")
app.compile()
```

You can create a multi-page app by adding more pages.