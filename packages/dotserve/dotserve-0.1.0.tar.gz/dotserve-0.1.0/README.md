```diff
+ Searching for Pynecone? You are in the right repo. Pynecone has been renamed to Dotserve. +
```

<div align="center">
<img src="https://raw.githubusercontent.com/dotserve/dotserve/main/docs/images/dotserve_dark.svg#gh-light-mode-only" alt="Dotserve Logo" width="300px">
<img src="https://raw.githubusercontent.com/dotserve/dotserve/main/docs/images/dotserve_light.svg#gh-dark-mode-only" alt="Dotserve Logo" width="300px">

<hr>

### **✨ Performant, customizable web apps in pure Python. Deploy in seconds. ✨**
[![PyPI version](https://badge.fury.io/py/dotserve.svg)](https://badge.fury.io/py/dotserve)
![tests](https://github.com/pynecone-io/pynecone/actions/workflows/integration.yml/badge.svg)
![versions](https://img.shields.io/pypi/pyversions/dotserve.svg)
[![Documentaiton](https://img.shields.io/badge/Documentation%20-Introduction%20-%20%23007ec6)](https://dotagent.dev/docs/getting-started/introduction)
[![Discord](https://img.shields.io/discord/1029853095527727165?color=%237289da&label=Discord)](https://discord.gg/T5WSbC2YtQ)
</div>

---
[English](https://github.com/dot-agent/dotserve/blob/main/README.md) | [简体中文](https://github.com/dot-agent/dotserve/blob/main/docs/zh/zh_cn/README.md) | [繁體中文](https://github.com/dot-agent/dotserve/blob/main/docs/zh/zh_tw/README.md) | [Türkçe](https://github.com/dot-agent/dotserve/blob/main/docs/tr/README.md)
---
## ⚙️ Installation

Open a terminal and run (Requires Python 3.7+):

```bash
pip install dotserve
```

## 🥳 Create your first app

Installing `dotserve` also installs the `dotserve` command line tool.

Test that the install was successful by creating a new project. (Replace `my_app_name` with your project name):

```bash
mkdir my_app_name
cd my_app_name
dotserve init
```

This command initializes a template app in your new directory. 

You can run this app in development mode:

```bash
dotserve run
```

You should see your app running at http://localhost:3000.

Now you can modify the source code in `my_app_name/my_app_name.py`. Dotserve has fast refreshes so you can see your changes instantly when you save your code.


## 🫧 Example App

Let's go over an example: creating an image generation UI around DALL·E. For simplicity, we just call the OpenAI API, but you could replace this with an ML model run locally.

&nbsp;

<div align="center">
<img src="https://raw.githubusercontent.com/dotserve/dotserve/main/docs/images/dalle.gif" alt="A frontend wrapper for DALL·E, shown in the process of generating an image." width="550" />
</div>

&nbsp;

Here is the complete code to create this. This is all done in one Python file!

```python
import dotserve as ds
import openai

openai.api_key = "YOUR_API_KEY"

class State(ds.State):
    """The app state."""
    prompt = ""
    image_url = ""
    processing = False
    complete = False

    def get_image(self):
        """Get the image from the prompt."""
        if self.prompt == "":
            return ds.window_alert("Prompt Empty")

        self.processing, self.complete = True, False
        yield
        response = openai.Image.create(prompt=self.prompt, n=1, size="1024x1024")
        self.image_url = response["data"][0]["url"]
        self.processing, self.complete = False, True
        

def index():
    return ds.center(
        ds.vstack(
            ds.heading("DALL·E"),
            ds.input(placeholder="Enter a prompt", on_blur=State.set_prompt),
            ds.button(
                "Generate Image",
                on_click=State.get_image,
                is_loading=State.processing,
                width="100%",
            ),
            ds.cond(
                State.complete,
                     ds.image(
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
app = ds.App()
app.add_page(index, title="dotserve:DALL·E")
app.compile()
```

## Let's break this down.

### **Dotserve UI**

Let's start with the UI.

```python
def index():
    return ds.center(
        ...
    )
```

This `index` function defines the frontend of the app.

We use different components such as `center`, `vstack`, `input`, and `button` to build the frontend. Components can be nested within each other
to create complex layouts. And you can use keyword args to style them with the full power of CSS.

Dotserve comes with [60+ built-in components](https://dotagent.dev/docs/library) to help you get started. We are actively adding more components, and it's easy to [create your own components](https://dotagent.dev/docs/advanced-guide/wrapping-react).

### **State**

Dotserve represents your UI as a function of your state.

```python
class State(ds.State):
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
        return ds.window_alert("Prompt Empty")

    self.processing, self.complete = True, False
    yield
    response = openai.Image.create(prompt=self.prompt, n=1, size="1024x1024")
    self.image_url = response["data"][0]["url"]
    self.processing, self.complete = False, True
```

Within the state, we define functions called event handlers that change the state vars. Event handlers are the way that we can modify the state in Dotserve. They can be called in response to user actions, such as clicking a button or typing in a text box. These actions are called events.

Our DALL·E. app has an event handler, `get_image` to which get this image from the OpenAI API. Using `yield` in the middle of an event handler will cause the UI to update. Otherwise the UI will update at the end of the event handler.

### **Routing**

Finally, we define our app.

```python
app = ds.App()
```

We add a page from the root of the app to the index component. We also add a title that will show up in the page preview/browser tab.

```python
app.add_page(index, title="DALL-E")
app.compile()
```

You can create a multi-page app by adding more pages.

## 📑 Resources

<div align="center">

📑 [Docs](https://dotagent.dev/docs/getting-started/introduction) &nbsp; |  &nbsp; 🗞️ [Blog](https://dotagent.dev/blog) &nbsp; |  &nbsp; 📱 [Component Library](https://dotagent.dev/docs/library) &nbsp; |  &nbsp; 🖼️ [Gallery](https://dotagent.dev/docs/gallery) &nbsp; |  &nbsp; 🛸 [Deployment](https://dotagent.dev/docs/hosting/deploy)  &nbsp;   

</div>





## ✅ Status

Dotserve launched in December 2022 with the name Pynecone.

As of July 2023, we are in the **Public Beta** stage.

-   :white_check_mark: **Public Alpha**: Anyone can install and use Dotserve. There may be issues, but we are working to resolve them actively.
-   :large_orange_diamond: **Public Beta**: Stable enough for non-enterprise use-cases.
-   **Public Hosting Beta**: _Optionally_, deploy and host your apps on Dotserve!
-   **Public**: Dotserve is production ready.

Dotserve has new releases and features coming every week! Make sure to :star: star and :eyes: watch this repository to stay up to date.

## Contributing

We welcome contributions of any size! Below are some good ways to get started in the Dotserve community.

-   **Join Our Discord**: Our [Discord](https://discord.gg/T5WSbC2YtQ) is the best place to get help on your Dotserve project and to discuss how you can contribute.
-   **GitHub Discussions**: A great way to talk about features you want added or things that are confusing/need clarification.
-   **GitHub Issues**: These are an excellent way to report bugs. Additionally, you can try and solve an existing issue and submit a PR.

We are actively looking for contributors, no matter your skill level or experience.

## License

Dotserve is open-source and licensed under the [Apache License 2.0](LICENSE).
