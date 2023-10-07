# **SleepyEmoji**
*Fetch your favorite emojis fast!*

<br />

## **Welcome to sleepyemoji!**
There's now a paralyzing volume of unicode characters known as "emojis", which is great for creative expression, but bad for fetching the ~%10 of emojis you ever care to use.

SleepyEmoji has entered the chat!

<br />

### **Table of Contents** 📖
<hr>

  - **Get Started**
  - Usage
  - Technologies
  - Contribute
  - Acknowledgements
  - License/Stats/Author

<br />

## **Get Started 🚀**
<hr>

```sh
pip install sleepyemoji
pip install --upgrade sleepyemoji
```

<br />

## **Usage ⚙**
<hr>

Fetch dependencies:
```sh
pip install -r requirements.txt
```

Set a function in your shell environment to run a script like:
```sh
# pip install sleepyemoji
# pip install --upgrade sleepyemoji

from sleepyemoji import sleepyemoji
from sys import argv, exit

sleepyemoji(argv[1:])
exit(0)
```

Presuming you've named said function `emoji`, print the help message:
```sh
emoji --help
```

<br />

## **Technologies 🧰**
<hr>

  - [prettytable]()
  - [typer]()

<br />

## **Contribute 🤝**
<hr>

If you feel slighted by your favorite emojis not being list in `toolchain/emojis`, submit a PR 😊.

<br />

## **Acknowledgements 💙**
<hr>

Thanks to my late cat Merlin, who whispered best practices in my ear while I wrote this.

<br />

## **License, Stats, Author 📜**
<hr>

<img align="right" alt="example image tag" src="https://i.imgur.com/jtNwEWu.png" width="200" />

<!-- badge cluster -->

![PyPI - License](https://img.shields.io/pypi/l/sleepyemoji?style=plastic)

<!-- / -->
See [License](TODO) for the full license text.

This package was authored by *Isaac Yep*.