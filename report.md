# Embedding Videos and Linking to External Pages in HTML: A Beginner's Guide

So you've built a fantastic webpage, but it's missing that *something*... that dynamic visual element that truly grabs your audience's attention.  Or perhaps you want to link to a relevant resource without interrupting the user's flow.  Fear not! This tutorial will show you how to seamlessly embed videos and link to external pages using HTML, making your web pages come alive.

We'll focus on two key elements: embedding a video and creating external links. Let's dive in!

## Embedding Videos: The Heart of Multimedia

Embedding videos is a crucial step in enhancing user engagement.  In this example, we'll use the `<video>` tag, a powerful tool that supports various video formats.  We'll primarily use MP4, a widely compatible format, and include a WebM file as a backup for browsers that may not support MP4.  This ensures your video plays smoothly on a broader range of devices.

Here's how you would embed a video using HTML:

```html
<video width="640" height="360" controls autoplay loop>
  <source src="myvideo.mp4" type="video/mp4">
  <source src="myvideo.webm" type="video/webm">
Your browser does not support the video tag.
</video>
```

Let's break down this code snippet:

* **`<video width="640" height="360" controls autoplay loop>`:** This opening tag defines the video player.  `width` and `height` set the dimensions, `controls` adds the play/pause and volume controls, `autoplay` starts the video automatically (use cautiously!), and `loop` makes it play continuously.
* **`<source src="myvideo.mp4" type="video/mp4">`:** This specifies the MP4 video file.  Replace `"myvideo.mp4"` with your actual file name.  The `type` attribute ensures the browser identifies the file type correctly.
* **`<source src="myvideo.webm" type="video/webm">`:** This provides a WebM alternative for better browser compatibility.
* **`Your browser does not support the video tag.`:** This fallback message displays if the browser doesn't support the `<video>` tag itself.


Remember to replace `"myvideo.mp4"` and `"myvideo.webm"` with the actual file paths to your video files.  Make sure these files are in the same directory as your HTML file or specify the correct relative or absolute paths.

## Linking to External Pages: Expanding Your Reach

Linking to external pages enhances your website's value by providing users with further reading or related information.  To open these links in a new tab, we leverage the `target="_blank"` attribute within the `<a>` (anchor) tag.

Here's an example:

```html
<a href="https://en.wikipedia.org/wiki/HTML" target="_blank">Learn more about HTML on Wikipedia</a>
```

This code creates a clickable link to the Wikipedia page about HTML, and `target="_blank"` ensures the link opens in a new tab or window, keeping the user on your current page.


## Conclusion: Combining Power and Functionality

By combining the power of video embedding and external linking, you can create dynamic and informative web pages that engage your audience and provide valuable resources. Remember to always consider user experience when deciding whether to use autoplay and to always test your code across different browsers and devices.  Happy coding!